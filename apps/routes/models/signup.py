from flask import jsonify, make_response
from flask_jwt_extended import create_access_token
from flask import request
from ...database.db_users import Users

import time


# SIGNUP MODEL ============================================================ Begin
class SignupModels():

    # SIGNUP ============================================================ Begin
    def signup(datas):
        try:
            # REQUEST BODY VALIDATION ================================ Start
            if datas is None:
                return invalid_params()

            required_data = [
                "username",
                "email",
                "password",
                "confirm_password",
                "workshop_name",
                "workshop_address",
                "workshop_phone"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(f"Missing {req} in request body.")
            # REQUEST BODY VALIDATION ================================ Finish

            # REQUEST DATA ======================================== Start
            username = datas["username"]
            email = datas["email"]
            password = datas["password"]
            confirm_password = datas["confirm_password"]
            workshop_name = datas["workshop_name"]
            workshop_address = datas["workshop_address"]
            workshop_phone = datas["workshop_phone"]
            # REQUEST DATA ======================================== Finish

            # DATA VALIDATION ======================================== Start
            checker_result = signup_validator(
                username,
                email,
                password,
                confirm_password,
                workshop_name,
                workshop_address,
                workshop_phone
            )

            if len(checker_result) > 0:
                return defined_error(checker_result, "Bad Request", statusCode=400)
            # DATA VALIDATION ======================================== Finish


            # CHECK USERNAME ======================================== Start
            user = Users.query.filter_by(
                username=username,
                is_delete=0
            ).first()

            if user is not None:
                return {
                    "status": False,
                    "message": "Username sudah digunakan"
                }, 400
            # CHECK USERNAME ======================================== Finish


            # CHECK EMAIL ======================================== Start
            email_check = Users.query.filter_by(
                email=email,
                is_delete=0
            ).first()

            if email_check is not None:
                return {
                    "status": False,
                    "message": "Email sudah digunakan"
                }, 400
            # CHECK EMAIL ======================================== Finish


            # CHECK PASSWORD ======================================== Start
            if password != confirm_password:
                return {
                    "status": False,
                    "message": "Konfirmasi password tidak sesuai"
                }, 400
            # CHECK PASSWORD ======================================== Finish


            timestamp = int(time.time())


            # INSERT USER ======================================== Start
            user = Users(
                username=username,
                email=email,
                password=generate_password_hash(password),
                role=1,
                is_active=1,
                created_at=timestamp,
                updated_at=timestamp
            )

            db.session.add(user)
            db.session.flush()
            # INSERT USER ======================================== Finish


            # INSERT WORKSHOP ======================================== Start
            workshop = Workshops(
                owner_id=user.id,
                parent_id=0,
                workshop_name=workshop_name,
                workshop_address=workshop_address,
                workshop_phone=workshop_phone,
                is_active=1,
                created_at=timestamp,
                updated_at=timestamp
            )

            db.session.add(workshop)
            # INSERT WORKSHOP ======================================== Finish


            db.session.commit()


            return {
                "status": True,
                "message": "Register berhasil"
            }

        except Exception as e:

            db.session.rollback()
            import traceback
            traceback.print_exc()

            return {
                "status": False,
                "message": str(e)
            }, 500

    # SIGNUP ============================================================ End
# SIGNUP MODEL ============================================================ End