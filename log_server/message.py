import datetime

from log_server import db


def timestamptz_now():
    return datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()


class Message(db.Model):
    time = db.Column(db.String(length=32), primary_key=True,
                     default=timestamptz_now)
    message = db.Column(db.Text, nullable=False)