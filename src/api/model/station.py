from typing_extensions import Required
from src.api.utils.database import db, ma
from marshmallow import fields, post_load

class Station(db.Model):
    __tablename__ = 'station'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String)
    s_batteries = db.relationship('Battery', backref='s_owner')

    def __init__(self, location):
        self.location = location

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class StationSchema(ma.Schema):
    class Meta(ma.Schema.Meta):
        model = Station
        load_instance = True

    id = fields.Number(dump_only=True)
    location = fields.String(required=True)

    @post_load
    def make_station(self, data, **kwargs):
        return Station(**data)
