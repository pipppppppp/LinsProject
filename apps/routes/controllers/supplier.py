from flask import Blueprint, request, render_template
from flask_jwt_extended import jwt_required, get_jwt

from ..models.supplier import SupplierModels
from ...utilities.responseHelpers import bad_request


# BLUEPRINT ================================================== Begin
supplier = Blueprint(
    name='supplier',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/supplier',
)
# BLUEPRINT ================================================== End


# SUPPLIER PAGE ============================================================ Begin
# [GET] https://127.0.0.1:5000/supplier/
@supplier.get('/')
@jwt_required()
def index():
    try:
        return render_template(
            title='Supplier - POS Bengkel',
            template_name_or_list='supplier.html',
            active_menu="supplier",
        )
    except Exception as e:
        return bad_request(str(e))
# SUPPLIER PAGE ============================================================ End


# ADD SUPPLIER DATA ============================================================ Begin
# [POST] https://127.0.0.1:5000/supplier/add
@supplier.post('/add')
@jwt_required()
def create_supplier():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        body = request.json

        response = SupplierModels.create_supplier(
            role,
            ws_id,
            body
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# ADD SUPPLIER DATA ============================================================ End


# GET SUPPLIER DATA ============================================================ Begin
# [GET] https://127.0.0.1:5000/supplier/view
@supplier.get('/view')
@jwt_required()
def read_supplier():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        response = SupplierModels.read_supplier(
            role,
            ws_id
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# GET SUPPLIER DATA ============================================================ End


# UPDATE SUPPLIER DATA ============================================================ Begin
# [PUT] https://127.0.0.1:5000/supplier/edit/<id>
@supplier.put('/edit/<int:id>')
@jwt_required()
def update_supplier(id):
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        body = request.json

        response = SupplierModels.update_supplier(
            role,
            ws_id,
            id,
            body
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# UPDATE SUPPLIER DATA ============================================================ End


# DELETE SUPPLIER DATA ============================================================ Begin
# [DELETE] https://127.0.0.1:5000/supplier/delete/<id>
@supplier.delete('/delete/<int:id>')
@jwt_required()
def delete_supplier(id):
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        response = SupplierModels.delete_supplier(
            role,
            ws_id,
            id
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE SUPPLIER DATA ============================================================ End