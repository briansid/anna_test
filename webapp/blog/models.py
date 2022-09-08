from .. import db
from sqlalchemy.inspection import inspect


class Serializer(object):

    @staticmethod
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class Post(db.Model, Serializer):
    id = db.Column(db.Integer(), primary_key=True)
    olx_id = db.Column(db.Integer(), nullable=False, unique=True, index=True)
    title = db.Column(db.String(255))
    price = db.Column(db.Integer())
    photo = db.Column(db.String(255))
    seller = db.Column(db.String(255))

    def __init__(self, title=""):
        self.title = title

    def __repr__(self):
        return "<Post '{}'>".format(self.title)

    # TODO use Marshmellow
    def serialize(self, role):
        d = Serializer.serialize(self)
        if role == 'default' or role == 'poster':
            del d['seller']
        return d
