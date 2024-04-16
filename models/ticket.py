from datetime import datetime
from typing import List
from sqlalchemy import Column, DateTime, ForeignKey, String, Integer
from sqlalchemy.orm import relationship, Mapped

from models import Base
from models.ticket_contact_email import TicketContactEmail


class Ticket(Base):
  __tablename__ = 'ticket'

  id = Column("pk_ticket", Integer, primary_key=True)
  code = Column(String(100))
  created_at = Column(DateTime, default=datetime.now())
  __contact_emails: Mapped[List["TicketContactEmail"]] = relationship(
      "TicketContactEmail", cascade="all, delete-orphan")
  event_id = Column(Integer, ForeignKey('event.pk_event'), nullable=False)

  def __init__(self, code: str, contact_email: str, event_id: int):
    self.code = code
    self.__contact_emails = [TicketContactEmail(contact_email)]
    self.event_id = event_id

  def add_contact_emails(self, contact_emails: List[TicketContactEmail]):
    for contact_email in contact_emails:
      self.__contact_emails.append(contact_email)

  def get_contact_emails(self):
    return [contact_email.email for contact_email in self.__contact_emails]

  def to_json(self):
    return {
        'id': self.id,
        'code': self.code,
        'created_at': self.created_at,
        'contact_emails': [contact_email.email for contact_email in self.__contact_emails],
        'event_id': self.event_id
    }
