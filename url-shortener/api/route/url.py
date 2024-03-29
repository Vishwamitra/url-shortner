import os
from flask import Blueprint, jsonify, request
from model.url import FullURL, URL
from model.shorturl import ShortURL
from model.error import BadRequest, NotFound
from schema.url import FullURLSchema, URLSchema
from schema.shorturl import ShortURLSchema
from marshmallow import ValidationError
from lib.dbquery import (
    query_url_mapping,
    update_full_url,
    delete_short_url,
    is_full_url_not_found,
    is_short_url_id_not_found
)
from lib.authenticator import require_login, decode_token

url_restapi = Blueprint("url_restapi", __name__)


@url_restapi.route("/<short_url_id>", methods=["GET"])
@require_login
def get_url(short_url_id):
    """
    Get the full URL through short URL ID.
    ---
    tags:
      - Full URL APIs
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: The format is `Bearer <access_token>`.
      - in: path
        name: short_url_id
        type: string
        required: true
        description: The result of Base 62 encode of URL ID
    description: Get the URL information of the corresponding short URL ID.
    responses:
        301:
            description: Get the URL information of the corresponding short URL ID.
            schema:
                $ref: '#/definitions/URL'
        403:
            description: Invalid access token.
        404:
            description: Short URL ID not found.
    """
    # get user_id from token
    _, token_payload, _ = decode_token()
    user_id = token_payload["sub"]

    if is_short_url_id_not_found(short_url_id, user_id):
        raise NotFound("Short URL ID not found.")

    url_mapping = query_url_mapping(short_url_id=short_url_id, user_id=user_id)
    short_base_url = os.environ.get("BASE_URL_FOR_SHORT_URL")
    url = URL(
        short_url_id=url_mapping["short_url_id"],
        short_url=f"{short_base_url}/{url_mapping['short_url_id']}",
        full_url=url_mapping["full_url"]
    )

    payload = URLSchema().dump(url)
    return payload, 301


@url_restapi.route("/<short_url_id>", methods=["PUT"])
@require_login
def update_url(short_url_id):
    """
    Update the mapping of short URL ID and full URL.
    ---
    tags:
      - Full URL APIs
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: The format is `Bearer <access_token>`.
      - in: path
        name: short_url_id
        type: string
        required: true
        description: The result of Base 62 encode of URL ID
      - name: FullURL
        in: body
        schema:
            $ref: '#/definitions/FullURL'
    description: Update the mapping of short URL ID and full URL and get the update URL information.
    responses:
        200:
            description: Updated succeed.
            schema:
                $ref: '#/definitions/URL'
        400:
            description: Invalid payload.
        403:
            description: Invalid access token.
        404:
            description: Short URL ID not found.
    """
    # get user_id from token
    _, token_payload, _ = decode_token()
    user_id = token_payload["sub"]

    try:
        request_data = request.get_json()
        full_url = FullURLSchema().load(request_data)
    except ValidationError:
        raise BadRequest("Invalid payload.")
    
    if is_short_url_id_not_found(short_url_id, user_id):
        raise NotFound("Short URL ID not found.")

    # the mapping of full url to short url already existed
    if not is_full_url_not_found(full_url.full_url, user_id):
        # get the exist mapping and delete (ignore if same)
        url_mapping_old = query_url_mapping(full_url=full_url.full_url, user_id=user_id)
        if url_mapping_old["short_url_id"] != short_url_id:
            delete_short_url(url_mapping_old["short_url_id"])

    # update mapping
    _ = update_full_url(short_url_id, full_url.full_url)

    # query the update result
    url_mapping = query_url_mapping(full_url=full_url.full_url, user_id=user_id)
    short_base_url = os.environ.get("BASE_URL_FOR_SHORT_URL")
    url = URL(
        short_url_id=url_mapping["short_url_id"],
        short_url=f"{short_base_url}/{url_mapping['short_url_id']}",
        full_url = url_mapping["full_url"]
    )

    payload = URLSchema().dump(url)
    return jsonify(payload), 200


@url_restapi.route("/<short_url_id>", methods=["DELETE"])
@require_login
def delete_url(short_url_id):
    """
    Delete the mapping of short URL ID and full URL.
    ---
    tags:
      - Full URL APIs
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: The format is `Bearer <access_token>`.
      - in: path
        name: short_url_id
        type: string
        required: true
        description: The result of Base 62 encode of URL ID
    description: Get all shorten URL.
    responses:
        204:
            description: Delete succeed.
        403:
            description: Invalid access token.
        404:
            description: Short URL ID not found.
    """
    # get user_id from token
    _, token_payload, _ = decode_token()
    user_id = token_payload["sub"]
    
    if is_short_url_id_not_found(short_url_id, user_id):
        raise NotFound("Short URL ID not found.")
    else:
        delete_short_url(short_url_id)
        return jsonify({}), 204
