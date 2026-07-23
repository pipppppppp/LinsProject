from datetime import datetime
import time
from sqlalchemy import func
from apps import db
from apps.database.db_users import Users
from apps.database.db_workshops import Workshops

from apps.utilities.responseHelpers import *
from apps.utilities.utilities import current_timestamp
from apps.utilities.validators import administrator_validator
from apps.utilities.formatter import format_date, format_datetime


# ADMINISTRATOR MODEL CLASS ============================================================ Begin
class AdministratorModels():

    # DASHBOARD ============================================================ Begin
    def dashboard(user_role):
        try:
             # Access Validation ---------------------------------------- Start
            access = administrator_validator(user_role)
            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Dashboard Data ---------------------------------------- Start
            total_workshop = Workshops.query.filter_by(
                is_delete=0
            ).count()

            active_workshop = Workshops.query.filter_by(
                is_delete=0,
                is_active=1
            ).count()

            inactive_workshop = Workshops.query.filter_by(
                is_delete=0,
                is_active=0
            ).count()

            # total_owner = Users.query.filter_by(
            #     role='1',
            #     is_delete=0
            # ).count()

            total_owner = db.session.query(
                func.count(func.distinct(Workshops.owner_id))
            ).filter(
                Workshops.is_delete == 0
            ).scalar()
            # Dashboard Data ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            response = {
                "total_workshop": total_workshop,
                "active_workshop": active_workshop,
                "inactive_workshop": inactive_workshop,
                "total_owner": total_owner
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ========================================
            return success_data(response)

        except Exception as e:
            return bad_request(str(e))
    # DASHBOARD ============================================================ End



    # VIEW WORKSHOP ============================================================ Begin
    def read_workshop(user_role, status):
        try:
            # Access Validation ---------------------------------------- Start
            access = administrator_validator(user_role)
            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Check Data ---------------------------------------- Start
            query = Workshops.query.filter_by(
                is_delete=0
            )
            status = status.strip().lower()
            
            if status == "pending":

                query = query.filter(
                    Workshops.is_verified == 0
                )

            elif status == "active":

                query = query.filter(
                    Workshops.is_verified == 1,
                    Workshops.is_active == 1
                )

            elif status == "inactive":

                query = query.filter(
                    Workshops.is_verified == 1,
                    Workshops.is_active == 0
                )
            result = query.order_by(
                Workshops.created_at.desc()
            ).all()       
            # if not result:
            #     return not_found("Workshop data could not be found.")
            # Check Data ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            response = []

            for workshop in result:

                owner = Users.query.filter_by(
                    id=workshop.owner_id,
                    is_delete=0
                ).first()

                created_at = format_datetime(workshop.created_at)

                data = {
                    "workshop_id": workshop.id,
                    "owner_id": workshop.owner_id,
                    "workshop_name": workshop.workshop_name,
                    "workshop_address": workshop.workshop_address,
                    "workshop_phone": workshop.workshop_phone,
                    "workshop_email": workshop.workshop_email,
                    "logo": workshop.logo,
                    "owner_name": owner.owner_name if owner else "-",
                    "owner_email": owner.email if owner else "-",
                    "account_status": owner.is_active if owner else 0,
                    "is_verified": workshop.is_verified,
                    "workshop_status": workshop.is_active,
                    "created_at": created_at
                }

                response.append(data)
            # Response Data ---------------------------------------- Finish

            # Return Response ========================================
            return success_data(response)

        except Exception as e:
            return bad_request(str(e))
    # VIEW WORKSHOP ============================================================ End

    # VERIFY WORKSHOP ============================================================ Begin
    def verify_workshop(user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = administrator_validator(user_role)
            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Check Request Body ---------------------------------------- Start
            if datas is None:
                return invalid_params()

            if "workshop_id" not in datas:
                return parameter_error("Missing workshop_id in request body.")
            # Check Request Body ---------------------------------------- Finish

            # Initialize Data ---------------------------------------- Start
            workshop_id = datas["workshop_id"]
            # Initialize Data ---------------------------------------- Finish

            # Check Data ---------------------------------------- Start
            workshop = Workshops.query.filter_by(
                id=workshop_id,
                is_delete=0
            ).first()

            if not workshop:
                return not_found("Workshop could not be found.")

            owner = Users.query.filter_by(
                id=workshop.owner_id,
                is_delete=0
            ).first()

            if not owner:
                return not_found("Owner could not be found.")

            if workshop.is_verified == 1:
                return success(message="Workshop already verified.")
            # Check Data ---------------------------------------- Finish

            # Update Data ---------------------------------------- Start
            timestamp = current_timestamp()

            workshop.is_verified = 1
            workshop.updated_at = timestamp

            owner.is_active = 1
            owner.updated_at = timestamp

            # Save Data
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Update Data ---------------------------------------- Finish

            # Return Response ========================================
            return success(message="Workshop has been verified successfully.")

        except Exception as e:
            return bad_request(str(e))
    # VERIFY WORKSHOP ============================================================ End

    # DETAIL WORKSHOP ============================================================ Begin
    def detail_workshop(role, workshop_id):

        # Role Checker ========================================
        access = administrator_validator(role)
        
        if not access:
            return authorization_error()
        
        # Query ========================================
        workshop = (
            db.session.query(
                Workshops,
                Users
            )
            .join(
                Users,
                Workshops.owner_id == Users.id
            )
            .filter(
                Workshops.id == workshop_id
            )
            .first()
        )

        # Data Not Found ========================================
        if workshop is None:
            return not_found("Workshop not found.")

        workshop_data, owner_data = workshop

        # Response ========================================
        return success_data({
            "workshop_id": workshop_data.id,
            "owner_id": owner_data.id,
            "workshop_name": workshop_data.workshop_name,
            "owner_name": owner_data.owner_name,
            "owner_email": owner_data.email,
            "workshop_phone": workshop_data.workshop_phone,
            "workshop_address": workshop_data.workshop_address,
            "logo": workshop_data.logo,
            "is_verified": workshop_data.is_verified,
            "workshop_status": workshop_data.is_active,
            "created_at": format_datetime(workshop_data.created_at)
        })

    # DETAIL WORKSHOP ============================================================ End

    # ACTIVATE WORKSHOP ============================================================ Begin
    def activate_workshop(user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = administrator_validator(user_role)
            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Check Request Body ---------------------------------------- Start
            if datas is None:
                return invalid_params()

            if "workshop_id" not in datas:
                return parameter_error("Missing workshop_id in request body.")
            # Check Request Body ---------------------------------------- Finish

            # Initialize Data ---------------------------------------- Start
            workshop_id = datas["workshop_id"]
            # Initialize Data ---------------------------------------- Finish

            # Check Data ---------------------------------------- Start
            workshop = Workshops.query.filter_by(
                id=workshop_id,
                is_delete=0
            ).first()

            if not workshop:
                return not_found("Workshop could not be found.")
            if not workshop.is_verified:
                return bad_request("Workshop has not been verified.")
            if workshop.is_active == 1:
                return success(message="Workshop already active.")
            # Check Data ---------------------------------------- Finish

            # Update Data ---------------------------------------- Start
            workshop.is_active = 1
            workshop.updated_at = current_timestamp()

            # Save Data
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Update Data ---------------------------------------- Finish

            # Return Response ========================================
            return success(message="Workshop has been activated successfully.")

        except Exception as e:
            return bad_request(str(e))
    # ACTIVATE WORKSHOP ============================================================ End

    # DEACTIVATE WORKSHOP ============================================================ Begin
    def deactivate_workshop(user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = administrator_validator(user_role)
            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Check Request Body ---------------------------------------- Start
            if datas is None:
                return invalid_params()

            if "workshop_id" not in datas:
                return parameter_error("Missing workshop_id in request body.")
            # Check Request Body ---------------------------------------- Finish

            # Initialize Data ---------------------------------------- Start
            workshop_id = datas["workshop_id"]
            # Initialize Data ---------------------------------------- Finish

            # Check Data ---------------------------------------- Start
            workshop = Workshops.query.filter_by(
                id=workshop_id,
                is_delete=0
            ).first()

            if not workshop:
                return not_found("Workshop could not be found.")
            if workshop.is_active == 0:
                return success(message="Workshop already inactive.")
            # Check Data ---------------------------------------- Finish

            # Update Data ---------------------------------------- Start
            workshop.is_active = 0
            workshop.updated_at = current_timestamp()

            # Save Data
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Update Data ---------------------------------------- Finish

            # Return Response ========================================
            return success(message="Workshop has been deactivated successfully.")

        except Exception as e:
            return bad_request(str(e))
    # DEACTIVATE WORKSHOP ============================================================ End



    # DELETE WORKSHOP ============================================================ Begin
    def delete_workshop(user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = administrator_validator(user_role)
            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Check Request Body ---------------------------------------- Start
            if datas is None:
                return invalid_params()

            if "workshop_id" not in datas:
                return parameter_error("Missing workshop_id in request body.")
            # Check Request Body ---------------------------------------- Finish

            # Initialize Data ---------------------------------------- Start
            workshop_id = datas["workshop_id"]
            # Initialize Data ---------------------------------------- Finish

            # Check Data ---------------------------------------- Start
            workshop = Workshops.query.filter_by(
                id=workshop_id,
                is_delete=0
            ).first()

            if not workshop:
                return not_found("Workshop could not be found.")

            # owner = Users.query.filter_by(
            #     id=workshop.owner_id,
            #     is_delete=0
            # ).first()
            # Check Data ---------------------------------------- Finish

            # Delete Data ---------------------------------------- Start
            timestamp = current_timestamp()

            workshop.is_delete = 1
            workshop.deleted_at = timestamp

            # if owner:
            #     owner.is_delete = 1
            #     owner.deleted_at = timestamp
            # Delete Data ---------------------------------------- Finish

            # Save Data ---------------------------------------- Start
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Save Data ---------------------------------------- Finish

            # Return Response ========================================
            return success(message="Workshop has been deleted successfully.")

        except Exception as e:
            return bad_request(str(e))
    # DELETE WORKSHOP ============================================================ End
# ADMINISTRATOR MODEL CLASS ============================================================ End