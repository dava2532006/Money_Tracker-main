from flask_sqlalchemy import SQLAlchemy
from extensions import db
from datetime import datetime

class Transaksi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipe = db.Column(db.String(10))  # 'masuk' atau 'keluar'
    kategori = db.Column(db.String(50))
    jumlah = db.Column(db.Integer)
    keterangan = db.Column(db.String(100))
    tanggal = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def total_pemasukan():
        result = db.session.query(db.func.sum(Transaksi.jumlah)).filter_by(tipe='masuk').scalar()
        return result or 0

    @staticmethod
    def total_pengeluaran():
        result = db.session.query(db.func.sum(Transaksi.jumlah)).filter_by(tipe='keluar').scalar()
        return result or 0

    @staticmethod
    def get_saldo():
        pemasukan = db.session.query(db.func.sum(Transaksi.jumlah)).filter_by(tipe='pemasukan').scalar() or 0
        pengeluaran = db.session.query(db.func.sum(Transaksi.jumlah)).filter_by(tipe='pengeluaran').scalar() or 0
        return pemasukan - pengeluaran

    @staticmethod
    def semua_transaksi():
        return Transaksi.query.order_by(Transaksi.tanggal.desc()).all()
    

