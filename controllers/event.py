from flask_openapi3 import Tag
from flask import request
from sqlalchemy.exc import IntegrityError

from app import app
from models import Session, Event, Platform
from models.event_date import EventDate
from schemas.event import *
from schemas.exception import ResponseException

base_url = '/api/event'

event_tag = Tag(name='event', description='Operações relacionadas a eventos')


@app.get(base_url, tags=[event_tag], responses={200: EventListSchema})
def get_events():
  """Retorna todos os eventos"""
  session = Session()
  events = session.query(Event).all()

  if not events:
    return [], 200
  else:
    result = [event.to_json() for event in events]
    return result, 200


@app.get(f'{base_url}/platform/<int:platform_id>', tags=[event_tag], responses={200: EventSchema, 404: ResponseException})
def get_events_from_platform(path: EventsByPlatformSchema):
  """Retorna todos os eventos de uma plataforma"""
  session = Session()
  events = session.query(Event).filter_by(platform_id=path.platform_id).all()

  if not events:
    return {'message': 'Nenhum evento encontrado'}, 404
  else:
    result = [event.to_json() for event in events]
    return result, 200


@app.post(base_url, tags=[event_tag], responses={201: EventSchema, 400: ResponseException, 404: ResponseException})
def create_event(body: EventCreateSchema):
  """Cria um evento"""
  session = Session()

  platform_id = body.platform_id
  platform = session.query(Platform).get(platform_id)

  if not platform:
    return {'message': 'Plataforma não encontrada'}, 404

  event = Event(body.name, body.image, platform_id)
  event_dates = [EventDate(date) for date in body.dates]
  event.add_dates(event_dates)

  try:
    session.add(event)
    session.add_all(event_dates)
    session.commit()
  except IntegrityError:
    session.rollback()
    return {'message': 'Esse evento já existe'}, 400

  return event.to_json(), 201


@app.delete(f'{base_url}/<int:id>', tags=[event_tag], responses={204: None, 404: ResponseException})
def delete_event(path: EventDeleteSchema):
  """Deleta um evento"""
  session = Session()
  event = session.query(Event).get(path.id)

  if not event:
    return {'message': 'Evento não encontrado'}, 404

  session.delete(event)
  session.commit()

  return "", 204
