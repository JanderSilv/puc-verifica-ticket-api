from typing import List, Union
from flask_openapi3 import Tag
from flask import request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as SessionMaker

from app import app
from helpers import make_hash
from models import Event, Session, Ticket, TicketContactEmail
from schemas.exception import ResponseException
from schemas.ticket import *
from services import send_email


base_url = '/api/ticket'

ticket_tag = Tag(
    name='ticket', description='Operações relacionadas a ingressos')


@app.get(f"{base_url}/<int:id>", tags=[ticket_tag], responses={200: TicketSchema},)
def get_ticket(path: TicketGetSchema):
  """Recupera um ticket pelo seu ID."""
  session = Session()
  ticket = session.query(Ticket).get(path.id)

  if not ticket:
    return {'message': 'Ingresso não encontrado'}, 404
  else:
    return ticket.to_json(), 200


@app.get(f"{base_url}/event/<int:event_id>", tags=[ticket_tag], responses={200: TicketSchema})
def get_tickets_by_event(path: TicketsByEventSchema):
  """Recupera os ingressos pelo ID do evento."""
  session = Session()
  tickets = session.query(Ticket).filter_by(event_id=path.event_id).all()

  if not tickets:
    return {'message': 'Ingressos não encontrados'}, 404
  else:
    return [ticket.to_json() for ticket in tickets], 200


@app.post(base_url, tags=[ticket_tag], responses={200: TicketVerifySchema, 201: TicketVerifySchema, 400: ResponseException})
def create_ticket(body: TicketCreateSchema):
  """Cria um novo ingresso para um evento."""
  session = Session()
  event_id = body.event_id

  event = get_event(session, event_id)

  if not event:
    return {'message': 'Evento não encontrado'}, 404

  ticket_code_hash = make_hash(body.code)
  email_input = body.contact_email.strip().lower()

  ticket: Union[Ticket, None] = session.query(
      Ticket).filter_by(code=ticket_code_hash).first()

  if ticket:
    if check_ticket_already_has_email(ticket, email_input):
      return {
          'matches': 'owner',
          'contact_emails': ticket.get_contact_emails()
      }, 200

    send_warning_email(ticket.get_contact_emails(), email_input, event.name)

    contact_emails = update_ticket_contact_emails(session, ticket, email_input)
    contact_emails = [
        email for email in contact_emails if email != email_input]

    return {
        'matches': True,
        'contact_emails': contact_emails
    }, 200

  new_ticket = Ticket(ticket_code_hash, email_input, event_id)

  try:
    session.add(new_ticket)
    session.commit()
  except IntegrityError:
    session.rollback()
    return {'message': 'Erro ao criar ingresso'}, 400

  return {
      "matches": False,
      "contact_emails": [],
  }, 201


def get_event(session: SessionMaker, event_id: int) -> Event:
  return session.query(Event).get(event_id)


def check_ticket_already_has_email(ticket: Ticket, contact_email: str):
  return any(email == contact_email for email in ticket.get_contact_emails())


def update_ticket_contact_emails(session: SessionMaker, ticket: Ticket, contact_email: str):
  new_contact_email = TicketContactEmail(contact_email)
  ticket.add_contact_emails([new_contact_email])
  session.commit()

  return ticket.get_contact_emails()


def send_warning_email(to: List[str], contact_email: str, event_name: str):
  return send_email({
      'to': to,
      'subject': "Uma pessoa cadastrou o mesmo ingresso que você 😥",
      'html': f"""<div>
        <img
          src="https://firebasestorage.googleapis.com/v0/b/verificaticket.appspot.com/o/logo%20text%20-%20blue.svg?alt=media&token=ef252dd8-25ae-4db1-9529-e1ac5d005e7b&_gl=1*10p4xqx*_ga*MTA5NjE5NjU1MC4xNjk2NDcyMTkx*_ga_CW55HF8NVT*MTY5ODgwNzk5Ny4yNi4xLjE2OTg4MTAwMzAuNDAuMC4w"
          alt="VerificaTicket Logo"
          width="184"
          height="24"
        />
        <br />
        <h1>Evento: {event_name}</h1>
        <p>Olá, infelizmente alguém cadastrou o mesmo ingresso que você.</p>
        <p>
          O email de contato dessa pessoa é: <a href=mailto:{contact_email}>{contact_email}</a>{' '}
        </p>
        <p>Esperamos que consigam resolver o problema, boa sorte! 🤞</p>
        <br />
        <p>Atenciosamente, VerificaTicket.</p>
      </div>"""
  })


@app.delete(f"{base_url}/<int:id>", tags=[ticket_tag], responses={200: TicketSchema, 404: ResponseException})
def delete_ticket(path: TicketDeleteSchema):
  """Deleta um ingresso com base no ID fornecido."""
  session = Session()
  ticket: Union[Ticket, None] = session.query(Ticket).get(path.id)

  if not ticket:
    return {'message': 'Ingresso não encontrado'}, 404

  session.delete(ticket)
  session.commit()

  return ticket.to_json(), 200
