import time

from apps import db
from apps.database.db_workshops import Workshops
from apps.utilities.responseHelpers import *
from apps.utilities.validators import role_validator, workshop_validator


# WORKSHOP MODEL CLASS ============================================================ Begin
class WorkshopModels():
    # ADD WORKSHOP ============================================================ Begin
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
            timestamp = int(round(time.time()*1000))
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
            return success(status_code=200)
        
        except Exception as e:
            print("WORKSHOP ERROR:", e)
            return bad_request(str(e))
    # ADD WORKSHOP ============================================================ End
    
    # GET WORKSHOP ============================================================ Begin
    def view_workshop():
        try:
            workshop = Workshops.query.filter_by(
                owner_id=session["user_id"],
                is_delete=0
            ).first()

            return workshop

        except Exception as e:
            return bad_request(str(e))
    # GET WORKSHOP ============================================================ End


    # UPDATE WORKSHOP ============================================================ Begin
    def edit_workshop(datas, logo):
        try:
            workshop = Workshops.query.filter_by(
                owner_id=session["user_id"],
                is_delete=0
            ).first()

            if workshop is None:
                return {
                    "status": False,
                    "message": "Profil bengkel tidak ditemukan"
                }

            workshop.workshop_name = datas["workshop_name"]
            workshop.workshop_phone = datas["workshop_phone"]
            workshop.workshop_address = datas["workshop_address"]
            workshop.workshop_email = datas["workshop_email"]
            workshop.is_active = datas["is_active"]

            # Upload Logo
            if logo and logo.filename != "":

                filename = secure_filename(logo.filename)
                ext = os.path.splitext(filename)[1]
                new_filename = f"{uuid.uuid4().hex}{ext}"

                upload_folder = os.path.join(
                    "apps",
                    "static",
                    "uploads",
                    "workshops"
                )

                os.makedirs(upload_folder, exist_ok=True)

                logo.save(
                    os.path.join(upload_folder, new_filename)
                )

                workshop.logo = f"images/profiles/{new_filename}"

            workshop.updated_at = int(time.time())

            db.session.commit()

            return {
                "status": True,
                "message": "Profil bengkel berhasil diupdate"
            }

        except Exception as e:
            return bad_request(str(e))
    # UPDATE WORKSHOP ============================================================ End

# WORKSHOP MODEL CLASS ============================================================ End