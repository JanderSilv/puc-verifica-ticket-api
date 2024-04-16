from flask_openapi3 import Tag
from flask import request
from sqlalchemy.exc import IntegrityError

from app import app
from models import Session, Platform
from schemas.platform import *

base_url = '/api/platform'

platform_tag = Tag(
    name='platform', description='Operações relacionadas a plataformas')


@app.get(base_url, tags=[platform_tag], responses={200: PlatformListSchema})
def get_platforms():
  """Retorna todas as plataformas"""
  session = Session()
  platforms = session.query(Platform).all()

  if not platforms:
    return [], 200
  else:
    result = [platform.to_json() for platform in platforms]
    return result, 200


@app.post(base_url, tags=[platform_tag], responses={201: PlatformSchema})
def create_platform(body: PlatformCreateSchema):
  """Cria uma plataforma"""
  session = Session()
  platform = Platform(body.name, body.image)

  try:
    session.add(platform)
    session.commit()
  except IntegrityError:
    session.rollback()
    return {'message': 'Essa plataforma já existe'}, 400

  return platform.to_json(), 201


@app.delete(f'{base_url}/<int:id>', tags=[platform_tag], responses={204: None})
def delete_platform(path: PlatformDeleteSchema):
  """Deleta uma plataforma"""
  session = Session()
  platform = session.query(Platform).get(path.id)

  if not platform:
    return {'message': 'Plataforma não encontrada'}, 404

  session.delete(platform)
  session.commit()

  return "", 204
