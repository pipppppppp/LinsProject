from flask import Blueprint, request, render_template
from flask import current_app as app

from ... import db
from ...database.db_customer import Customers

import time

# BLUEPRINT ================================================== Begin
customer = Blueprint(
    name='customer',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/customer',
)
# BLUEPRINT ================================================== End


# CUSTOMER PAGE ============================================================ Begin
# [GET] https://127.0.0.1:5000/customer/
@customer.get('/')
def index():

    customers = Customers.query.filter_by(
        is_delete=0
    ).all()

    return render_template(
        template_name_or_list='customer.html',
        title='Data Pelanggan',
        customers=customers
    )
# CUSTOMER PAGE ============================================================ End


# ADD CUSTOMER DATA ============================================================ Begin
# [POST] https://127.0.0.1:5000/customer/add
@customer.post('/add')
def addCustomer():

    body = request.json

    customer = Customers(
        nama=body['nama'],
        alamat=body['alamat'],
        telepon=body['telepon'],
        created_at=int(time.time()),
        updated_at=int(time.time())
    )

    db.session.add(customer)
    db.session.commit()

    return {
        "status": True,
        "message": "Data berhasil disimpan"
    }
# ADD CUSTOMER DATA ============================================================ End


# UPDATE CUSTOMER DATA ============================================================ Begin
# [PUT] https://127.0.0.1:5000/customer/update/<id>
@customer.put('/update/<int:id>')
def updateCustomer(id):
    try:
        body = request.json

        data = Customers.query.get_or_404(id)

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
# UPDATE CUSTOMER DATA ============================================================ End


# DELETE CUSTOMER DATA ============================================================ Begin
# [DELETE] https://127.0.0.1:5000/customer/delete/<id>
@customer.delete('/delete/<int:id>')
def deleteCustomer(id):

    data = Customers.query.get_or_404(id)

    data.is_delete = 1
    data.deleted_at = int(time.time())

    db.session.commit()

    return {
        "status": True,
        "message": "Data berhasil dihapus"
    }
# DELETE CUSTOMER DATA ============================================================ End
