from pydantic import BaseModel, Field, RootModel
from typing import List


class EventSchema(BaseModel):
  id: int = Field(ge=1, description='ID do evento')
  name: str = Field(min_length=1, max_length=100, description='Nome do evento')
  image: str = Field(min_length=1, max_length=255,
                     description='URL da imagem do evento')
  dates: List[str] = Field(min_items=1, description='Datas do evento')
  created_at: str = Field(description='Data de criação do evento')


class EventCreateSchema(BaseModel):
  name: str = Field(min_length=1, max_length=100, description='Nome do evento')
  image: str = Field(min_length=1, max_length=255,
                     description='URL da imagem do evento')
  dates: List[str] = Field(min_items=1, description='Datas do evento')
  platform_id: int = Field(ge=1, description='ID da plataforma')


class EventListSchema(RootModel):
  root: List[EventSchema] = []


class EventsByPlatformSchema(BaseModel):
  platform_id: int = Field(ge=1, description='ID da plataforma')


class EventDeleteSchema(BaseModel):
  id: int = Field(ge=1, description='ID do evento')
