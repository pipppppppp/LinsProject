from datetime import datetime
import time

from ... import db
from ...database.db_workshops import Workshops
from ...database.db_customers import Customers
from ...database.db_vehicles import Vehicles

from ...utilities.validators import role_validator, vehicle_validator

from apps.utilities.responseHelpers import *
from apps.utilities.utilities import current_timestamp
from apps.utilities.formatter import format_date


# VEHICLE MODEL CLASS ============================================================ Begin
class VehicleModels():
    # CREATE VEHICLE ============================================================ Begin
    def create_vehicle(user_role, workshop_id, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)

            if not access:
                return authorization_error()
            
            subscription_access = subscription_validator(user_role, workshop_id)

            if not subscription_access:
                return subscription_required()
            # Access Validation ---------------------------------------- Finish

            # Check Request Body ---------------------------------------- Start
            if datas is None:
                return invalid_params()

            required_data = [
                "customer_id",
                "plate_number",
                "vehicle_brand",
                "vehicle_type",
                "vehicle_year",
                "vehicle_color"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )
            # Check Request Body ---------------------------------------- Finish

            # Initialize Data Input ---------------------------------------- Start
            customer_id = datas["customer_id"]
            plate_number = datas["plate_number"].strip().upper()
            vehicle_brand = datas["vehicle_brand"].strip()
            vehicle_type = datas["vehicle_type"].strip()
            vehicle_year = datas["vehicle_year"]
            vehicle_color = datas["vehicle_color"].strip()
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checker_result = vehicle_validator(
                customer_id,
                plate_number,
                vehicle_brand,
                vehicle_type,
                vehicle_year,
                vehicle_color,
                workshop_id
            )

            if len(checker_result) != 0:
                return defined_error(
                    checker_result,
                    "Defined Error",
                    499
                )
            # Data Validation ---------------------------------------- Finish

            # Check Workshop ---------------------------------------- Start
            workshop = Workshops.query.filter_by(
                id=workshop_id,
                is_delete=0
            ).first()

            if not workshop:
                return not_found(
                    "Workshop could not be found."
                )
            # Check Workshop ---------------------------------------- Finish

            # Check Customer ---------------------------------------- Start
            customer = Customers.query.filter_by(
                id=customer_id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not customer:
                return not_found(
                    "Customer could not be found."
                )
            # Check Customer ---------------------------------------- Finish

            # Insert Data ---------------------------------------- Start
            timestamp = current_timestamp()

            data = Vehicles(
                workshop_id=workshop_id,
                customer_id=customer_id,
                plate_number=plate_number,
                vehicle_brand=vehicle_brand,
                vehicle_type=vehicle_type,
                vehicle_year=vehicle_year,
                vehicle_color=vehicle_color,
                created_at=timestamp,
                updated_at=timestamp
            )

            try:
                db.session.add(data)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Insert Data ---------------------------------------- Finish

            # Return Response ========================================
            return success(
                status_code=201
            )
        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # CREATE VEHICLE ============================================================ End

    # READ VEHICLE ============================================================ Begin
    def read_vehicle(user_role, workshop_id, customer_id):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)

            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Check Workshop ---------------------------------------- Start
            workshop = Workshops.query.filter_by(
                id=workshop_id,
                is_delete=0
            ).first()

            if not workshop:
                return not_found(
                    "Workshop could not be found."
                )
            # Check Workshop ---------------------------------------- Finish

            # Check Customer ---------------------------------------- Start
            customer = Customers.query.filter_by(
                id=customer_id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not customer:
                return not_found(
                    "Customer could not be found."
                )
            # Check Customer ---------------------------------------- Finish

            # Get Data ---------------------------------------- Start
            vehicles = Vehicles.query.filter_by(
                workshop_id=workshop_id,
                customer_id=customer_id,
                is_delete=0
            ).all()
            # Get Data ---------------------------------------- Finish

            # Initialize Data ---------------------------------------- Start
            data = []

            for vehicle in vehicles:

                created_at = format_date(vehicle.created_at)

                updated_at = format_date(vehicle.updated_at)
                

                deleted_at = None

                if vehicle.deleted_at:
                    deleted_at = format_date(vehicle.deleted_at)
                    

                data.append({
                    "id": vehicle.id,
                    "customer_id": vehicle.customer_id,
                    "plate_number": vehicle.plate_number,
                    "vehicle_brand": vehicle.vehicle_brand,
                    "vehicle_type": vehicle.vehicle_type,
                    "vehicle_year": vehicle.vehicle_year,
                    "vehicle_color": vehicle.vehicle_color,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "deleted_at": deleted_at
                })
            # Initialize Data ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            # Response Data ---------------------------------------- Start
            return success_data(
                data={
                    "customer": {
                        "id": customer.id,
                        "customer_name": customer.customer_name,
                        "customer_phone": customer.customer_phone,
                        "customer_address": customer.customer_address,
                    },
                    "vehicles": data
                },
                status_code=200
            )

        except Exception as e:
            return bad_request(str(e))
    # READ VEHICLE ============================================================ End

    # UPDATE VEHICLE ============================================================ Begin
    def update_vehicle(user_role, workshop_id, id, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)

            if not access:
                return authorization_error()
            
            subscription_access = subscription_validator(user_role, workshop_id)

            if not subscription_access:
                return subscription_required()
            # Access Validation ---------------------------------------- Finish

            # Check Request Body ---------------------------------------- Start
            if datas is None:
                return invalid_params()

            required_data = [
                "customer_id",
                "plate_number",
                "vehicle_brand",
                "vehicle_type",
                "vehicle_year",
                "vehicle_color"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )
            # Check Request Body ---------------------------------------- Finish

            # Initialize Data Input ---------------------------------------- Start
            customer_id = datas["customer_id"]
            plate_number = datas["plate_number"].strip().upper()
            vehicle_brand = datas["vehicle_brand"].strip()
            vehicle_type = datas["vehicle_type"].strip()
            vehicle_year = datas["vehicle_year"]
            vehicle_color = datas["vehicle_color"].strip()
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checker_result = vehicle_validator(
                customer_id,
                plate_number,
                vehicle_brand,
                vehicle_type,
                vehicle_year,
                vehicle_color,
                workshop_id,
                id
            )

            if len(checker_result) != 0:
                return defined_error(
                    checker_result,
                    "Defined Error",
                    499
                )
            # Data Validation ---------------------------------------- Finish

            # Check Workshop ---------------------------------------- Start
            workshop = Workshops.query.filter_by(
                id=workshop_id,
                is_delete=0
            ).first()

            if not workshop:
                return not_found(
                    "Workshop could not be found."
                )
            # Check Workshop ---------------------------------------- Finish

            # Check Customer ---------------------------------------- Start
            customer = Customers.query.filter_by(
                id=customer_id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not customer:
                return not_found(
                    "Customer could not be found."
                )
            # Check Customer ---------------------------------------- Finish

            # Check Vehicle ---------------------------------------- Start
            data = Vehicles.query.filter_by(
                id=id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not data:
                return not_found(
                    "Vehicle could not be found."
                )
            # Check Vehicle ---------------------------------------- Finish

            # Update Data ---------------------------------------- Start
            timestamp = current_timestamp()

            data.customer_id = customer_id
            data.plate_number = plate_number
            data.vehicle_brand = vehicle_brand
            data.vehicle_type = vehicle_type
            data.vehicle_year = vehicle_year
            data.vehicle_color = vehicle_color
            data.updated_at = timestamp

            try:
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Update Data ---------------------------------------- Finish

            # Return Response ========================================
            return success(
                status_code=200
            )

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # UPDATE VEHICLE ============================================================ End
    
    # DELETE VEHICLE ============================================================ Begin
    def delete_vehicle(user_role, workshop_id, id):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)

            if not access:
                return authorization_error()

            subscription_access = subscription_validator(user_role, workshop_id)

            if not subscription_access:
                return subscription_required()
            # Access Validation ---------------------------------------- Finish

            # Check Workshop ---------------------------------------- Start
            workshop = Workshops.query.filter_by(
                id=workshop_id,
                is_delete=0
            ).first()

            if not workshop:
                return not_found(
                    "Workshop could not be found."
                )
            # Check Workshop ---------------------------------------- Finish

            # Check Vehicle ---------------------------------------- Start
            data = Vehicles.query.filter_by(
                id=id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not data:
                return not_found(
                    "Vehicle could not be found."
                )
            # Check Vehicle ---------------------------------------- Finish

            # Delete Data ---------------------------------------- Start
            timestamp = current_timestamp()

            data.is_delete = 1
            data.deleted_at = timestamp
            data.updated_at = timestamp

            try:
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Delete Data ---------------------------------------- Finish

            # Return Response ========================================
            return success(
                status_code=200
            )

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
        # DELETE VEHICLE ============================================================ End
# VEHICLE MODEL CLASS ============================================================ End