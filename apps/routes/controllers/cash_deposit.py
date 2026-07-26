from flask import Blueprint, request, render_template
from flask_jwt_extended import jwt_required, get_jwt

from ..models.cash_deposit import CashDepositModels
from ...utilities.responseHelpers import bad_request


# BLUEPRINT ================================================== Begin
cash_deposit = Blueprint(
    name="cash_deposit",
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix="/cash-deposit",
)
# BLUEPRINT ================================================== End


# CASH DEPOSIT PAGE ============================================================ Begin
# [GET] https://127.0.0.1:5000/cash-deposit/
@cash_deposit.get("/")
@jwt_required()
def index():
    try:
        return render_template(
            title="Setor Kas - POS Bengkel",
            template_name_or_list="cash_deposit.html",
            active_menu="cash_deposit",
        )

    except Exception as e:
        return bad_request(str(e))
# CASH DEPOSIT PAGE ============================================================ End


# ADD CASH DEPOSIT ============================================================ Begin
# [POST] https://127.0.0.1:5000/cash-deposit/add
@cash_deposit.post("/add")
@jwt_required()
def create_cash_deposit():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])
        user_id = str(get_jwt()["id"])

        body = request.json

        response = CashDepositModels.create_cash_deposit(
            role,
            ws_id,
            user_id,
            body
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# ADD CASH DEPOSIT ============================================================ End


# GET CASH DEPOSIT ============================================================ Begin
# [GET] https://127.0.0.1:5000/cash-deposit/view
@cash_deposit.get("/view")
@jwt_required()
def read_cash_deposit():
    try:
        print("===== JWT =====")
        print(get_jwt())
        
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])
        user_id = str(get_jwt()["id"])

        date = request.args.get("date", "")
        status = request.args.get("status", "")

        response = CashDepositModels.read_cash_deposit(
            role,
            ws_id,
            user_id,
            date,
            status,
        )
        return response

    except Exception as e:
        return bad_request(str(e))
# GET CASH DEPOSIT ============================================================ End

# CASH DEPOSIT VERIFICATION PAGE ============================================== Begin
# [GET] https://127.0.0.1:5000/cash-deposit/verification
@cash_deposit.get("/verification")
@jwt_required()
def verification():
    try:
        return render_template(
            title="Verifikasi Setor Kas - POS Bengkel",
            template_name_or_list="cash_deposit_verify.html",
            active_menu="cash_deposit_verify",
        )

    except Exception as e:
        return bad_request(str(e))
# CASH DEPOSIT VERIFICATION PAGE ============================================== End

# VERIFY CASH DEPOSIT ============================================================ Begin
# [PUT] https://127.0.0.1:5000/cash-deposit/verify
@cash_deposit.put("/verify")
@jwt_required()
def verify_cash_deposit():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])
        user_id = str(get_jwt()["id"])

        body = request.json

        response = CashDepositModels.verify_cash_deposit(
            role,
            ws_id,
            user_id,
            body
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# VERIFY CASH DEPOSIT ============================================================ End

# DELETE CASH DEPOSIT ============================================================ Begin
# [DELETE] https://127.0.0.1:5000/cash-deposit/delete/<id>
@cash_deposit.delete("/delete/<int:id>")
@jwt_required()
def delete_cash_deposit(id):
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        response = CashDepositModels.delete_cash_deposit(
            role,
            ws_id,
            id
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE CASH DEPOSIT ============================================================ End
