from urllib.parse import unquote
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

from models import Base


class Platform(Base):
  __tablename__ = 'platform'

  id = Column("pk_platform", Integer, primary_key=True)
  name = Column(String(100), unique=True)
  image = Column(String(255))
  created_at = Column(DateTime, default=datetime.now())

  def __init__(self, name: str, image: str):
    self.name = name
    self.image = unquote(image)

  def to_json(self):
    return {
        'id': self.id,
        'name': self.name,
        'image': unquote(self.image),
        'created_at': self.created_at.strftime('%d/%m/%Y %H:%M:%S')
    }
