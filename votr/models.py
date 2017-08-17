import uuid

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                onupdate=db.func.current_timestamp())

class Users(Base):
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))


class Topics(Base):
    title = db.Column(db.String(500))
    status = db.Column(db.Boolean)

    def __repr__(self):
        return self.title

    def to_json(self):
        poll_data = {
            'title': self.title,
            'options': 
                [{'name': option.option.name,'vote_count':option.vote_count}
                    for option in self.options.all()],
            'status': self.status
        }
        return poll_data

class Polls(Base):
    # Set polls table columns
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'))
    vote_count = db.Column(db.Integer, default=0)
    # Declare relationship
    topic = db.relationship('Topics', foreign_keys=[topic_id], backref=db.backref('options', lazy='dynamic'))
    option = db.relationship('Options', foreign_keys=[option_id])

    def __repr__(self):
        return self.option.name


class Options(Base):
    name = db.Column(db.String(200), unique=True)

    def __repr__(self):
        return self.name

    def to_json(self):
        return {'id': uuid.uuid4(), 'name': self.name}



