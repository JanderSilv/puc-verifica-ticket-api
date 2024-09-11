from flask_openapi3 import Tag
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as SessionMaker

from app import app
from models import Event, Platform, Session
from database import seed_events, seed_platforms
from schemas.exception import ResponseException
from schemas.ticket import *


base_url = '/api/seed'

database_seed_tag = Tag(
    name='Database seed',
    description='Operações relacionadas a seed de dados'
)


@app.post(base_url, tags=[database_seed_tag], responses={400: ResponseException})
def live_run():
  """ Popula o banco de dados com dados iniciais """
  session = Session()
  has_platform = check_database_has_platform(session)

  if has_platform:
    return {'message': 'Database already has data'}, 400

  seed_platforms(session)
  seed_events(session)

  return "", 200


def check_database_has_platform(session: SessionMaker):
  has_platform = session.query(Platform).first()
  if has_platform:
    return True
  else:
    return False
