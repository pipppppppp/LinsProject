from flask import Blueprint, request, render_template
from flask_jwt_extended import jwt_required, get_jwt

from ..models.services import ServiceModels
from ...utilities.responseHelpers import bad_request


# BLUEPRINT ============================================================ Begin
service = Blueprint(
    name="service",
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix="/service",
)
# BLUEPRINT ============================================================ End


# SERVICE PAGE ============================================================ Begin
# [GET] https://127.0.0.1:5000/service/
@service.get("/")
@jwt_required()
def index():
    try:
        return render_template(
            title="Jasa Servis - POS Bengkel",
            template_name_or_list="service.html",
            active_menu="service",
        )

    except Exception as e:
        return bad_request(str(e))
# SERVICE PAGE ============================================================ End


# ADD SERVICE DATA ============================================================ Begin
# [POST] https://127.0.0.1:5000/service/add
@service.post("/add")
@jwt_required()
def create_service():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        body = request.json

        response = ServiceModels.create_service(
            role,
            ws_id,
            body
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# ADD SERVICE DATA ============================================================ End


# GET SERVICE DATA ============================================================ Begin
# [GET] https://127.0.0.1:5000/service/view
@service.get("/view")
@jwt_required()
def read_service():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        response = ServiceModels.read_service(
            role,
            ws_id
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# GET SERVICE DATA ============================================================ End


# UPDATE SERVICE DATA ============================================================ Begin
# [PUT] https://127.0.0.1:5000/service/edit/<id>
@service.put("/edit/<int:id>")
@jwt_required()
def update_service(id):
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        body = request.json

        response = ServiceModels.update_service(
            role,
            ws_id,
            id,
            body
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# UPDATE SERVICE DATA ============================================================ End


# DELETE SERVICE DATA ============================================================ Begin
# [DELETE] https://127.0.0.1:5000/service/delete/<id>
@service.delete("/delete/<int:id>")
@jwt_required()
def delete_service(id):
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        response = ServiceModels.delete_service(
            role,
            ws_id,
            id
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE SERVICE DATA ============================================================ End