from flask import Blueprint, request, render_template, session, redirect, url_for

from ..models.vehicle import VehicleModels
from ...utilities.responseHelpers import bad_request

# BLUEPRINT ================================================== Begin
vehicle = Blueprint(
    name='vehicle',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/vehicle',
)
# BLUEPRINT ================================================== End


# VEHICLE PAGE ============================================================ Begin
# [GET] http://127.0.0.1:5000/vehicle/
@vehicle.get('/')
def index():
    try:
        # Session Validation ========================================
        if 'user_id' not in session:
            return redirect(
                url_for('auth.signin_page')
            )

        # Role Validation ===========================================
        if session.get('role') != 1:
            return redirect(
                url_for('dashboard.index')
            )

        # Return Page ===============================================
        return render_template(
            title='Kendaraan - POS Bengkel',
            template_name_or_list='vehicle.html',
            active_menu="customer",
        )

    except Exception:
        return render_template(
            title="Error 404 - POS Bengkel",
            template_name_or_list='errorPages/404.html')
# VEHICLE PAGE ============================================================ End


# VIEW VEHICLE DATA ======================================================= Begin
# [GET] http://127.0.0.1:5000/vehicle/view/<customer_id>
@vehicle.get('/view/<int:customer_id>')
def get_vehicle(customer_id):
    try:
        # Request Process ========================================
        response = VehicleModels.view_vehicle(customer_id)

        # Return Data ============================================
        return response

    except Exception as e:
        return bad_request(str(e))
# VIEW VEHICLE DATA ======================================================= End


# ADD VEHICLE DATA ======================================================== Begin
# [POST] http://127.0.0.1:5000/vehicle/add
@vehicle.post('/add')
def create_vehicle():
    try:
        # Request Data ===========================================
        body = request.json

        # Request Process ========================================
        response = VehicleModels.add_vehicle(body)

        # Return Data ============================================
        return response

    except Exception as e:
        return bad_request(str(e))
# ADD VEHICLE DATA ======================================================== End


# DETAIL VEHICLE DATA ===================================================== Begin
# [GET] http://127.0.0.1:5000/vehicle/detail/<id>
@vehicle.get('/detail/<int:id>')
def detail_vehicle(id):
    try:
        # Request Process ========================================
        response = VehicleModels.detail_vehicle(id)

        # Return Data ============================================
        return response

    except Exception as e:
        return bad_request(str(e))
# DETAIL VEHICLE DATA ===================================================== End


# UPDATE VEHICLE DATA ===================================================== Begin
# [PUT] http://127.0.0.1:5000/vehicle/edit/<id>
@vehicle.put('/edit/<int:id>')
def update_vehicle(id):
    try:
        # Request Data ===========================================
        body = request.json

        # Request Process ========================================
        response = VehicleModels.edit_vehicle(body, id)

        # Return Data ============================================
        return response

    except Exception as e:
        return bad_request(str(e))
# UPDATE VEHICLE DATA ===================================================== End


# DELETE VEHICLE DATA ===================================================== Begin
# [DELETE] http://127.0.0.1:5000/vehicle/delete/<id>
@vehicle.delete('/delete/<int:id>')
def delete_vehicle(id):
    try:
        # Request Process ========================================
        response = VehicleModels.delete_vehicle(id)

        # Return Data ============================================
        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE VEHICLE DATA ===================================================== End