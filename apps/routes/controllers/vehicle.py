from flask import Blueprint, request, render_template
from flask_jwt_extended import jwt_required, get_jwt
from ...database.db_customers import Customers

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
@vehicle.get('/<int:customer_id>')
@jwt_required()
def index(customer_id):
    try:
        customer = Customers.query.filter_by(
            id=customer_id,
            is_delete=0
        ).first()

        if customer is None:
            return bad_request("Customer not found")

        return render_template(
            title='Kendaraan - POS Bengkel',
            template_name_or_list='vehicle.html',
            active_menu="customer",
            customer_id=customer_id,
            customer_name=customer.customer_name,
            customer_phone=customer.customer_phone,
            customer_address=customer.customer_address
        )

    except Exception as e:
        return bad_request(str(e))
# VEHICLE PAGE ============================================================ End


# VIEW VEHICLE DATA ======================================================= Begin
# [GET] http://127.0.0.1:5000/vehicle/view/<customer_id>
@vehicle.get('/view/<int:customer_id>')
@jwt_required()
def read_vehicle(customer_id):
    try:

        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        response = VehicleModels.read_vehicle(role, ws_id, customer_id)

        return response

    except Exception as e:
        return bad_request(str(e))
# VIEW VEHICLE DATA ======================================================= End


# ADD VEHICLE DATA ======================================================== Begin
# [POST] http://127.0.0.1:5000/vehicle/add
@vehicle.post('/add')
@jwt_required()
def create_vehicle():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])
        
        body = request.json

        response = VehicleModels.create_vehicle(role, ws_id, body)
        return response

    except Exception as e:
        return bad_request(str(e))
# ADD VEHICLE DATA ======================================================== End


# UPDATE VEHICLE DATA ===================================================== Begin
# [PUT] http://127.0.0.1:5000/vehicle/edit/<id>
@vehicle.put('/edit/<int:id>')
@jwt_required()
def update_vehicle(id):
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        body = request.json

        response = VehicleModels.update_vehicle(role, ws_id, id, body)
        return response

    except Exception as e:
        return bad_request(str(e))
# UPDATE VEHICLE DATA ===================================================== End


# DELETE VEHICLE DATA ===================================================== Begin
# [DELETE] http://127.0.0.1:5000/vehicle/delete/<id>
@vehicle.delete('/delete/<int:id>')
@jwt_required()
def delete_vehicle(id):
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        response = VehicleModels.delete_vehicle(role, ws_id, id)
        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE VEHICLE DATA ===================================================== End