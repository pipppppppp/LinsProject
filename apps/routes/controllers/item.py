from flask import Blueprint, request, render_template, session, redirect, url_for
from flask import current_app as app

from ... import db
from ...database.db_items import Items
from ...database.db_categories import Categories

import time

item = Blueprint(
    name='item',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/item',
)

# TAMPIL HALAMAN
@item.get('/')
def index():

    if 'user_id' not in session:
        return redirect(
            url_for('auth.signin_page')
        )
    # Protrksi role
    if session.get('role') != 'admin':
        return redirect(
            url_for('dashboard.index')
        )

    items = Items.query.filter_by(
        is_delete=0
    ).all()
    for item in items:
        item.category = Categories.query.get(
            item.category_id
        )
    # Ambil data category
    categories = Categories.query.filter_by(
        is_delete=0
    ).all()

    return render_template(
        template_name_or_list='item.html',
        title='Data Barang',
        items=items,
        categories=categories,
        active_menu="item"
    )


# TAMBAH DATA
@item.post('/add')
def addItem():

    body = request.json

    item_data = Items(
        category_id=body['category_id'],
        nama_barang=body['nama_barang'],
        stok=body['stok'],
        harga_beli=body['harga_beli'],
        harga_jual=body['harga_jual'],
        created_at=int(time.time()),
        updated_at=int(time.time())
    )

    db.session.add(item_data)
    db.session.commit()

    return {
        "status": True,
        "message": "Data berhasil disimpan"
    }

# UPDATE
@item.put('/update/<int:id>')
def updateItem(id):
    try:
        body = request.json

        data = Items.query.get_or_404(id)

        data.category_id = body['category_id']
        data.nama_barang = body['nama_barang']
        data.stok = body['stok']
        data.harga_beli = body['harga_beli']
        data.harga_jual = body['harga_jual']
        data.updated_at = int(time.time())

        db.session.commit()

        return {
            "status": True,
            "message": "Data berhasil diupdate"
        }

    except Exception as e:
        return {
            "status": False,
            "message": str(e)
        }, 500


# DELETE
@item.delete('/delete/<int:id>')
def deleteItem(id):

    if session.get('role') != 'admin':
            return {
            "status": False,
            "message": "Akses ditolak"
        }, 403

    data = Items.query.get_or_404(id)

    data.is_delete = 1
    data.deleted_at = int(time.time())

    db.session.commit()

    return {
        "status": True,
        "message": "Data berhasil dihapus"
    }