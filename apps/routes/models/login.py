from flask_jwt_extended import create_access_token
from flask import request


import time

# BLOCK FIRST/BASE ============================================================ Begin
class LoginModels():
    # CREATE ADMIN ============================================================ Begin
    # Clear
    def create_admin(datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["username", "email", "password", "retype_password"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish
            
            # Initialize Data Input ---------------------------------------- Start
            username = datas["username"].strip()
            email = datas["email"].strip()
            password = datas["password"].strip()
            retypePassword = datas["retype_password"].strip()
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checkResult = vld_admin_regis(username, email, password, retypePassword)
            if len(checkResult) != 0:
                return defined_error(checkResult, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            passEncrypt = hashPassword(password)
            timestamp = int(round(time.time()*1000))
            query = ADM_ADD_QUERY
            values = (username, email, passEncrypt, timestamp, timestamp, timestamp)
            resReturn = 1
            resReturn = DBHelper().save_return(query, values)
            if resReturn is None:
                return defined_error("Gagal menyimpan data.", "Bad Request", 400)
            # Insert Data ---------------------------------------- Finish

            # Insert Profile ---------------------------------------- Start
            try:
                data = {
                    "user_id": resReturn,
                    "level": 1, # 1 = Admin, 2 = User
                    "first_name": username, 
                    "middle_name": "", 
                    "last_name": "", 
                    "phone": "0"
                }
                profile = ProfileModels.create_profile(data)
            except Exception as e:
                return bad_request(str(e))
            # Insert Profile ---------------------------------------- Finish
            
            # Log Activity Record ---------------------------------------- Start
            if profile.status_code == 200:
                activity = f"Admin baru dengan id {resReturn} telah berhasil mendafftar."
                query = LOG_ADD_QUERY
                values = (resReturn, 1, activity, timestamp, )
                DBHelper().save_data(query, values)
            else:
                query = ADM_DELETE_QUERY
                values = (timestamp, resReturn, )
                DBHelper().save_data(query, values)
                
                return bad_request("Gagal membuat akun.")
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(statusCode=201)

        except Exception as e:
            return bad_request(str(e))
    # CREATE ADMIN ============================================================ End

    # # SIGN IN ============================================================ Begin
    # # Clear
    # def signin_admin(datas):
    #     try:
    #         # Checking Request Body ---------------------------------------- Start
    #         if datas == None:
    #             return invalid_params()
            
    #         requiredData = ["email", "password"]
    #         for req in requiredData:
    #             if req not in datas:
    #                 return parameter_error(f"Missing {req} in Request Body.")
    #         # Checking Request Body ---------------------------------------- Finish
            
    #         # Initialize Data Request ---------------------------------------- Start
    #         email = datas["email"].strip().lower()
    #         password = datas["password"].strip()
    #         # Initialize Data Request ---------------------------------------- Finish
            
    #         # Data Validation ---------------------------------------- Start
    #         level = 1
    #         checkResult, result, stts = vld_signin(email, password, level)
    #         if len(checkResult) != 0:
    #             return defined_error(checkResult, "Bad Request", statusCode=stts)
    #         # Data Validation ---------------------------------------- Finish

    #         # Update Data Last Active ---------------------------------------- Start
    #         timestamp = int(round(time.time()*1000))
    #         query = ADM_UPDATE_ACTIVE_QUERY
    #         values = (timestamp, result[0]["id"])
    #         DBHelper().save_data(query, values)
    #         # Update Data Last Active ---------------------------------------- Finish
            
    #         # Log Activity Record ---------------------------------------- Start
    #         activity = f"Admin dengan id {result[0]['id']} telah berhasil log in."
    #         query = LOG_ADD_QUERY
    #         values = (result[0]["id"], level, activity, timestamp, )
    #         DBHelper().save_data(query, values)
    #         # Log Activity Record ---------------------------------------- Finish

    #         # Generate File URL ---------------------------------------- Start
    #         if len(result) >= 1:
    #             detailRequestURL = str(request.url).find('?')
    #             if detailRequestURL != -1:
    #                 index = detailRequestURL
    #                 request.url = request.url[:index]
    #         for item in result:
    #             item["photos"] = f"{request.url_root}admin/media/{item['photos']}"
    #         # Generate File URL ---------------------------------------- Finish
            
    #         # Data Payload ---------------------------------------- Start
    #         jwt_payload = {
    #             "id" : result[0]["id"],
    #             "email" : email,
    #             "name" : result[0]["username"],
    #             "photos" : result[0]["photos"],
    #             "role" : "ADMIN"
    #         }
    #         # Data Payload ---------------------------------------- Finish
            
    #         # Access Token by Email ======================================== 
    #         access_token = create_access_token(email, additional_claims=jwt_payload)
            
    #         # Data Response ---------------------------------------- Start
    #         response = {
    #             "access_token" : access_token,
    #             "role" : "ADMIN"
    #         }
    #         # Data Response ---------------------------------------- Finish
            
    #         # Return Response ======================================== 
    #         return success_data(response)

    #     except Exception as e:
    #         return bad_request(str(e))
    # # SIGN IN ============================================================ End
# BLOCK FIRST/BASE ============================================================ End
