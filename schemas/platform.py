from pydantic import BaseModel, Field, RootModel
from typing import List


class PlatformSchema(BaseModel):
  id: int = Field(ge=1, description='ID da plataforma')
  name: str = Field(min_length=1, max_length=100,
                    description='Nome da plataforma')
  image: str = Field(min_length=1, max_length=255,
                     description='Imagem da plataforma')
  created_at: str = Field(description='Data de criação da plataforma')


class PlatformCreateSchema(BaseModel):
  name: str = Field(min_length=1, max_length=100,
                    description='Nome da plataforma')
  image: str = Field(min_length=1, max_length=255,
                     description='Imagem da plataforma')


class PlatformListSchema(RootModel):
  root: List[PlatformSchema] = Field(description='Lista de plataformas')


class PlatformDeleteSchema(BaseModel):
  id: int = Field(ge=1, description='ID da plataforma')
