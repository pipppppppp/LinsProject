import time, json

from apps import db
from apps.database.db_users import Users
from apps.database.db_workshops import Workshops
from apps.utilities.responseHelpers import *
from apps.utilities.validators import role_validator, workshop_validator


# CATEGORY MODEL CLASS ============================================================ Begin
class WorkshopModels():
    # ADD CATEGORY ============================================================ Begin
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
                    return parameter_error(f"Missing {req} in Request Body.")
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
            timestamp = int(round(time.time()*1000))
            data = Workshops(
                workshop_name=workshop_name,
                workshop_address=workshop_address,
                workshop_phone=workshop_phone,
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
            return success(statusCode=201)
        
        except Exception as e:
            return bad_request(str(e))
    # ADD CATEGORY ============================================================ End

    # # GET ALL CATEGORY ============================================================ Begin
    # # Clear
    # def view_category():
    #     try:
    #         # Checking Data ---------------------------------------- Start
    #         query = CTGR_GET_ALL_QUERY
    #         result = DBHelper().execute(query)
    #         if len(result) < 1 or result is None:
    #             return not_found("Data kategori tidak dapat ditemukan.")
    #         # Checking Data ---------------------------------------- Finish
            
    #         # Response Data ---------------------------------------- Start
    #         response = []
    #         for rsl in result:
    #             createdAt = split_date_time(datetime.fromtimestamp(rsl['created_at']/1000))
    #             data = {
    #                 "category_id" : rsl["id"],
    #                 "category" : rsl["category"],
    #                 "format_data" : json.loads(rsl["format_data"]),
    #                 "created_at": createdAt
    #             }
    #             response.append(data)
    #         # Response Data ---------------------------------------- Finish
            
    #         # Return Response ======================================== 
    #         return success_data(response)
        
    #     except Exception as e:
    #         return bad_request(str(e))
    # # GET ALL CATEGORY ============================================================ End

    # # UPDATE CATEGORY ============================================================ Begin
    # # Clear
    # def edit_category(user_id, user_role, datas):
    #     try:
    #         # Access Validation ---------------------------------------- Start
    #         access = vld_role(user_role)
    #         if not access: # Access = True -> Admin
    #             return authorization_error()
    #         # Access Validation ---------------------------------------- Finish

    #         # Checking Request Body ---------------------------------------- Start
    #         if datas == None:
    #             return invalid_params()
            
    #         requiredData = ["category_id", "category", "format_data"]
    #         for req in requiredData:
    #             if req not in datas:
    #                 return parameter_error(f"Missing {req} in Request Body.")
    #         # Checking Request Body ---------------------------------------- Finish
            
    #         # Initialize Data Input ---------------------------------------- Start
    #         catgId = datas["category_id"]
    #         category = datas["category"].strip()
    #         formatData = datas["format_data"]
    #         # Initialize Data Input ---------------------------------------- Finish

    #         # Data Validation ---------------------------------------- Start
    #         query = CTGR_GET_BY_ID_QUERY
    #         values = (catgId,)
    #         result = DBHelper().get_data(query, values)
    #         if len(result) < 1 :
    #             return not_found(f"Data kategori dengan id {catgId} tidak dapat ditemukan.")
            
    #         ctgrCheck = vld_category(category, formatData, False)
    #         if len(ctgrCheck) != 0:
    #             return defined_error(ctgrCheck, "Bad Request", 400)
    #         # Data Validation ---------------------------------------- Finish
            
    #         # Update Data ---------------------------------------- Start
    #         formatData = json.dumps(formatData)
    #         timestamp = int(round(time.time()*1000))
    #         query = CTGR_UPDATE_QUERY
    #         values = (category, formatData, timestamp, user_id, catgId)
    #         DBHelper().save_data(query, values)
    #         # Update Data ---------------------------------------- Finish

    #         # Log Activity Record ---------------------------------------- Start
    #         activity = f"Admin dengan id {user_id} mengubah kategori {result[0]['category']} menjadi {category}."
    #         query = LOG_ADD_QUERY
    #         values = (user_id, 1, activity, timestamp, )
    #         DBHelper().save_data(query, values)
    #         # Log Activity Record ---------------------------------------- Finish

    #         # Return Response ======================================== 
    #         return success(message="Updated!")
            
    #     except Exception as e:
    #         return bad_request(str(e))
    # # UPDATE CATEGORY ============================================================ End

    # # DELETE CATEGORY ============================================================ Begin
    # # Clear
    # def delete_category(user_id, user_role, datas):
    #     try:
    #         # Access Validation ---------------------------------------- Start
    #         access = vld_role(user_role)
    #         if not access: # Access = True -> Admin
    #             return authorization_error()
    #         # Access Validation ---------------------------------------- Finish

    #         # Checking Request Body ---------------------------------------- Start
    #         if datas == None:
    #             return invalid_params()
            
    #         if "category_id" not in datas:
    #             return parameter_error("Missing 'category_id' in Request Body.")
            
    #         catgId = datas["category_id"]
    #         if catgId == "":
    #             return defined_error("Id kategori tidak boleh kosong.", "Defined Error", 499)
    #         # Checking Request Body ---------------------------------------- Finish
            
    #         # Checking Data ---------------------------------------- Finish
    #         query = CTGR_GET_BY_ID_QUERY
    #         values = (catgId,)
    #         result = DBHelper().get_count_filter_data(query, values)
    #         if result < 1 or result is None:
    #             return not_found(f"Kategori dengan Id {catgId} tidak dapat ditemukan.")
    #         # Checking Data ---------------------------------------- Finish
            
    #         # Delete Data ---------------------------------------- Start
    #         timestamp = int(round(time.time()*1000))
    #         query = CTGR_DELETE_QUERY
    #         values = (timestamp, user_id, catgId)
    #         DBHelper().save_data(query, values)
    #         # Delete Data ---------------------------------------- Finish
            
    #         # Delete Join Data ---------------------------------------- Start
    #         # Template
    #         query = TMPLT_GET_BY_CAT_QUERY
    #         values = (catgId,)
    #         template = DBHelper().get_data(query, values)
    #         invitation = []
    #         if len(template) > 0 :
    #             query = TMPLT_DELETE_CAT_QUERY
    #             values = (timestamp, user_id, catgId, )
    #             DBHelper().save_data(query, values)
    #             print("masuk")
    #             for temp in template:
    #                 # Invitation
    #                 print(temp)
    #                 query = INV_GET_BY_TEMP_QUERY
    #                 values = (temp['id'],)
    #                 invitation = DBHelper().get_data(query, values)
    #                 print(invitation)
    #                 if len(invitation) > 0:
    #                     query = INV_DELETE_TEMP_QUERY
    #                     values = (timestamp, user_id, temp['id'],)
    #                     DBHelper().save_data(query, values)

    #         if len(invitation) > 0:
    #             print("masuk 2")
    #             for inv in invitation:
    #                 # Guest
    #                 query = GUEST_GET_BY_CODE_QUERY
    #                 values = (inv['code'], )
    #                 guest = DBHelper().get_count_filter_data(query, values)
    #                 print(guest)
    #                 if guest > 0:
    #                     query = GUEST_DELETE_INV_QUERY
    #                     values = (timestamp, user_id, inv['code'], )
    #                     DBHelper().save_data(query, values)

    #                 # Greeting
    #                 query = GRTG_GET_BY_CODE_QUERY
    #                 values = (inv['code'], )
    #                 greeting = DBHelper().get_count_filter_data(query, values)
    #                 print(greeting)
    #                 if greeting > 0:
    #                     query = GRTG_DELETE_INV_QUERY
    #                     values = (timestamp, user_id, inv['code'], )
    #                     DBHelper().save_data(query, values)
            
    #         # Request
    #         query = REQ_GET_BY_CAT_QUERY
    #         values = (catgId, )
    #         reqtem = DBHelper().get_count_filter_data(query, values)
    #         if reqtem > 0:
    #             query = REQ_DELETE_CAT_QUERY
    #             values = (timestamp, user_id, catgId, )
    #             DBHelper().save_data(query, values)
    #         # Delete Join Data ---------------------------------------- Finish

    #         # Log Activity Record ---------------------------------------- Start
    #         activity = f"Admin dengan id {user_id} menghapus kategori {catgId}."
    #         query = LOG_ADD_QUERY
    #         values = (user_id, 1, activity, timestamp, )
    #         # DBHelper().save_data(query, values)
    #         # Log Activity Record ---------------------------------------- Finish

    #         # Return Response ======================================== 
    #         return success(message="Deleted!")
            
    #     except Exception as e:
    #         return bad_request(str(e))
    # # DELETE CATEGORY ============================================================ End

    # # GET DETAIL CATEGORY ============================================================ Begin
    # # Clear
    # def view_detail_category(datas):
    #     try:
    #         # Checking Request Body ---------------------------------------- Start
    #         if datas == None:
    #             return invalid_params()
            
    #         if "category_id" not in datas:
    #             return parameter_error("Missing 'category_id' in Request Body.")
            
    #         catgId = datas["category_id"]
    #         if catgId == "":
    #             return defined_error("Id kategori tidak boleh kosong.", "Defined Error", 400)
    #         # Checking Request Body ---------------------------------------- Finish
            
    #         # Checking Data ---------------------------------------- Start
    #         query = CTGR_GET_BY_ID_QUERY
    #         values = (catgId,)
    #         result = DBHelper().get_data(query, values)
    #         if len(result) < 1 :
    #             return not_found(f"Data kategori dengan Id {catgId} tidak dapat ditemukan.")
    #         # Checking Data ---------------------------------------- Finish
            
    #         # Response Data ---------------------------------------- Start
    #         response = {
    #             "category_id" : result[0]["id"],
    #             "category" : result[0]["category"],
    #             "format_data" : json.loads(result[0]["format_data"]),
    #             "created_at": split_date_time(datetime.fromtimestamp(result[0]["created_at"]/1000))
    #         }
    #         # Response Data ---------------------------------------- Finish

    #         # Return Response ======================================== 
    #         return success_data(response)
        
    #     except Exception as e:
    #         return bad_request(str(e))
    # # GET DETAIL CATEGORY ============================================================ End

    # # GET ROW-COUNT CATEGORY ============================================================ Begin
    # # Clear
    # def get_count_category():
    #     try:
    #         # Checking Data ---------------------------------------- Start
    #         query = CTGR_GET_ALL_QUERY
    #         result = DBHelper().get_count_data(query)
    #         if result < 1 or result is None :
    #             return not_found("Data kategori tidak dapat ditemukan.")
    #         # Checking Data ---------------------------------------- Finish
            
    #         # Response Data ---------------------------------------- Start
    #         response = {
    #             "category_count" : result
    #         }
    #         # Response Data ---------------------------------------- Finish

    #         # Return Response ======================================== 
    #         return success_data(response)
        
    #     except Exception as e:
    #         return bad_request(str(e))
    # # GET ROW-COUNT CATEGORY ============================================================ End
# CATEGORY MODEL CLASS ============================================================ End