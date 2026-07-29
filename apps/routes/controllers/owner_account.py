from flask import Blueprint, request, render_template
from flask_jwt_extended import jwt_required, get_jwt

from ..models.owner_account import OwnerAccountModels
from ...utilities.responseHelpers import authorization_error, bad_request


# BLUEPRINT ============================================================ Begin
owner_account = Blueprint(
    name="owner_account",
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix="/owner-account"
)
# BLUEPRINT ============================================================ End


# OWNER ACCOUNT PAGE ============================================================ Begin
# [GET] https://127.0.0.1:5000/owner-account/
@owner_account.get("/")
@jwt_required()
def index():
    try:
        # JWT Access Data ---------------------------------------- Start
        role = str(get_jwt()["role"])
        # JWT Access Data ---------------------------------------- Finish

        # Access Validation ---------------------------------------- Start
        if role != "1":
            return authorization_error()
        # Access Validation ---------------------------------------- Finish

        # Return Page ========================================
        return render_template(
            title="Pengaturan Akun - POS Bengkel",
            template_name_or_list="owner_account.html",
            active_menu="owner_account"
        )

    except Exception as e:
        return bad_request(str(e))
# OWNER ACCOUNT PAGE ============================================================ End


# GET OWNER ACCOUNT ============================================================ Begin
# [GET] https://127.0.0.1:5000/owner-account/view
@owner_account.get("/view")
@jwt_required()
def read_owner_account():
    try:
        # JWT Access Data ---------------------------------------- Start
        user_id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])
        # JWT Access Data ---------------------------------------- Finish

        # Process Data ---------------------------------------- Start
        response = OwnerAccountModels.read_owner_account(
            role,
            user_id
        )
        # Process Data ---------------------------------------- Finish

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# GET OWNER ACCOUNT ============================================================ End


# UPDATE OWNER ACCOUNT ============================================================ Begin
# [PUT] https://127.0.0.1:5000/owner-account/edit
@owner_account.put("/edit")
@jwt_required()
def update_owner_account():
    try:
        # JWT Access Data ---------------------------------------- Start
        user_id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])
        # JWT Access Data ---------------------------------------- Finish

        # Request Data ---------------------------------------- Start
        body = request.json
        # Request Data ---------------------------------------- Finish

        # Process Data ---------------------------------------- Start
        response = OwnerAccountModels.update_owner_account(
            role,
            user_id,
            body
        )
        # Process Data ---------------------------------------- Finish

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# UPDATE OWNER ACCOUNT ============================================================ End


# CHANGE OWNER PASSWORD ============================================================ Begin
# [PUT] https://127.0.0.1:5000/owner-account/change-password
@owner_account.put("/change-password")
@jwt_required()
def change_owner_password():
    try:
        # JWT Access Data ---------------------------------------- Start
        user_id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])
        # JWT Access Data ---------------------------------------- Finish

        # Request Data ---------------------------------------- Start
        body = request.json
        # Request Data ---------------------------------------- Finish

        # Process Data ---------------------------------------- Start
        response = OwnerAccountModels.change_owner_password(
            role,
            user_id,
            body
        )
        # Process Data ---------------------------------------- Finish

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# CHANGE OWNER PASSWORD ============================================================ End