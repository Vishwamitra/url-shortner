from flask import Blueprint, jsonify, request
from model.id import ID
from model.url import URL
from schema.id import IDSchema
from schema.url import URLSchema
from model.error import BadRequest, NotFound

# from shortner import getShortURL

id_restapi = Blueprint("id_restapi", __name__)


@id_restapi.route("/", methods=["GET"])
def getId():
    """
    Get all shorten URL.
    ---
    tags:
      - ID APIs
    description: Get all shorten URL.
    responses:
        200:
            description: A list of shorten URL.
    """
    id = ID(id="123")

    # validation and serialization
    try:
        payload = IDSchema().dump(id)
    except:
        raise BadRequest("Invalid payload.")
    return payload, 200


@id_restapi.route("/", methods=["POST"])
def createId():
    """
    Create shorten URL by passing URL in payload.
    ---
    tags:
      - ID APIs
    description: Create shorten URL by passing URL in payload.
    parameters:
        - name: URL
          in: body
          schema:
            id: URL
            required:
                - url
            properties:
                url:
                    type: string
                    example: "https://www.youtube.com"
                    description: The URL to shorten.
    responses:
        201:
            description: A shorten URL.
        400:
            description: Bad URL in the payload.
    """
    try:
        request_data = request.get_json()
        url = URLSchema.load(request_data)
    except:
        raise BadRequest("Invalid URL")

    # id = getShortURL(url.url)
    id = "123"
    if not id:
        raise BadRequest("Invalid URL")

    # validation and serialization
    try:
        payload = IDSchema().dump(id)
    except:
        raise BadRequest("Invalid payload.")
    return payload, 201


@id_restapi.route("/", methods=["DELETE"])
def deleteId():

    raise NotFound("Delete Method Not Found")
