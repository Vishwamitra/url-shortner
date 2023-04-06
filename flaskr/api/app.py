from flask import Flask
import os
from flasgger import Swagger
from route.url import url_restapi
from route.id import id_restapi
from route.error_controller import error_controller

from dbmodel import db, URL_MAPPER, UrlMapperSchema

app = Flask(__name__, instance_relative_config=True)


app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db.app = app
db.init_app(app)
with app.app_context():
    db.create_all()

# For Documatation
swagger = Swagger(app)

app.register_blueprint(url_restapi)
app.register_blueprint(id_restapi)
app.register_blueprint(error_controller)


if __name__ == "__main__":
    app.run(debug=True)
