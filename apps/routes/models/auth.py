from flask_jwt_extended import create_access_token, set_access_cookies
from flask import request
import secrets

from apps import db
from apps.database.db_users import Users
from apps.database.db_cashier import Cashiers
from apps.database.db_workshops import Workshops
from apps.routes.models.workshop import WorkshopModels
from apps.utilities.responseHelpers import *
from apps.utilities.utilities import hash_password, email_sender, current_timestamp
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
            email = datas["email"].strip().lower()
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
            timestamp = current_timestamp()
            verification_token = secrets.token_urlsafe(32)
            verification_token_expired_at = timestamp + (24 * 60 * 60 * 1000)

            user_data = Users(
                owner_name=owner_name,
                username=username,
                email=email,
                email_verified_at=None,
                verification_token=verification_token,
                verification_token_expired_at=verification_token_expired_at,
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
            workshop = WorkshopModels.create_workshop(user_data.id, user_data.role, datas)
            if workshop.status_code != 200:
                user_data.is_delete = 1
                user_data.deleted_at = int(time.time() * 1000)
                db.session.commit()
                return workshop
            # Insert Workshop ---------------------------------------- Finish

            # Send Verification Email ---------------------------------------- Start
            verification_url = (
                f"{request.host_url.rstrip('/')}"
                f"/auth/verify-email/{user_data.verification_token}"
            )

            email_content = f"""
            <div style="font-family: Arial, sans-serif;">
                <h2>Verifikasi Akun POS Bengkel</h2>

                <p>Halo {user_data.owner_name},</p>

                <p>
                    Registrasi akun Anda berhasil. Silakan klik tombol berikut
                    untuk mengaktifkan akun Anda.
                </p>

                <a
                    href="{verification_url}"
                    style="
                        display: inline-block;
                        padding: 12px 20px;
                        background-color: #435ebe;
                        color: #ffffff;
                        text-decoration: none;
                        border-radius: 5px;
                    "
                >
                    Verifikasi Akun
                </a>

                <p>Link verifikasi ini berlaku selama 24 jam.</p>

                <p>
                    Abaikan email ini apabila Anda tidak melakukan registrasi.
                </p>
            </div>
            """

            email_response = email_sender(
                user_data.email,
                "Verifikasi Akun POS Bengkel",
                email_content
            )

            if email_response.status_code != 200:
                return bad_request(
                    "Registrasi berhasil, tetapi email verifikasi gagal dikirim."
                )
            # Send Verification Email ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(
                message="Registrasi berhasil. Silakan periksa email Anda untuk melakukan verifikasi akun."
            )

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # SIGN UP ============================================================ End

    # VERIFY EMAIL ============================================================ Begin
    def verify_email(token):
        try:
            # Token Validation ---------------------------------------- Start
            if token is None or token.strip() == "":
                return bad_request(
                    "Token verifikasi tidak valid."
                )
            # Token Validation ---------------------------------------- Finish

            # Initialize Timestamp ---------------------------------------- Start
            timestamp = current_timestamp()
            # Initialize Timestamp ---------------------------------------- Finish

            # Get User ---------------------------------------- Start
            user_data = Users.query.filter_by(
                verification_token=token,
                is_delete=0
            ).first()

            if not user_data:
                return not_found(
                    "Token verifikasi tidak ditemukan atau sudah digunakan."
                )
            # Get User ---------------------------------------- Finish

            # Token Expiration Validation ---------------------------------------- Start
            if (
                user_data.verification_token_expired_at is None or
                int(user_data.verification_token_expired_at) <= timestamp
            ):
                return bad_request(
                    "Link verifikasi sudah kedaluwarsa."
                )
            # Token Expiration Validation ---------------------------------------- Finish

            # Get Workshop ---------------------------------------- Start
            workshop_data = Workshops.query.filter_by(
                owner_id=user_data.id,
                is_delete=0
            ).first()

            if not workshop_data:
                return not_found(
                    "Data bengkel tidak ditemukan."
                )
            # Get Workshop ---------------------------------------- Finish

            # Activate Account ---------------------------------------- Start
            user_data.email_verified_at = timestamp
            user_data.verification_token = None
            user_data.verification_token_expired_at = None
            user_data.is_active = 1
            user_data.updated_at = timestamp

            workshop_data.is_active = 1
            workshop_data.updated_at = timestamp

            db.session.commit()
            # Activate Account ---------------------------------------- Finish

            # Return Response ========================================
            return success(
                message="Verifikasi email berhasil. Silakan login."
            )

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # VERIFY EMAIL ============================================================ End

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
