import datetime

from log_server import db


def timestamptz_now():
    return datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()


class Message(db.Model):
    __tablename__ = 'messages'

    time = db.Column(db.String(length=32), primary_key=True,
                     default=timestamptz_now)
    message = db.Column(db.Text, nullable=False)

    def get_local_time(self):
        if self.time is not None:
            parsed_time = datetime.datetime.fromisoformat(self.time)
            result = parsed_time.astimezone()
        else:
            result = None
        return result
