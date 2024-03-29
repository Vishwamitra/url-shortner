import os
from sqlalchemy.sql import func
from dbmodel import db, UrlMapper, url_mapper_schema, UrlUserMapper
from sqlalchemy.orm.exc import UnmappedInstanceError
from model.error import InternalServer
from lib.shortener import get_next_unique_id


def create_short_url(full_url, user_id) -> dict:
    """
    Function to create a new record in database for any new URL

    parameters:
        full_url: complete url including http or https as well

    returns:
        json response with following details:
        url_id : unique primary key [highest int]
        short_url_id : new generated short url [without domain]
        full_url : full url which was passed as input
    """
    next_unique_id = get_next_unique_id(full_url)
    # add url mapping
    new_url = UrlMapper(
        short_url_id=next_unique_id,
        full_url=full_url,
    )
    db.session.add(new_url)
    db.session.commit()
    # add user and url mapping
    url_id, = db.session.query(UrlMapper.url_id).filter_by(short_url_id=next_unique_id).first()
    new_url_user = UrlUserMapper(url_id=url_id, user_id=user_id)
    db.session.add(new_url_user)
    db.session.commit()

    return url_mapper_schema.dump(new_url)


def update_full_url(short_url_id, full_url):
    url_map = UrlMapper.query.filter_by(short_url_id=short_url_id).first()
    if url_map is None:
        raise UnmappedInstanceError(f"No row found with short_url_id={short_url_id}")
    url_map.full_url = full_url
    db.session.commit()

    return short_url_id


def delete_short_url(short_url_id) -> str:
    """
    To delete the mapping of short url
    parameter:
        short_url_id : short ur id which is without the domain name [base url]
    returns:
        short url id
    """
    db.session.query(UrlMapper).filter_by(short_url_id=short_url_id).delete()
    db.session.commit()

    return short_url_id


def is_full_url_not_found(full_url, user_id) -> bool:
    not_found = False
    count = (
        db.session.query(func.count(UrlUserMapper.url_id))
        .filter_by(user_id=user_id)
        .join(UrlMapper, UrlUserMapper.url_id == UrlMapper.url_id)
        .filter(UrlMapper.full_url == full_url)
        .scalar()
    )
    if count < 1:
        not_found = True
    return not_found


def is_short_url_id_not_found(short_url_id, user_id) -> bool:
    not_found = False
    count = (
        db.session.query(func.count(UrlUserMapper.url_id))
        .filter_by(user_id=user_id)
        .join(UrlMapper, UrlUserMapper.url_id == UrlMapper.url_id)
        .filter(UrlMapper.short_url_id == short_url_id)
        .scalar()
    )
    if count < 1:
        not_found = True
    return not_found


def query_url_mapping(*args, short_url_id=None, full_url=None, user_id=None):
    statement = db.session.query(UrlMapper.url_id)
    if user_id is not None:
        statement = (
            db.session.query(UrlUserMapper.url_id)
            .filter_by(user_id=user_id)
            .join(UrlMapper, UrlUserMapper.url_id == UrlMapper.url_id)
        )

    url_id = None
    if args:
        raise InternalServer("Provide short_url_id or full_url to get url_mapping")
    elif short_url_id:
        url_id = statement.filter(UrlMapper.short_url_id == short_url_id).scalar()
        if url_id is None:
            return None
            # raise InternalServer("short_url_id not found in database.")
    elif full_url:
        url_id = statement.filter(UrlMapper.full_url == full_url).scalar()
        if url_id is None:
            return None
            # raise InternalServer("short_url_id not found in database.")

    if url_id is not None:
        url_map = UrlMapper.query.get(url_id)
        result = url_mapper_schema.dump(url_map)
    # get all result if not provide variable
    else:
        result = []
        url_id_list = statement.all()
        for url_id in url_id_list:
            url_map = UrlMapper.query.get(url_id)
            result.append(url_mapper_schema.dump(url_map))

    return result
