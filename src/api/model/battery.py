from src.api.utils.database import db, ma
from marshmallow import fields, post_load
class Battery(db.Model):
    __tablename__ = 'battery'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    idUser = db.Column(db.Integer, db.ForeignKey('user.id'))
    idStation = db.Column(db.Integer, db.ForeignKey('station.id'))
    rfidCode = db.Column(db.String)

    def __init__(self, idUser, idStation, rfidCode):
        self.idUser = idUser
        self.idStation = idStation
        self.rfidCode = rfidCode

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class BatterySchema(ma.Schema):
    class Meta(ma.Schema.Meta):
        model = Battery
        load_instance = True

    id = fields.Number(dump_only=True)
    idUser = fields.Number(required=True)
    idStation = fields.Number(required=True)
    rfidCode = fields.String(required=True)

    @post_load
    def make_battery(self, data, **kwargs):
        return Battery(**data)

    # def __init__(self, **kwargs):
    #     self.id

