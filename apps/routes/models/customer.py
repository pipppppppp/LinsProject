from datetime import datetime
import time

from ... import db
from ...database.db_workshops import Workshops
from ...database.db_customers import Customers
from ...database.db_vehicles import Vehicles
from ...utilities.validators import role_validator, customer_validator, subscription_validator

from apps.utilities.responseHelpers import *
from apps.utilities.utilities import current_timestamp
from apps.utilities.formatter import format_date


# CUSTOMER MODEL CLASS ============================================================ Begin
class CustomerModels():
    # CREATE CUSTOMER ============================================================ Begin
    def create_customer(user_role, workshop_id, datas):
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
                "customer_name",
                "customer_address",
                "customer_phone"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )
            # Check Request Body ---------------------------------------- Finish
            
           # Initialize Data Input ---------------------------------------- Start
            customer_name = datas["customer_name"].strip()
            customer_address = datas["customer_address"].strip()
            customer_phone = datas["customer_phone"]
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checker_result = customer_validator(
                customer_name,
                customer_address,
                customer_phone,
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
            
            timestamp = current_timestamp()

            # Insert Data ---------------------------------------- Start
            data = Customers(
                workshop_id=workshop_id,
                customer_name=customer_name,
                customer_address=customer_address,
                customer_phone=customer_phone,
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
            # return success(statusCode=201)
            return success(
                status_code=201
            )
        
        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # CREATE CUSTOMER ============================================================ End

    # READ CUSTOMER ============================================================ Begin
    def read_customer(user_role, workshop_id):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)
            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Get Data ---------------------------------------- Start
            customers = Customers.query.filter_by(
                workshop_id=workshop_id,
                is_delete=0
            ).order_by(
                Customers.created_at.desc()
            ).all()
            # Get Data ---------------------------------------- Finish
            
            # Initialize Data ---------------------------------------- Start
            data = []

            for customer in customers:

                created_at = format_date(customer.created_at)

                updated_at = format_date(customer.updated_at)

                deleted_at = None

                if customer.deleted_at:
                    deleted_at = format_date(customer.deleted_at)

                vehicles = Vehicles.query.filter_by(
                    customer_id=customer.id,
                    is_delete=0
                ).all()
                total_vehicle = len(vehicles)

                data.append({
                    "id": customer.id,
                    "customer_name": customer.customer_name,
                    "customer_address": customer.customer_address,
                    "customer_phone": customer.customer_phone,
                    "total_vehicle": total_vehicle,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "deleted_at": deleted_at
                })
            # Initialize Data ---------------------------------------- Finish

            # Summary Data ---------------------------------------- Start
            total_customer = len(customers)

            total_vehicle = Vehicles.query.filter_by(
                workshop_id=workshop_id,
                is_delete=0
            ).count()
            # Summary Data ---------------------------------------- End


            # Response Data ---------------------------------------- Start
            return success_data(
                data={
                    "customer": data,
                    "total_customer": total_customer,
                    "total_vehicle": total_vehicle
                },
                status_code=200
            )
        
        except Exception as e:
            return bad_request(str(e))
    # READ CUSTOMER ============================================================ End

    # UPDATE CUSTOMER ============================================================ Begin
    def update_customer(user_role, workshop_id, id, datas):
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
                "customer_name",
                "customer_address",
                "customer_phone"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )
            # Check Request Body ---------------------------------------- Finish

            # Initialize Data Input ---------------------------------------- Start
            customer_name = datas["customer_name"].strip()
            customer_address = datas["customer_address"].strip()
            customer_phone = datas["customer_phone"]
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checker_result = customer_validator(
                customer_name,
                customer_address,
                customer_phone,
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
            data = Customers.query.filter_by(
                id=id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not data:
                return not_found(
                    "Customer could not be found."
                )
            # Check Customer ---------------------------------------- Finish

            # Update Data ---------------------------------------- Start
            timestamp = current_timestamp()
            data.customer_name = customer_name
            data.customer_address = customer_address
            data.customer_phone = customer_phone
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
    # UPDATE CUSTOMER ============================================================ End
    
    # DELETE CUSTOMER ============================================================ Begin
    def delete_customer(user_role, workshop_id, id):
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

            # Check Customer ---------------------------------------- Start
            data = Customers.query.filter_by(
                id=id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not data:
                return not_found(
                    "Customer could not be found."
                )
            # Check Customer ---------------------------------------- Finish

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
    # DELETE CUSTOMER ============================================================ End
# CUSTOMER MODEL CLASS ============================================================ End