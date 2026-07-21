from datetime import datetime
import time

from ... import db
from ...database.db_workshops import Workshops
from ...database.db_users import Users
from ...utilities.validators import owner_validator, user_validator

from apps.utilities.responseHelpers import *
from apps.utilities.utilities import hash_password, split_date_time


# CASHIER MANAGEMENT MODEL CLASS =============================================== Begin
class CashierManagementModels():

    # CREATE CASHIER ============================================================ Begin
    def create_cashier(user_role, workshop_id, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = owner_validator(user_role)

            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Check Request Body ---------------------------------------- Start
            if datas is None:
                return invalid_params()

            required_data = [
                "owner_name",
                "username",
                "email",
                "password",
                "role",
                "is_active"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )
            # Check Request Body ---------------------------------------- Finish

            # Initialize Data Input ---------------------------------------- Start
            owner_name = datas["owner_name"].strip()
            username = datas["username"].strip()
            email = datas["email"].strip().lower()
            password = datas["password"]
            role = str(datas["role"])
            is_active = int(datas["is_active"])
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checker_result = user_validator(
                owner_name,
                username,
                email,
                password,
                role,
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

            timestamp = int(time.time() * 1000)

            # Insert Data ---------------------------------------- Start
            data = Users(
                owner_name=owner_name,
                username=username,
                email=email,
                password=hash_password(password),
                role=role,
                is_active=is_active,
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
    # CREATE CASHIER ============================================================ End
        # READ CASHIER ============================================================ Begin
    def read_cashier(user_role, workshop_id):
        try:
            # Access Validation ---------------------------------------- Start
            access = owner_validator(user_role)

            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Get Data ---------------------------------------- Start
            cashiers = Users.query.filter_by(
                role="2",
                is_delete=0
            ).all()
            # Get Data ---------------------------------------- Finish

            # Initialize Data ---------------------------------------- Start
            data = []

            for cashier in cashiers:

                created_at = split_date_time(
                    datetime.fromtimestamp(cashier.created_at / 1000)
                )

                updated_at = split_date_time(
                    datetime.fromtimestamp(cashier.updated_at / 1000)
                )

                deleted_at = None

                if cashier.deleted_at:
                    deleted_at = split_date_time(
                        datetime.fromtimestamp(cashier.deleted_at / 1000)
                    )

                data.append({
                    "id": cashier.id,
                    "owner_name": cashier.owner_name,
                    "username": cashier.username,
                    "email": cashier.email,
                    "role": cashier.role,
                    "is_active": cashier.is_active,
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
    # READ CASHIER ============================================================ End

        # UPDATE CASHIER ============================================================ Begin
    def update_cashier(user_role, workshop_id, id, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = owner_validator(user_role)

            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Check Request Body ---------------------------------------- Start
            if datas is None:
                return invalid_params()

            required_data = [
                "owner_name",
                "username",
                "email",
                "password",
                "role",
                "is_active"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )
            # Check Request Body ---------------------------------------- Finish

            # Initialize Data Input ---------------------------------------- Start
            owner_name = datas["owner_name"].strip()
            username = datas["username"].strip()
            email = datas["email"].strip().lower()
            password = datas["password"]
            role = str(datas["role"])
            is_active = int(datas["is_active"])
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checker_result = user_validator(
                owner_name,
                username,
                email,
                password,
                role,
                workshop_id,
                id,
                True
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

            # Check Cashier ---------------------------------------- Start
            data = Users.query.filter_by(
                id=id,
                role="2",
                is_delete=0
            ).first()

            if not data:
                return not_found(
                    "Cashier could not be found."
                )
            # Check Cashier ---------------------------------------- Finish

            # Update Data ---------------------------------------- Start
            timestamp = int(time.time() * 1000)

            data.owner_name = owner_name
            data.username = username
            data.email = email
            data.role = role
            data.is_active = is_active

            if password != "":
                data.password = hash_password(password)

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
    # UPDATE CASHIER ============================================================ End

        # DELETE CASHIER ============================================================ Begin
    def delete_cashier(user_role, workshop_id, id):
        try:
            # Access Validation ---------------------------------------- Start
            access = owner_validator(user_role)

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

            # Check Cashier ---------------------------------------- Start
            data = Users.query.filter_by(
                id=id,
                role="2",
                is_delete=0
            ).first()

            if not data:
                return not_found(
                    "Cashier could not be found."
                )
            # Check Cashier ---------------------------------------- Finish

            # Delete Data ---------------------------------------- Start
            timestamp = int(time.time() * 1000)

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
    # DELETE CASHIER ============================================================ End


# CASHIER MANAGEMENT MODEL CLASS =============================================== End