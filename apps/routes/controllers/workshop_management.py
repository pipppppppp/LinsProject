from flask import Blueprint, request, render_template
from flask_jwt_extended import jwt_required, get_jwt

from apps.utilities.responseHelpers import bad_request

from ..models.workshop_management import WorkshopManagementModels


# BLUEPRINT ============================================================ Begin
workshop_management = Blueprint(
    name="workshop_management",
    import_name=__name__,
    template_folder="../../templates/pages/adminPages",
    url_prefix="/workshop-management",
)
# BLUEPRINT ============================================================ End


# WORKSHOP MANAGEMENT PAGE ============================================================ Begin
# GET http://127.0.0.1:5000/workshop-management/
@workshop_management.get("/")
@jwt_required()
def workshop_management_page():
    try:
        return render_template(
            template_name_or_list="workshop_management.html",
            title="Manajemen Bengkel - POS Bengkel",
            active_menu="workshop_management",
        )

    except Exception as e:
        return bad_request(str(e))
# WORKSHOP MANAGEMENT PAGE ============================================================ End


# VIEW WORKSHOP ============================================================ Begin
# GET http://127.0.0.1:5000/workshop-management/view
@workshop_management.get("/view")
@jwt_required()
def read_workshop():
    try:
        # JWT Access Data ========================================
        role = str(get_jwt()["role"])

        # Request Parameters ========================================
        status = request.args.get(
            "status",
            "all"
        )

        # Request Process ========================================
        response = WorkshopManagementModels.read_workshop(
            role,
            status
        )

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# VIEW WORKSHOP ============================================================ End


# DETAIL WORKSHOP ============================================================ Begin
# GET http://127.0.0.1:5000/workshop-management/detail/1
@workshop_management.get("/detail/<int:workshop_id>")
@jwt_required()
def detail_workshop(workshop_id):
    try:
        # JWT Access Data ========================================
        role = str(get_jwt()["role"])

        # Request Process ========================================
        response = WorkshopManagementModels.detail_workshop(
            role,
            workshop_id
        )

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# DETAIL WORKSHOP ============================================================ End


# ACTIVATE WORKSHOP ============================================================ Begin
# PUT http://127.0.0.1:5000/workshop-management/activate
@workshop_management.put("/activate")
@jwt_required()
def activate_workshop():
    try:
        # JWT Access Data ========================================
        role = str(get_jwt()["role"])

        # Request Data ========================================
        body = request.get_json(
            silent=True
        )

        # Request Process ========================================
        response = (
            WorkshopManagementModels
            .activate_workshop(
                role,
                body
            )
        )

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# ACTIVATE WORKSHOP ============================================================ End

# DEACTIVATE WORKSHOP ============================================================ Begin
# PUT http://127.0.0.1:5000/workshop-management/deactivate
@workshop_management.put("/deactivate")
@jwt_required()
def deactivate_workshop():
    try:
        # JWT Access Data ========================================
        role = str(get_jwt()["role"])

        # Request Data ========================================
        body = request.get_json(
            silent=True
        )

        # Request Process ========================================
        response = (
            WorkshopManagementModels
            .deactivate_workshop(
                role,
                body
            )
        )

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# DEACTIVATE WORKSHOP ============================================================ End


# DELETE WORKSHOP ============================================================ Begin
# DELETE http://127.0.0.1:5000/workshop-management/delete
@workshop_management.delete("/delete")
@jwt_required()
def delete_workshop():
    try:
        # JWT Access Data ========================================
        role = str(get_jwt()["role"])

        # Request Data ========================================
        body = request.get_json(
            silent=True
        )

        # Request Process ========================================
        response = (
            WorkshopManagementModels
            .delete_workshop(
                role,
                body
            )
        )

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE WORKSHOP ============================================================ End