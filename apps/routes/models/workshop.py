import time
import os

from apps.configure.config import STATIC_FOLDER_PATH

from apps import db
from apps.database.db_workshops import Workshops
from apps.utilities.responseHelpers import *
from apps.utilities.validators import role_validator, workshop_validator, email_checker, saving_upload_image


# WORKSHOP MODEL CLASS ============================================================ Begin
class WorkshopModels():
    # CREATE WORKSHOP ============================================================ Begin
    def create_workshop(user_id, user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)
            if not access: # Access = True -> Owner/ Administrator
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            required_data = ["workshop_name", "workshop_address", "workshop_phone"]
            for req in required_data:
                if req not in datas:
                    return parameter_error(f"Missing {req} in request body.")
            # Checking Request Body ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            workshop_name = datas["workshop_name"].strip()
            workshop_address = datas["workshop_address"]
            workshop_phone = datas["workshop_phone"]
            checker_result = workshop_validator(user_id, workshop_name, workshop_address, workshop_phone)
            if len(checker_result) != 0:
                return defined_error(checker_result, "Defined Error", 499)
            # Data Validation ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            # Initialize
            timestamp = int(time.time()*1000)
            data = Workshops(
                workshop_name=workshop_name,
                owner_id=user_id,
                workshop_address=workshop_address,
                workshop_phone=workshop_phone,
                created_at=timestamp,
                updated_at=timestamp
            )

            # Save Data
            try:
                db.session.add(data)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Insert Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(status_code=201)
        
        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # CREATE WORKSHOP ============================================================ End
    
    # READ WORKSHOP ============================================================ Begin
    def read_workshop(user_role, workshop_id):
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

            # Initialize Data ---------------------------------------- Start
            data = {
                "id": workshop.id,
                "workshop_name": workshop.workshop_name,
                "workshop_address": workshop.workshop_address,
                "workshop_phone": workshop.workshop_phone,
                "workshop_email": workshop.workshop_email,
                "logo": workshop.logo,
                "is_verified": workshop.is_verified,
                "is_active": workshop.is_active
            }
            # Initialize Data ---------------------------------------- Finish

            # Return Response ========================================
            return success_data(
                data=data,
                status_code=200
            )

        except Exception as e:
            return bad_request(str(e))
    # READ WORKSHOP ============================================================ End

    # UPDATE WORKSHOP ============================================================ Begin
    def update_workshop(user_role, workshop_id, datas, logo):
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
                "workshop_name",
                "workshop_address",
                "workshop_phone",
                "workshop_email"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )
            # Check Request Body ---------------------------------------- Finish

            # Initialize Data Input ---------------------------------------- Start
            workshop_name = datas["workshop_name"].strip()
            workshop_address = datas["workshop_address"].strip()
            workshop_phone = datas["workshop_phone"].strip()
            workshop_email = datas["workshop_email"].strip()
            # Initialize Data Input ---------------------------------------- Finish

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

            # Data Validation ---------------------------------------- Start
            checker_result = workshop_validator(
                workshop.owner_id,
                workshop_name,
                workshop_address,
                workshop_phone,
                False
            )

            if workshop_email != "":
                if email_checker(workshop_email):
                    checker_result.append(
                        "Email tidak valid."
                    )

            if len(checker_result) != 0:
                return defined_error(
                    checker_result,
                    "Defined Error",
                    499
                )
            # Data Validation ---------------------------------------- Finish

            # Update Data ---------------------------------------- Start
            timestamp = current_timestamp()

            if logo:
                filename = saving_upload_image(
                    logo,
                    os.path.join(
                        STATIC_FOLDER_PATH,
                        "images",
                        "profiles"
                    )
                )

                workshop.logo = filename

            workshop.workshop_name = workshop_name
            workshop.workshop_address = workshop_address
            workshop.workshop_phone = workshop_phone
            workshop.workshop_email = workshop_email
            workshop.updated_at = timestamp

            try:
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Update Data ---------------------------------------- Finish

            # Return Response ========================================
            return success(status_code=200)

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # UPDATE WORKSHOP ============================================================ End

# WORKSHOP MODEL CLASS ============================================================ End