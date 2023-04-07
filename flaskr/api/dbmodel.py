from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# init my cool db
db = SQLAlchemy()

# init sweet marshmallow
ma = Marshmallow()


# url shortner model class
class url_mapper(db.Model):
    __tablename__ = "url_mapper"
    url_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    short_url_id = db.Column(db.String(7), unique=True)
    short_base_url = db.Column(db.String(200))
    full_url = db.Column(db.String(500), unique=True)

    def __init__(self, url_id, short_url_id, short_base_url, full_url):
        self.url_id = url_id
        self.short_url_id = short_url_id
        self.short_base_url = short_base_url
        self.full_url = full_url


# url mapper class Schema to serealize
class UrlMapperSchema(ma.Schema):
    class Meta:
        fields = ("url_id", "short_url_id", "short_base_url", "full_url")


# Initialize the schemas
url_mapper_schema = UrlMapperSchema()