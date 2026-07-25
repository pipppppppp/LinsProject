from flask import Blueprint, request, render_template, session, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt

from ..models.customer import CustomerModels
from ...utilities.responseHelpers import bad_request

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
@jwt_required()
def index():
    try:
        return render_template(
            title='Customer - POS Bengkel',
            template_name_or_list='customer.html',
            active_menu="customer",
        )
    except Exception as e:
        return bad_request(str(e))
# CUSTOMER PAGE ============================================================ End


# ADD CUSTOMER DATA ============================================================ Begin
# [POST] https://127.0.0.1:5000/customer/add
@customer.post('/add')
@jwt_required()
def create_customer():
    try:
        role = str(get_jwt()["role"])
        if role != "1":
              return authorization_error(
            "Hanya Owner yang dapat menambah pelanggan."
        )
        ws_id = str(get_jwt()["ws_id"])

        body = request.json

        response = CustomerModels.create_customer(role, ws_id, body)

        return response

    except Exception as e:
        return bad_request(str(e))
# ADD CUSTOMER DATA ============================================================ End

# GET CUSTOMER DATA ============================================================ Begin
# GET https://127.0.0.1:5000/customer/view
@customer.get('/view')
@jwt_required()
def read_customer():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        response = CustomerModels.read_customer(role, ws_id)

        return response

    except Exception as e:
        return bad_request(str(e))
# GET CUSTOMER DATA ============================================================ End


# UPDATE CUSTOMER DATA ============================================================ Begin
# [PUT] https://127.0.0.1:5000/customer/edit/<id>
@customer.put('/edit/<int:id>')
@jwt_required()
def update_customer(id):
    try:
        role = str(get_jwt()["role"])
        if role != "1":
              return authorization_error(
            "Hanya Owner yang dapat mengubah data pelanggan."
        )
        ws_id = str(get_jwt()["ws_id"])

        body = request.json

        response = CustomerModels.update_customer(role, ws_id, id, body)

        return response

    except Exception as e:
        return bad_request(str(e))
# UPDATE CUSTOMER DATA ============================================================ End


# DELETE CUSTOMER DATA ============================================================ Begin
# [DELETE] https://127.0.0.1:5000/customer/delete/<id>
@customer.delete('/delete/<int:id>')
@jwt_required()
def delete_customer(id):
    try:
        role = str(get_jwt()["role"])
        if role != "1":
              return authorization_error(
            "Hanya Owner yang dapat menghapus pelanggan."
        )
        ws_id = str(get_jwt()["ws_id"])

        response = CustomerModels.delete_customer(role, ws_id, id)

        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE CUSTOMER DATA ============================================================ End