from sqlalchemy.orm import Session as SessionMaker
from datetime import datetime, timedelta

from models import Event, EventDate


def seed_events(session: SessionMaker):
  def make_event_dates():
    return [EventDate(date=(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')) for i in range(3)]

  events = [
      Event(
          name='Lollapalooza',
          image='https://cdn.getcrowder.com/images/6d5f34c0-fe1c-4ccf-b598-d60bbbf3ed77-lollapaloozageral1920x720.jpg',
          platform_id=1
      ),
      Event(
          name='Jessie J',
          image='https://cooltours.s3.sa-east-1.amazonaws.com/images/preview/fa970b6c63ef29f56ca465c082a372aab90227474c3f846db1661a3c38d25f1f.jpg',
          platform_id=2
      ),
      Event(
          name='FESTIVAL DE VERÃO DE SALVADOR 2024',
          image='https://assets.bileto.sympla.com.br/eventmanager/production/k09au16q1kvkn2f1u0nqg4aj5dum33di5tj232gduqfc2futs5jckgg6dsms2m73mn0n80mi0meb2gd8e3mvj53cqcoh0vr2tk2gm9.webp',
          platform_id=3
      ),
      Event(
          name='RBD',
          image='https://www.eventim.com.br/obj/media/BR-eventim/teaser/evo/artwork/2020/r_artworkbd.png',
          platform_id=4
      ),
  ]

  for event in events:
    event.add_dates(make_event_dates())

  session.add_all(events)
  session.commit()
