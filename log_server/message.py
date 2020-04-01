from flask_sqlalchemy import event
from sqlalchemy import func
import datetime
import os

from log_server import db

LOGGER_MAX_MESSAGES = os.environ.get('LOGGER_MAX_MESSAGES')
try:
    LOGGER_MAX_MESSAGES = int(float(LOGGER_MAX_MESSAGES))
    if LOGGER_MAX_MESSAGES <= 0:
        LOGGER_MAX_MESSAGES = None
except:
    LOGGER_MAX_MESSAGES = None
print('LOGGER_MAX_MESSAGES={}'.format(LOGGER_MAX_MESSAGES))


def timestamptz_now():
    return datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()


class Message(db.Model):
    __tablename__ = 'messages'

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.String(length=32), default=timestamptz_now)
    message = db.Column(db.Text, nullable=False)

    def get_local_time(self):
        if self.time is not None:
            parsed_time = datetime.datetime.fromisoformat(self.time)
            result = parsed_time.astimezone()
        else:
            result = None
        return result


@event.listens_for(Message, 'before_insert')
def do_stuff(mapper, connect, target):
    if LOGGER_MAX_MESSAGES:
        table_count = db.session.query(Message).count()
        if table_count >= LOGGER_MAX_MESSAGES:
            min_index = db.session.query(func.min(Message.index)).first()[0]
            Message.query.filter_by(index=min_index).delete()
