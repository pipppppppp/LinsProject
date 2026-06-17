from flask import Blueprint, request, render_template, session, redirect, url_for
from flask import current_app as app

from ... import db
from ...database.db_suppliers import Suppliers

import time

supplier = Blueprint(
    name='supplier',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/supplier',
)

# TAMPIL HALAMAN
@supplier.get('/')
def index():

    if 'user_id' not in session:
        return redirect(
            url_for('auth.signin_page')
        )

    suppliers = Suppliers.query.filter_by(
        is_delete=0
    ).all()

    return render_template(
        template_name_or_list='supplier.html',
        active_menu="supplier",
        title='Data Supplier',
        suppliers=suppliers
    )


# TAMBAH DATA
@supplier.post('/add')
def addSupplier():

    body = request.json

    supplier = Suppliers(
        nama=body['nama'],
        alamat=body['alamat'],
        telepon=body['telepon'],
        created_at=int(time.time()),
        updated_at=int(time.time())
    )

    db.session.add(supplier)
    db.session.commit()

    return {
        "status": True,
        "message": "Data berhasil disimpan"
    }

# UPDATE
@supplier.put('/update/<int:id>')
def updateSupplier(id):
    try:
        body = request.json

        data = Suppliers.query.get_or_404(id)

        data.nama = body['nama']
        data.alamat = body['alamat']
        data.telepon = body['telepon']
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
@supplier.delete('/delete/<int:id>')
def deleteSupplier(id):

    data = Suppliers.query.get_or_404(id)

    data.is_delete = 1
    data.deleted_at = int(time.time())

    db.session.commit()

    return {
        "status": True,
        "message": "Data berhasil dihapus"
    }