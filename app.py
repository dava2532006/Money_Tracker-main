from flask import Flask, render_template
from flask import request, redirect, url_for
from sqlalchemy import or_
from models.prioritas import Prioritas
from models.transaksi import Transaksi
import os

from extensions import db


app = Flask(__name__)

# Konfigurasi SQLite
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'database1.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi objek database
db.init_app(app)

@app.route('/')
def dashboard():
    saldo = Transaksi.get_saldo()
    pemasukan = Transaksi.total_pemasukan()
    pengeluaran = Transaksi.total_pengeluaran()
    riwayat = Transaksi.semua_transaksi()
    return render_template('dashboard.html', saldo=saldo, pemasukan=pemasukan, pengeluaran=pengeluaran, riwayat=riwayat)

@app.route('/tambah', methods=['POST'])
def tambah_transaksi():
    tipe = request.form['tipe']
    kategori = request.form['kategori']
    jumlah = int(request.form['jumlah'])
    keterangan = request.form['keterangan']
    transaksi = Transaksi(tipe=tipe, kategori=kategori, jumlah=jumlah, keterangan=keterangan)
    db.session.add(transaksi)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/riwayat')
def riwayat_transaksi():
    data = Transaksi.query.order_by(Transaksi.tanggal.desc()).all()
    return render_template('riwayat.html', data=data)

@app.route('/cari', methods=['GET'])
def cari_transaksi():
    keyword = request.args.get('q', '').lower()
    if keyword:
        hasil = Transaksi.query.filter(
            db.or_(
                Transaksi.kategori.ilike(f"%{keyword}%"),
                Transaksi.keterangan.ilike(f"%{keyword}%")
            )
        ).order_by(Transaksi.tanggal.desc()).all()
    else:
        hasil = []
    return render_template('pencarian.html', hasil=hasil, keyword=keyword)

@app.route('/kategori')
def detail_kategori():
    from sqlalchemy import func
    hasil = db.session.query(
        Transaksi.kategori,
        func.sum(Transaksi.jumlah)
    ).filter(
        Transaksi.tipe == 'keluar'
    ).group_by(
        Transaksi.kategori
    ).order_by(
        func.sum(Transaksi.jumlah).desc()
    ).all()
    return render_template('kategori.html', hasil=hasil)







if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    