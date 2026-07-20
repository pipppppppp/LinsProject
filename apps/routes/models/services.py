from datetime import datetime
import time

from ... import db
from ...database.db_workshops import Workshops
from ...database.db_services import Services
from ...utilities.validators import role_validator, service_validator

from apps.utilities.responseHelpers import *
from apps.utilities.utilities import split_date_time


# SERVICE MODEL CLASS ============================================================ Begin
class ServiceModels():

    # CREATE SERVICE ============================================================ Begin
    def create_service(user_role, workshop_id, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)
            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Check Request Body ---------------------------------------- Start
            if datas is None:
                return invalid_params()

            required_data = [
                "name",
                "service_fee",
                "description"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )
            # Check Request Body ---------------------------------------- Finish

            # Initialize Data Input ---------------------------------------- Start
            name = datas["name"].strip()
            service_fee = str(datas["service_fee"]).strip()
            description = datas["description"].strip()
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checker_result = service_validator(
                name,
                service_fee,
                description,
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
            data = Services(
                workshop_id=workshop_id,
                name=name,
                service_fee=int(service_fee),
                description=description,
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
    # CREATE SERVICE ============================================================ End

    # READ SERVICE ============================================================ Begin
    def read_service(user_role, workshop_id):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)
            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Get Data ---------------------------------------- Start
            services = Services.query.filter_by(
                workshop_id=workshop_id,
                is_delete=0
            ).all()
            # Get Data ---------------------------------------- Finish

            # Initialize Data ---------------------------------------- Start
            data = []

            for service in services:

                created_at = split_date_time(
                    datetime.fromtimestamp(service.created_at / 1000)
                )

                updated_at = split_date_time(
                    datetime.fromtimestamp(service.updated_at / 1000)
                )

                deleted_at = None

                if service.deleted_at:
                    deleted_at = split_date_time(
                        datetime.fromtimestamp(service.deleted_at / 1000)
                    )

                data.append({
                    "id": service.id,
                    "name": service.name,
                    "service_fee": service.service_fee,
                    "description": service.description,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "deleted_at": deleted_at
                })
            # Initialize Data ---------------------------------------- Finish

            return success_data(
                data=data,
                status_code=200
            )

        except Exception as e:
            return bad_request(str(e))
    # READ SERVICE ============================================================ End

    # UPDATE SERVICE ============================================================ Begin
    def update_service(user_role, workshop_id, id, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)
            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Check Request Body ---------------------------------------- Start
            if datas is None:
                return invalid_params()

            required_data = [
                "name",
                "service_fee",
                "description"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )
            # Check Request Body ---------------------------------------- Finish

            # Initialize Data Input ---------------------------------------- Start
            name = datas["name"].strip()
            service_fee = str(datas["service_fee"]).strip()
            description = datas["description"].strip()
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checker_result = service_validator(
                name,
                service_fee,
                description,
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

            # Check Service ---------------------------------------- Start
            data = Services.query.filter_by(
                id=id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not data:
                return not_found(
                    "Service could not be found."
                )
            # Check Service ---------------------------------------- Finish

            # Update Data ---------------------------------------- Start
            timestamp = int(time.time() * 1000)

            data.name = name
            data.service_fee = int(service_fee)
            data.description = description
            data.updated_at = timestamp

            try:
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Update Data ---------------------------------------- Finish

            return success(
                status_code=200
            )

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # UPDATE SERVICE ============================================================ End

    # DELETE SERVICE ============================================================ Begin
    def delete_service(user_role, workshop_id, id):
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

            # Check Service ---------------------------------------- Start
            data = Services.query.filter_by(
                id=id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not data:
                return not_found(
                    "Service could not be found."
                )
            # Check Service ---------------------------------------- Finish

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

            return success(
                status_code=200
            )

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # DELETE SERVICE ============================================================ End

# SERVICE MODEL CLASS ============================================================ End