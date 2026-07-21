from flask import Blueprint, request, render_template
from flask_jwt_extended import jwt_required, get_jwt

from ..models.cashier_management import CashierManagementModels
from ...utilities.responseHelpers import bad_request


# BLUEPRINT ============================================================ Begin
cashier_management = Blueprint(
    name='cashier_management',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/cashier-management',
)
# BLUEPRINT ============================================================ End


# CASHIER MANAGEMENT PAGE ============================================================ Begin
# [GET] https://127.0.0.1:5000/cashier-management/
@cashier_management.get('/')
@jwt_required()
def index():
    try:
        return render_template(
            title='Cashier Management - POS Bengkel',
            template_name_or_list='cashier_management.html',
            active_menu="cashier_management",
        )

    except Exception as e:
        return bad_request(str(e))
# CASHIER MANAGEMENT PAGE ============================================================ End


# ADD CASHIER ============================================================ Begin
# [POST] https://127.0.0.1:5000/cashier-management/add
@cashier_management.post('/add')
@jwt_required()
def create_cashier():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        body = request.json

        response = CashierManagementModels.create_cashier(
            role,
            ws_id,
            body
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# ADD CASHIER ============================================================ End


# GET CASHIER ============================================================ Begin
# [GET] https://127.0.0.1:5000/cashier-management/view
@cashier_management.get('/view')
@jwt_required()
def read_cashier():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        response = CashierManagementModels.read_cashier(
            role,
            ws_id
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# GET CASHIER ============================================================ End


# UPDATE CASHIER ============================================================ Begin
# [PUT] https://127.0.0.1:5000/cashier-management/edit/<id>
@cashier_management.put('/edit/<int:id>')
@jwt_required()
def update_cashier(id):
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        body = request.json

        response = CashierManagementModels.update_cashier(
            role,
            ws_id,
            id,
            body
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# UPDATE CASHIER ============================================================ End


# DELETE CASHIER ============================================================ Begin
# [DELETE] https://127.0.0.1:5000/cashier-management/delete/<id>
@cashier_management.delete('/delete/<int:id>')
@jwt_required()
def delete_cashier(id):
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        response = CashierManagementModels.delete_cashier(
            role,
            ws_id,
            id
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE CASHIER ============================================================ End