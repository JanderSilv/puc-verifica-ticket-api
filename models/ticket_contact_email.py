from sqlalchemy import Column, String, Integer, ForeignKey
from models import Base


class TicketContactEmail(Base):
  __tablename__ = 'ticket_contact_email'

  id = Column("pk_ticket_contact_email", Integer, primary_key=True)
  email = Column(String(100))
  ticket_id = Column(Integer, ForeignKey('ticket.pk_ticket'))

  def __init__(self, email: str):
    self.email = email.strip().lower()
