from datetime import datetime
import time

from ... import db
from ...database.db_workshops import Workshops
from ...database.db_suppliers import Suppliers
from ...utilities.validators import role_validator, supplier_validator, subscription_validator

from apps.utilities.responseHelpers import *
from apps.utilities.utilities import current_timestamp
from apps.utilities.formatter import format_date


# SUPPLIER MODEL CLASS ============================================================ Begin
class SupplierModels():

    # CREATE SUPPLIER ============================================================ Begin
    def create_supplier(user_role, workshop_id, datas):
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
                "name",
                "phone",
                "address"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )
            # Check Request Body ---------------------------------------- Finish

            # Initialize Data Input ---------------------------------------- Start
            name = datas["name"].strip()
            phone = datas["phone"]
            address = datas["address"].strip()
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checker_result = supplier_validator(
                name,
                phone,
                address,
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

            # Insert Data ---------------------------------------- Start
            timestamp = current_timestamp()

            data = Suppliers(
                workshop_id=workshop_id,
                name=name,
                phone=phone,
                address=address,
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
    # CREATE SUPPLIER ============================================================ End


    # READ SUPPLIER ============================================================ Begin
    def read_supplier(user_role, workshop_id):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)
            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Get Data ---------------------------------------- Start
            suppliers = Suppliers.query.filter_by(
                workshop_id=workshop_id,
                is_delete=0
            ).all()
            # Get Data ---------------------------------------- Finish

            # Initialize Data ---------------------------------------- Start
            data = []

            for supplier in suppliers:

                created_at = format_date(supplier.created_at)
                

                updated_at = format_date(supplier.updated_at)
                

                deleted_at = None

                if supplier.deleted_at:
                    deleted_at = format_date(supplier.deleted_at)
                    

                data.append({
                    "id": supplier.id,
                    "name": supplier.name,
                    "phone": supplier.phone,
                    "address": supplier.address,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "deleted_at": deleted_at
                })
            # Initialize Data ---------------------------------------- Finish

            # Return Response ========================================
            return success_data(
                data=data,
                status_code=200
            )

        except Exception as e:
            return bad_request(str(e))
    # READ SUPPLIER ============================================================ End


    # UPDATE SUPPLIER ============================================================ Begin
    def update_supplier(user_role, workshop_id, id, datas):
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
                "name",
                "phone",
                "address"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )
            # Check Request Body ---------------------------------------- Finish

            # Initialize Data Input ---------------------------------------- Start
            name = datas["name"].strip()
            phone = datas["phone"]
            address = datas["address"].strip()
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checker_result = supplier_validator(
                name,
                phone,
                address,
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

            # Check Supplier ---------------------------------------- Start
            data = Suppliers.query.filter_by(
                id=id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not data:
                return not_found(
                    "Supplier could not be found."
                )
            # Check Supplier ---------------------------------------- Finish

            # Update Data ---------------------------------------- Start
            timestamp = current_timestamp()

            data.name = name
            data.phone = phone
            data.address = address
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
    # UPDATE SUPPLIER ============================================================ End


    # DELETE SUPPLIER ============================================================ Begin
    def delete_supplier(user_role, workshop_id, id):
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

            # Check Supplier ---------------------------------------- Start
            data = Suppliers.query.filter_by(
                id=id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not data:
                return not_found(
                    "Supplier could not be found."
                )
            # Check Supplier ---------------------------------------- Finish

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
    # DELETE SUPPLIER ============================================================ End

# SUPPLIER MODEL CLASS ============================================================ End