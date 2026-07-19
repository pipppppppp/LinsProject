from flask import Blueprint, request, render_template
from flask_jwt_extended import jwt_required, get_jwt

from apps.utilities.responseHelpers import bad_request

from ..models.administrator import AdministratorModels


# BLUEPRINT ================================================== Begin
administrator = Blueprint(
    name='administrator',
    import_name=__name__,
    template_folder="../../templates/pages/adminPages",
    url_prefix='/administrator',
)
# BLUEPRINT ================================================== End


# DASHBOARD PAGE ============================================================ Begin
# GET http://127.0.0.1:5000/administrator/
@administrator.get('/dashboard')
@jwt_required()
def dashboard():
    try:
      role = str(get_jwt()["role"])

    #   response = AdministratorModels.dashboard(role)
      
      return render_template(
            title='Administrator - POS Bengkel',
            template_name_or_list='administrator.html',
            active_menu="administrator",
      )

    except Exception as e:
        return bad_request(str(e))
# DASHBOARD PAGE ============================================================ End

# DASHBOARD DATA ============================================================ Begin
# GET http://127.0.0.1:5000/administrator/statistic
@administrator.get('/statistic')
@jwt_required()
def dashboard_statistic():
    try:

        role = str(get_jwt()["role"])

        response = AdministratorModels.dashboard(role)

        return response

    except Exception as e:
        return bad_request(str(e))
# DASHBOARD DATA ============================================================ End

# VIEW WORKSHOP ============================================================ Begin
# GET http://127.0.0.1:5000/administrator/view
@administrator.get('/view')
@jwt_required()
def read_workshop():
    try:
        # JWT Access Data ========================================
        role = str(get_jwt()["role"])

        status = request.args.get(
            "status",
            "all"
        )

        # Request Process ========================================
        response = AdministratorModels.read_workshop(role, status)

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# VIEW WORKSHOP ============================================================ End

# DETAIL WORKSHOP ============================================================ Begin
# GET http://127.0.0.1:5000/administrator/detail/<int:workshop_id>
@administrator.get('/detail/<int:workshop_id>')
@jwt_required()
def detail_workshop(workshop_id):
    try:
        # JWT Access Data ========================================
        role = str(get_jwt()["role"])

        # Request Process ========================================
        response = AdministratorModels.detail_workshop(role, workshop_id)

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# DETAIL WORKSHOP ============================================================ End

# VERIFY WORKSHOP ============================================================ Begin
# PUT http://127.0.0.1:5000/administrator/verify
@administrator.put('/verify')
@jwt_required()
def verify_workshop():
    try:
        # JWT Access Data ========================================
        role = str(get_jwt()["role"])

        # Request Data ========================================
        body = request.json

        # Request Process ========================================
        response = AdministratorModels.verify_workshop(role, body)

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# VERIFY WORKSHOP ============================================================ End


# ACTIVATE WORKSHOP ============================================================ Begin
# PUT http://127.0.0.1:5000/administrator/activate
@administrator.put('/activate')
@jwt_required()
def activate_workshop():
    try:
        role = str(get_jwt()["role"])
        body = request.json

        response = AdministratorModels.activate_workshop(role, body)

        return response

    except Exception as e:
        return bad_request(str(e))
# ACTIVATE WORKSHOP ============================================================ End


# DEACTIVATE WORKSHOP ============================================================ Begin
# PUT http://127.0.0.1:5000/administrator/deactivate
@administrator.put('/deactivate')
@jwt_required()
def deactivate_workshop():
    try:
        role = str(get_jwt()["role"])
        body = request.json

        response = AdministratorModels.deactivate_workshop(role, body)

        return response

    except Exception as e:
        return bad_request(str(e))
# DEACTIVATE WORKSHOP ============================================================ End


# DELETE WORKSHOP ============================================================ Begin
# DELETE http://127.0.0.1:5000/administrator/delete
@administrator.delete('/delete')
@jwt_required()
def delete_workshop():
    try:
        role = str(get_jwt()["role"])
        body = request.json

        response = AdministratorModels.delete_workshop(role, body)

        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE WORKSHOP ============================================================ End