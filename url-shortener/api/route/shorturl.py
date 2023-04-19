from flask import Blueprint, request
from model.shorturl import ShortURL
from model.url import FullURL, URL
from schema.shorturl import ShortURLSchema
from schema.url import FullURLSchema, URLSchema
from model.error import BadRequest, NotFound, InternalServer
from shortner import query_url_mapping, create_short_url, is_full_url_not_found

shorturl_restapi = Blueprint("shorturl_restapi", __name__)


@shorturl_restapi.route("/", methods=["GET"])
def get_short_url_api():
    """
    Get all shorten URL.
    ---
    tags:
      - Short URL APIs
    description: Get all URL information.
    responses:
        200:
            description: Get a list of URL information.
            schema:
                type: array
                items:
                    $ref: '#/definitions/URL'
    """
    payload = []
    url_mapping_all = query_url_mapping()
    for url_mapping in url_mapping_all:
        url = URL(
            short_url_id=url_mapping["short_url_id"],
            short_url=f"{url_mapping['short_base_url']}/{url_mapping['short_url_id']}",
            full_url=url_mapping["full_url"]
        )
        payload.append(URLSchema().dump(url))

    return payload, 200


@shorturl_restapi.route("/", methods=["POST"])
def create_short_url_api():
    """
    Create shorten URL by passing a full URL in the payload.
    ---
    tags:
      - Short URL APIs
    description: Create shorten URL by passing a full URL in the payload.
    parameters:
      - name: FullURL
        in: body
        schema:
            $ref: '#/definitions/FullURL'
    responses:
        201:
            description: Create a shorten URL successed and reponse the shorted URL.
            schema:
                $ref: '#/definitions/ShortURL'
        400:
            description: Invalid payload.
    """
    try:
        request_data = request.get_json()
        full_url = FullURLSchema().load(request_data)
    except:
        raise BadRequest("Invalid payload.")

    # the mapping of full url to short url already existed
    if not is_full_url_not_found(full_url.full_url):
        raise BadRequest("The URL already has short URL.")

    url_mapping = create_short_url(full_url.full_url)
    data = ShortURL(
        short_url_id=url_mapping["short_url_id"],
        short_url=f"{url_mapping['short_base_url']}/{url_mapping['short_url_id']}",
    )
    
    payload = ShortURLSchema().dump(data)
    return payload, 201


@shorturl_restapi.route("/", methods=["DELETE"])
def delete_short_url_api():
    """
    Delete URL (no such method).
    ---
    tags:
      - Short URL APIs
    description: Delete URL (no such method).
    responses:
        404:
            description: Delete method not found.
    """
    raise NotFound("Delete method not found")