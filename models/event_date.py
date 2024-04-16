from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime

from models import Base


class EventDate(Base):
  __tablename__ = 'event_date'

  id = Column(Integer, primary_key=True)
  date = Column(DateTime)
  event_id = Column(Integer, ForeignKey('event.pk_event'), nullable=False)

  def __init__(self, date: str):
    self.date = datetime.strptime(date, '%Y-%m-%d')
