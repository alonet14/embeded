from src.api.utils.database import db, ma
class Station(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    