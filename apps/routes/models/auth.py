from flask_jwt_extended import create_access_token, set_access_cookies
import time

from apps import db
from apps.database.db_users import Users
from apps.database.db_cashier import Cashiers
from apps.database.db_workshops import Workshops
from apps.routes.models.workshop import WorkshopModels
from apps.utilities.responseHelpers import *
from apps.utilities.utilities import hash_password
from apps.utilities.validators import signin_validator, signup_validator


# AUTH MODELS ============================================================ Begin
class AuthModels():
    # SIGN UP ============================================================ Begin
    def signup(datas):
        try:
            # Validation Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            required_data = [
                "owner_name",
                "username",
                "email",
                "password",
                "retype_password",
                "workshop_name",
                "workshop_address",
                "workshop_phone"
            ]
            for req in required_data:
                if req not in datas:
                    return parameter_error(f"Missing {req} in request body.")
            # Validation Request Body ---------------------------------------- Finish
            
            # Initialize Data Input ---------------------------------------- Start
            owner_name = datas["owner_name"].strip()
            username = datas["username"].strip()
            email = datas["email"].strip()
            password = datas["password"]
            retype_password = datas["retype_password"]
            workshop_name = datas["workshop_name"]
            workshop_address = datas["workshop_address"]
            workshop_phone = datas["workshop_phone"]
            # Initialize Data Input ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            checker_result = signup_validator(owner_name, username, email, password, retype_password, workshop_name, workshop_address, workshop_phone)
           
            if len(checker_result) != 0:
                return defined_error(checker_result, "Bad Request", status_code=400)
            # Data Validation ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            # Initialize
            password_encrypt = hash_password(password)
            timestamp = int(round(time.time()*1000))
            user_data = Users(
                owner_name=owner_name,
                username=username,
                email=email,
                password=password_encrypt,
                role=1,
                is_active=0,
                created_at=timestamp,
                updated_at=timestamp
            )

            # Save Data
            db.session.add(user_data)
            db.session.commit()
            # Insert Data ---------------------------------------- Finish

            # Insert Workshop ---------------------------------------- Start
            # user_data = Users.query.filter_by(email=email, is_delete=0).first()
            workshop = WorkshopModels.create_workshop(user_data.id, user_data.role, datas)
            if workshop.status_code != 200:
                user_data.is_delete = 1
                user_data.deleted_at = int(time.time())
                db.session.commit()
                return workshop
            # Insert Workshop ---------------------------------------- Finish

            # Data Payload ---------------------------------------- Start
            # workshop_data = Workshops.query.filter_by(owner_id=user_data.id, is_delete=0).first()
            # jwt_payload = {
            #     "id" : user_data.id,
            #     "email" : user_data.email,
            #     "username" : user_data.username,
            #     "role" : user_data.role,
            #     "ws_id" : user_data.workshops[0].id
            # }
            # Data Payload ---------------------------------------- Finish
            
            # Access Token by Email ======================================== 
            # access_token = create_access_token(email, additional_claims=jwt_payload)
            
            # Data Response ---------------------------------------- Start
            # response = success_data({
            #     "access_token" : access_token,
            #     "role" : user_data.role
            # })
            # set_access_cookies(response, access_token)
            # Data Response ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return success(
                message="Registrasi berhasil. Akun Anda sedang menunggu verifikasi Administrator."
            )

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # SIGN UP ============================================================ End

    # SIGN IN ============================================================ Begin
    def signin(datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["usermail", "password"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in request body.")
            # Checking Request Body ---------------------------------------- Finish
            
            # Initialize Data Input ---------------------------------------- Start
            usermail = datas["usermail"].strip().lower()
            password = datas["password"].strip()
            # Initialize Data Input ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            checker_result, result, stts = signin_validator(usermail, password)

            if len(checker_result) > 0:
                return defined_error(checker_result, "Bad Request", status_code=stts)
            # Data Validation ---------------------------------------- Finish
            
            # Update Data Last Active ---------------------------------------- Start
            # Update Data Last Active ---------------------------------------- Finish
            
            # Log Activity Record ---------------------------------------- Start
            # Log Activity Record ---------------------------------------- Finish

            # Generate File URL ---------------------------------------- Start
            # Generate File URL ---------------------------------------- Finish
            
            # Get Workshop ID ---------------------------------------- Start
            if str(result.role) == "1":
                    ws_id = result.workshops[0].id if result.workshops else None

            elif str(result.role) == "2":
                cashier = Cashiers.query.filter_by(
                    user_id=result.id,
                    is_delete=0
                ).first()

                ws_id = cashier.workshop_id if cashier else None

            else:
                ws_id = None
            # Get Workshop ID ---------------------------------------- Finish
           
            # Data Payload ---------------------------------------- Start
            # workshop_data = Workshops.query.filter_by(owner_id=result.id, is_delete=0).first()
            jwt_payload = {
                "id" : result.id,
                "email" : result.email,
                "name" : result.username,
                "role" : result.role,
                "ws_id" : ws_id
            }
            # Data Payload ---------------------------------------- Finish

            # Access Token by Email ======================================== 
            access_token = create_access_token(result.email, additional_claims=jwt_payload)

            # Data Response ---------------------------------------- Start
            response = success_data({
                "access_token" : access_token,
                "role" : result.role,
                "name": result.username
            })
            set_access_cookies(response, access_token)
            # Data Response ---------------------------------------- Finish

            # Return Response ======================================== 
            return response

        except Exception as e:
            return bad_request(str(e))
    # SIGN IN ============================================================ End
    
# AUTH MODELS ============================================================ End
