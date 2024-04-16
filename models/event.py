from datetime import datetime
from typing import List
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models import Base
from models.event_date import EventDate


class Event(Base):
  __tablename__ = 'event'

  id = Column("pk_event", Integer, primary_key=True)
  name = Column(String(100), unique=True)
  image = Column(String(255))
  created_at = Column(DateTime, default=datetime.now())
  platform_id = Column(Integer, ForeignKey(
      'platform.pk_platform'), nullable=False)
  dates = relationship("EventDate", cascade="all, delete-orphan")
  tickets = relationship("Ticket")

  def __init__(self, name: str, image: str, platform_id: int):
    self.name = name
    self.image = image
    self.platform_id = platform_id

  def add_dates(self, dates: List[EventDate]):
    for date in dates:
      self.dates.append(date)

  def to_json(self):
    return {
        'id': self.id,
        'name': self.name,
        'image': self.image,
        'dates': [eventDate.date for eventDate in self.dates],
        'platform_id': self.platform_id
    }
