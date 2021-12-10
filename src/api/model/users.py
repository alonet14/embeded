from src.api.utils.database import db, ma
from marshmallow import fields, post_load


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idn = db.Column(db.Integer)
    name = db.Column(db.String(100))
    wallet = db.Column(db.Integer)

    def __init__(self, idn, name, wallet):
        self.idn = idn
        self.name = name
        self.wallet = wallet

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class UserSchema(ma.Schema):
    class Meta(ma.Schema.Meta):
        model = User
        load_instance = True


    id = fields.Number(dump_only=True)
    idn = fields.Number(dump_only=False, required=True)
    name = fields.String(required=True)
    wallet = fields.Number(required=True, default=0)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)