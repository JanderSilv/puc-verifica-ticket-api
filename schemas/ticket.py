from typing import List
from pydantic import BaseModel, Field, RootModel


class TicketGetSchema(BaseModel):
  id: int = Field(ge=1, description='Ticket ID')


class TicketSchema(BaseModel):
  id: int
  code: str
  created_at: str
  contactEmails: List[str]
  event_id: int


class TicketVerifySchema(BaseModel):
  matches: bool = Field(
      description='Defines if the ticket was already registered')
  contact_emails: List[str] = Field(
      description='List of contact emails associated with the ticket')


class TicketCreateSchema(BaseModel):
  code: str = Field(min_length=1, max_length=100, description='Ticket code')
  event_id: int = Field(ge=1, description='Event ID')
  contact_email: str = Field(
      min_length=1, max_length=100, description='Contact email')


class TicketListSchema(RootModel):
  root: List[TicketSchema]


class TicketDeleteSchema(BaseModel):
  id: int = Field(ge=1, description='Ticket ID')


class TicketsByEventSchema(BaseModel):
  event_id: int = Field(ge=1, description='Event ID')
