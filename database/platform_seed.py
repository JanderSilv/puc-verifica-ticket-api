from sqlalchemy.orm import Session as SessionMaker

from models import Platform


def seed_platforms(session: SessionMaker):
  platforms = [
      Platform(
          name='Ticketmaster',
          image='https://cdn.freebiesupply.com/logos/thumbs/2x/ticketmaster-5-logo.png'
      ),
      Platform(
          name='Tickets for fun',
          image='https://cooltours.s3.sa-east-1.amazonaws.com/images/preview/7097181fdfcf056d2827081f02b40ac86fb39d16.png'
      ),
      Platform(
          name='Sympla',
          image='https://logodownload.org/wp-content/uploads/2018/10/sympla-logo.png'
      ),
      Platform(
          name='Eventim',
          image='https://logodownload.org/wp-content/uploads/2022/04/eventim-logo.png'
      ),
  ]

  session.add_all(platforms)
  session.commit()
