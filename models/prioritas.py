from app import db

class Prioritas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kategori = db.Column(db.String(100), nullable=False)
    persentase = db.Column(db.Integer, nullable=False)
