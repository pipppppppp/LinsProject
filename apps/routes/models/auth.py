from flask_jwt_extended import create_access_token
import time

from apps import db
from apps.database.db_users import Users
from apps.routes.models.workshop import WorkshopModels
from apps.utilities.responseHelpers import *
from apps.utilities.utilities import hash_password
from apps.utilities.validators import signin_validator, signup_validator


# AUTH MODELS ============================================================ Begin
class AuthModels():
    # SIGB UP ============================================================ Begin
    def signup(datas):
        try:
            # Validation Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            required_data = ["username", "email", "password", "retype_password"]
            for req in required_data:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Validation Request Body ---------------------------------------- Finish
            
            # Initialize Data Input ---------------------------------------- Start
            username = datas["username"].strip()
            email = datas["email"].strip()
            password = datas["password"]
            retype_password = datas["retype_password"]
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checker_result = signup_validator(username, email, password, retype_password)
            if len(checker_result) != 0:
                return defined_error(checker_result, "Bad Request", statusCode=400)
            # Data Validation ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            password_encrypt = hash_password(password)
            timestamp = int(round(time.time()*1000))
            data = Users(
                username=username,
                email=email,
                password=password_encrypt,
                role='1',
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

            # Insert Workshop ---------------------------------------- Start
            user_data = Users.query.filter_by(email=email, is_delete=0).first()
            workshop_data = WorkshopModels.create_workshop(user_data.id, user_data.role, datas)
            if workshop_data.status_code != 200:
                user_data.is_delete = '1'
                user_data.deleted_at = int(time.time())

                db.session.commit()
                return workshop_data
            # Insert Workshop ---------------------------------------- Finish

            # Data Payload ---------------------------------------- Start
            jwt_payload = {
                "id" : user_data.id,
                "email" : user_data.email,
                "username" : user_data.username,
                "role" : user_data.role
            }
            # Data Payload ---------------------------------------- Finish
            
            # Access Token by Email ======================================== 
            access_token = create_access_token(email, additional_claims=jwt_payload)
            
            # Data Response ---------------------------------------- Start
            response = {
                "access_token" : access_token,
                "role" : user_data.role
            }
            # Data Response ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return success_data(response)

        except Exception as e:
            return bad_request(str(e))
    # SIGB UP ============================================================ End

    # SIGN IN ============================================================ Begin
    def signin(datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["usermail", "password"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish
            
            # Initialize Data Input ---------------------------------------- Start
            usermail = datas["usermail"].strip().lower()
            password = datas["password"].strip()
            # Initialize Data Input ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            checkResult, result, stts = signin_validator(usermail, password)
            if len(checkResult) > 0:
                return defined_error(checkResult, "Bad Request", statusCode=stts)
            print("Check here!")
            # Data Validation ---------------------------------------- Finish

            # Update Data Last Active ---------------------------------------- Start
            # Update Data Last Active ---------------------------------------- Finish
            
            # Log Activity Record ---------------------------------------- Start
            # Log Activity Record ---------------------------------------- Finish

            # Generate File URL ---------------------------------------- Start
            # Generate File URL ---------------------------------------- Finish
            
            # Data Payload ---------------------------------------- Start
            jwt_payload = {
                "id" : result.id,
                "email" : result.email,
                "name" : result.username,
                "role" : result.role
            }
            # Data Payload ---------------------------------------- Finish

            # Access Token by Email ======================================== 
            access_token = create_access_token(result.email, additional_claims=jwt_payload)

            # Data Response ---------------------------------------- Start
            response = {
                "access_token" : access_token,
                "role" : "USER"
            }
            # Data Response ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)

        except Exception as e:
            return bad_request(str(e))
    # SIGN IN ============================================================ End
    
#     # GET ALL USER ============================================================ Begin
#     def view_user(user_id, user_role):
#         try:
#             # Access Validation ---------------------------------------- Start
#             access = vld_role(user_role)
#             if not access: # Access = True -> Admin
#                 return authorization_error()
#             # Access Validation ---------------------------------------- Finish

#             # Get Data User ---------------------------------------- Start
#             query = USR_GET_ALL_QUERY
#             result = DBHelper().execute(query)
#             if len(result) < 1 or result is None:
#                 return not_found("Data user tidak dapat ditemukan.")
#             # Get Data User ---------------------------------------- Finish

#             # Get Data User ---------------------------------------- Start
#             query1 = INV_GET_BY_USR_QUERY
#             query2 = REQ_GET_BY_USER_QUERY
#             # Get Data User ---------------------------------------- Finish

#             # Response Data ---------------------------------------- Start
#             response = []
#             for rsl in result:
#                 print("=======================================")
#                 values = (rsl['id'], 2, )
#                 invitation = DBHelper().get_count_filter_data(query1, values)
#                 reqUser = DBHelper().get_count_filter_data(query2, values)
#                 lastActive = split_date_time(datetime.fromtimestamp(rsl["last_active"]/1000))
#                 data = {
#                     "user_id" : rsl["id"],
#                     "username" : rsl["username"],
#                     "invitation_count" : invitation,
#                     "request_count" : reqUser,
#                     "status" : "Active" if rsl["is_delete"] == 0 else "Blocked",                    
#                     "last_active": lastActive
#                 }
#                 response.append(data)
#             # Response Data ---------------------------------------- Finish
            
#             # Return Response ======================================== 
#             return success_data(response)
        
#         except Exception as e:
#             return bad_request(str(e))
#     # GET ALL USER ============================================================ End
    
#     # DELETE USER ============================================================ Begin
#     def activate_user(datas):
#         try:
#             print(datas)
#             # Checking Request Body ---------------------------------------- Start
#             if datas == None:
#                 return invalid_params()
            
#             requiredData = ["user_id", "user_level", "token"]
#             for req in requiredData:
#                 if req not in datas:
#                     return parameter_error(f"Missing {req} in Request Body.")
#             # Checking Request Body ---------------------------------------- Finish

#             # Initialize Data Input ---------------------------------------- Start
#             userId = datas["user_id"]
#             userLevel = datas["user_level"]
#             token = datas["token"]
#             # Initialize Data Input ---------------------------------------- Finish

#             # Checking Data ---------------------------------------- Start
#             query = USR_GET_BY_ID_QUERY
#             values = (userId,)
#             result = DBHelper().get_count_filter_data(query, values)
#             if result < 1:
#                 return not_found(f"Data user dengan id {userId} tidak dapat ditemukan.")
#             # Checking Data ---------------------------------------- Finish

#             # Delete Account ---------------------------------------- Start
#             query = USR_ACTIVATED_ACCOUNT_QUERY
#             values = (userId, )
#             DBHelper().save_data(query, values)
#             # Delete Account ---------------------------------------- Finish

#             # Return Response ======================================== 
#             return success(message="Activate!")
        
#         except Exception as e:
#             return bad_request(str(e))
#     # DELETE USER ============================================================ End
    
#     # DELETE USER ============================================================ Begin
#     def delete_user(user_id, user_role, datas):
#         try:
#             # # Access Validation ---------------------------------------- Start
#             # access = vld_role(user_role)
#             # if not access: # Access = True -> Admin
#             #     return authorization_error()
#             # # Access Validation ---------------------------------------- Finish

#             # Checking Request Body ---------------------------------------- Start
#             if datas == None:
#                 return invalid_params()
            
#             if "user_id" not in datas:
#                 return parameter_error("Missing 'user_id' in request body.")
            
#             usrId = datas["user_id"]
#             if usrId == "":
#                 return defined_error("Id user tidak boleh kosong.", "Defined Error", 499)
#             # Checking Request Body ---------------------------------------- Finish

#             # Checking Data ---------------------------------------- Start
#             query = USR_GET_BY_ID_QUERY
#             values = (user_id,)
#             result = DBHelper().get_count_filter_data(query, values)
#             if result < 1:
#                 return not_found(f"Data user dengan id {usrId} tidak dapat ditemukan.")
#             # Checking Data ---------------------------------------- Finish

#             # Delete Account ---------------------------------------- Start
#             timestamp = int(round(time.time()*1000))
#             query = USR_DELETE_QUERY
#             values = (timestamp, user_id, usrId)
#             DBHelper().save_data(query, values)
#             # Delete Account ---------------------------------------- Finish

#             # Delete Profile ---------------------------------------- Start
#             query = PROF_DELETE_QUERY
#             values = (timestamp, usrId)
#             DBHelper().save_data(query, values)
#             # Delete Profile ---------------------------------------- Finish

#             # Delete Invitation & Guest ---------------------------------------- Start
#             query = INV_GET_BY_USR_QUERY
#             values = (user_id, )
#             invitations = DBHelper().get_data(query, values)
#             if len(invitations) > 0:
#                 query1 = INV_DELETE_QUERY
#                 query2 = GUEST_GET_BY_CODE_QUERY
#                 query3 = GUEST_DELETE_INV_QUERY
#                 for invite in invitations:
#                     # Delete Invitation
#                     delValues1 = (timestamp, user_id, invite['id'], )
#                     DBHelper().save_data(query1, delValues1)

#                     # Delete Guest
#                     values = (invite['code'], )
#                     guest = DBHelper().get_count_filter_data(query2, values)
#                     if guest > 0:
#                         delValues2 = (timestamp, user_id, invite['code'], )
#                         DBHelper().save_data(query3, delValues2)
#             # Delete Invitation & Guest ---------------------------------------- Finish

#             # Delete Template Private ---------------------------------------- Start
#             query = TMPLT_GET_BY_USER_QUERY
#             values = (user_id, )
#             templates = DBHelper().get_count_filter_data(query, values)
#             if templates > 0:
#                 query = TMPLT_PRIV_DELETE_USER_QUERY
#                 values = (timestamp, user_id, user_id, )
#                 DBHelper().save_data(query, values)
#             # Delete Template Private ---------------------------------------- Finish
            
#             # Return Response ======================================== 
#             return success(message="Deleted!")
        
#         except Exception as e:
#             return bad_request(str(e))
#     # DELETE USER ============================================================ End
    
#     # GET ROW-COUNT USER ============================================================ Begin
#     def get_count_user():
#         try:
#             # Checking Data ---------------------------------------- Start
#             query = USR_GET_ALL_QUERY
#             result = DBHelper().get_count_data(query)
#             if result < 1 or result is None :
#                 return not_found("User tidak dapat ditemukan.")
#             # Checking Data ---------------------------------------- Finish
            
#             # Response Data ---------------------------------------- Start
#             response = {
#                 "user_count" : result
#             }
#             # Response Data ---------------------------------------- Finish

#             # Return Response ======================================== 
#             return success_data(response)
        
#         except Exception as e:
#             return bad_request(str(e))
#     # GET ROW-COUNT USER ============================================================ End
# AUTH MODELS ============================================================ End