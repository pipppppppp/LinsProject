from flask import Blueprint, request, render_template
from flask_jwt_extended import jwt_required, get_jwt

from ..models.workshop import WorkshopModels
from ...utilities.responseHelpers import bad_request

# BLUEPRINT ============================================================ Begin
workshop = Blueprint(
    name="workshop",
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix="/workshop"
)
# BLUEPRINT ============================================================ End


# WORKSHOP PAGE ============================================================ Begin
# [GET] https://127.0.0.1:5000/workshop/
@workshop.get("/")
@jwt_required()
def index():
    try:
        return render_template(
            title="Workshop Profile - POS Bengkel",
            template_name_or_list="workshop_profile.html",
            active_menu="workshop"
        )

    except Exception as e:
        return bad_request(str(e))
# WORKSHOP PAGE ============================================================ End


# ADD WORKSHOP ============================================================ Begin
# [POST] https://127.0.0.1:5000/workshop/add
@workshop.post("/add")
@jwt_required()
def create_workshop():
    try:
        user_id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        body = request.json

        response = WorkshopModels.create_workshop(
            user_id,
            role,
            body
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# ADD WORKSHOP ============================================================ End


# GET WORKSHOP ============================================================ Begin
# [GET] https://127.0.0.1:5000/workshop/view
@workshop.get("/view")
@jwt_required()
def read_workshop():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        response = WorkshopModels.read_workshop(
            role,
            ws_id
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# GET WORKSHOP ============================================================ End


# UPDATE WORKSHOP ============================================================ Begin
# [PUT] https://127.0.0.1:5000/workshop/edit
@workshop.put("/edit")
@jwt_required()
def update_workshop():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        datas = request.form

        logo = request.files.get("logo")

        response = WorkshopModels.update_workshop(
            role,
            ws_id,
            datas,
            logo
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# UPDATE WORKSHOP ============================================================ End