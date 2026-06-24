from flask import Blueprint, request, render_template
from flask import session, redirect, url_for

from ... import db
from ...database.db_services import Services

import time

services = Blueprint(
    name='services',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/services',
)

# TAMPIL HALAMAN
@services.get('/')
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

    services_data = Services.query.filter_by(
        is_delete=0
    ).all()

    return render_template(
        template_name_or_list='services.html',
        active_menu="services",
        title='Data Jasa Servis',
        services=services_data
    )


# TAMBAH DATA
@services.post('/add')
def addService():

    body = request.json

    service = Services(
        nama_jasa=body['nama_jasa'],
        biaya_jasa=body['biaya_jasa'],
        keterangan=body['keterangan'],
        created_at=int(time.time()),
        updated_at=int(time.time())
    )

    db.session.add(service)
    db.session.commit()

    return {
        "status": True,
        "message": "Data berhasil disimpan"
    }


# UPDATE
@services.put('/update/<int:id>')
def updateService(id):

    body = request.json

    data = Services.query.get_or_404(id)

    data.nama_jasa = body['nama_jasa']
    data.biaya_jasa = body['biaya_jasa']
    data.keterangan = body['keterangan']
    data.updated_at = int(time.time())

    db.session.commit()

    return {
        "status": True,
        "message": "Data berhasil diupdate"
    }


# DELETE
@services.delete('/delete/<int:id>')
def deleteService(id):
    
    if session.get('role') != 'admin':
            return {
            "status": False,
            "message": "Akses ditolak"
        }, 403

    data = Services.query.get_or_404(id)

    data.is_delete = 1
    data.deleted_at = int(time.time())

    db.session.commit()

    return {
        "status": True,
        "message": "Data berhasil dihapus"
    }