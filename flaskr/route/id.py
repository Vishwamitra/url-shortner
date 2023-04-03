from flask import Blueprint
from model.error import BadRequest, NotFound
from shortner import getShortURL

id_restapi = Blueprint("id_restapi", __name__)

@id_restapi.route("/", methods=["GET"])
def getId():
    
    return "", 200

@id_restapi.route("/", methods=["POST"])
def createId():

    id = getShortURL("https://www.youtube.com/watch?v=NQUo3vITjgY")
    if not id:
        raise BadRequest("Bad URL")

    return id, 201

@id_restapi.route("/", methods=["DELETE"])
def deleteId():

    return "", 404