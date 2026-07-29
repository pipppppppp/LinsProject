from apps import db
from apps.database.db_users import Users

from apps.utilities.responseHelpers import *
from apps.utilities.utilities import current_timestamp, hash_password
from apps.utilities.validators import owner_validator, owner_account_validator, owner_password_validator


# **************************************************************
# OWNER ACCOUNT MODEL | START
# **************************************************************
class OwnerAccountModels():

    # **************************************************************
    # READ OWNER ACCOUNT | START
    # **************************************************************
    def read_owner_account(user_role, user_id):
        try:
            # Access Validation ========================================
            access = owner_validator(user_role)

            if not access:
                return authorization_error()

            # User ID Validation ========================================
            if (
                user_id is None or
                not str(user_id).isdigit()
            ):
                return invalid_params()

            user_id = int(user_id)

            # Get Owner Account ========================================
            owner = Users.query.filter_by(
                id=user_id,
                role="1",
                is_delete="0"
            ).first()

            if not owner:
                return not_found(
                    "Akun owner tidak ditemukan."
                )

            # Response Data ========================================
            response = {
                "id": owner.id,
                "owner_name": owner.owner_name,
                "username": owner.username,
                "email": owner.email,
                "role": owner.role,
                "is_active": owner.is_active,
                "created_at": owner.created_at,
                "updated_at": owner.updated_at
            }

            return success_data(
                data=response,
                status_code=200
            )

        except Exception as e:
            return bad_request(str(e))
    # **************************************************************
    # READ OWNER ACCOUNT | END
    # **************************************************************


    # **************************************************************
    # UPDATE OWNER ACCOUNT | START
    # **************************************************************
    def update_owner_account(user_role, user_id, datas):
        try:
            # Access Validation ========================================
            access = owner_validator(user_role)

            if not access:
                return authorization_error()

            # User ID Validation ========================================
            if (
                user_id is None or
                not str(user_id).isdigit()
            ):
                return invalid_params()

            user_id = int(user_id)

            # Request Body Validation ========================================
            if datas is None:
                return invalid_params()

            required_data = [
                "owner_name",
                "username",
                "email"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )

            # Initialize Data ========================================
            owner_name = str(
                datas["owner_name"] or ""
            ).strip()

            username = str(
                datas["username"] or ""
            ).strip()

            email = str(
                datas["email"] or ""
            ).strip().lower()

            # Data Validation ---------------------------------------- Start
            checker_result = owner_account_validator(
                  user_id,
                  owner_name,
                  username,
                  email
            )

            if len(checker_result) != 0:
                  return defined_error(
                        checker_result,
                        "Defined Error",
                        499
                  )
            # Data Validation ---------------------------------------- Finish

            # Get Owner Account ========================================
            owner = Users.query.filter_by(
                  id=user_id,
                  role="1",
                  is_delete="0"
            ).first()

            if not owner:
                  return not_found(
                        "Akun owner tidak ditemukan."
                  )

            # Update Owner Account ========================================
            owner.owner_name = owner_name
            owner.username = username
            owner.email = email
            owner.updated_at = current_timestamp()

            try:
                db.session.commit()

            except Exception as e:
                db.session.rollback()

                return parameter_error(
                    str(e)
                )

            return success(
                message="Data akun berhasil diperbarui.",
                status_code=200
            )

        except Exception as e:
            db.session.rollback()

            return bad_request(str(e))
    # **************************************************************
    # UPDATE OWNER ACCOUNT | END
    # **************************************************************


    # **************************************************************
    # CHANGE OWNER PASSWORD | START
    # **************************************************************
    def change_owner_password(user_role, user_id, datas):
        try:
            # Access Validation ========================================
            access = owner_validator(user_role)

            if not access:
                return authorization_error()

            # User ID Validation ========================================
            if (
                user_id is None or
                not str(user_id).isdigit()
            ):
                return invalid_params()

            user_id = int(user_id)

            # Request Body Validation ========================================
            if datas is None:
                return invalid_params()

            required_data = [
                "old_password",
                "new_password",
                "confirm_password"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )

            # Initialize Data ========================================
            old_password = str(
                datas["old_password"] or ""
            )

            new_password = str(
                datas["new_password"] or ""
            )

            confirm_password = str(
                datas["confirm_password"] or ""
            )

            # Get Owner Account ========================================
            owner = Users.query.filter_by(
                id=user_id,
                role="1",
                is_delete="0"
            ).first()

            if not owner:
                return not_found(
                    "Akun owner tidak ditemukan."
                )

            # Password Validation ========================================
            
            # Data Validation ---------------------------------------- Start
            checker_result = owner_password_validator(
                  old_password,
                  new_password,
                  confirm_password,
                  owner.password
            )

            if len(checker_result) != 0:
                  return defined_error(
                        checker_result,
                        "Defined Error",
                        499
                  )
            # Data Validation ---------------------------------------- Finish

            # Update Password ========================================
            owner.password = hash_password(
                new_password
            )

            owner.updated_at = current_timestamp()

            try:
                db.session.commit()

            except Exception as e:
                db.session.rollback()

                return parameter_error(
                    str(e)
                )

            return success(
                message="Password berhasil diperbarui.",
                status_code=200
            )

        except Exception as e:
            db.session.rollback()

            return bad_request(str(e))
    # **************************************************************
    # CHANGE OWNER PASSWORD | END
    # **************************************************************


# **************************************************************
# OWNER ACCOUNT MODEL | END
# **************************************************************