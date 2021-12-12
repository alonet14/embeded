from src.api.utils.database import db


class Battery(db.Model):
    __tablename__ = 'battery'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUser=db.Column(db.Integer)
    idStation=db.Column(db.Integer)

    def __init__(self, **kwargs):
        self.id
