from extensions import db

class Prioritas(db.Model):
    __tablename__ = 'prioritas'

    id = db.Column(db.Integer, primary_key=True)
    kategori = db.Column(db.String(100), nullable=False)
    persentase = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Prioritas {self.kategori} - {self.persentase}%>"