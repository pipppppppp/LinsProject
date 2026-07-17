from datetime import datetime
import time

from apps import db
from apps.database.db_categories import Categories
from apps.database.db_products import Products
from apps.database.db_users import Users
from apps.database.db_workshops import Workshops
from apps.utilities.responseHelpers import *
from apps.utilities.utilities import split_date_time
from apps.utilities.validators import role_validator, category_validator


# CATEGORY MODEL CLASS ============================================================ Begin
class CategoryModels():
    # ADD CATEGORY ============================================================ Begin
    def create_category(user_role, workshop_id, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)
            if not access: # Access = True -> Admin
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Check Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "category_name" not in datas:
                return parameter_error(f"Missing category in request body.")
            # Check Request Body ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            category = datas["category_name"].strip()
            checker_result = category_validator(category, workshop_id)
            if len(checker_result) != 0:
                return defined_error(checker_result, "Defined Error", 499)
            # Data Validation ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            # Get Workshop Data
            result = Workshops.query.filter_by(id=workshop_id, is_delete=0).first()

            # Initialize
            timestamp = int(round(time.time()*1000))
            data = Categories(
                workshop_id=result.id,
                category=category,
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

            # # Log Activity Record ---------------------------------------- Start
            # # Log Activity Record ---------------------------------------- Finish

            # # Return Response ======================================== 
            return success(status_code=200)
        
        except Exception as e:
            return bad_request(str(e))
    # ADD CATEGORY ============================================================ End

    # VIEW CATEGORY ============================================================ Begin
    def read_category(workshop_id):
        try:
            # Check Data ---------------------------------------- Start
            result = Categories.query.filter_by(workshop_id=workshop_id, is_delete=0).all()
            if not result:
                # return not_found("Data kategori tidak dapat ditemukan.")
                return not_found("Category data could not be found.")
            # Check Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = []
            for res in result:
                created_at = split_date_time(datetime.fromtimestamp(res.created_at/1000))
                data = {
                    "category_id" : res.id,
                    "workshop_id" : res.workshop_id,
                    "category_name" : res.category,
                    "created_at": created_at
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # VIEW CATEGORY ============================================================ End

    # EDIT CATEGORY ============================================================ Begin
    def update_category(user_role, workshop_id, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)
            if not access: # Access = True -> Admin
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Check Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            required_data = ["category_id", "category_name"]
            for req in required_data:
                if req not in datas:
                    return parameter_error(f"Missing {req} in request body.")
            # Check Request Body ---------------------------------------- Finish
            
            # Initialize Data Input ---------------------------------------- Start
            category_id = datas["category_id"]
            category = datas["category_name"].strip()
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            result = Categories.query.filter_by(id=category_id, workshop_id=workshop_id, is_delete=0).first()
            if not result :
                # return not_found(f"Data kategori dengan id {category_id} tidak dapat ditemukan.")
                return not_found(f"Category data with id {category_id} could not be found.")
            
            if result.category == category:
                return success(message="Successful!")
            
            checker_result = category_validator(category, workshop_id)
            if len(checker_result) != 0:
                return defined_error(checker_result, "Defined Error", 499)
            # Data Validation ---------------------------------------- Finish
            
            # Update Data ---------------------------------------- Start
            # Initialize
            result.category = datas['category_name']
            result.updated_at = int(round(time.time()*1000))

            # Save Data
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Update Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(message="Data has been updated!")
            
        except Exception as e:
            return bad_request(str(e))
    # EDIT CATEGORY ============================================================ End

    # DELETE CATEGORY ============================================================ Begin
    def delete_category(user_role, workshop_id, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)
            if not access: # Access = True -> Admin
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "category_id" not in datas:
                return parameter_error("Missing 'category_id' in request body.")
            
            category_id = datas["category_id"]
            if category_id == "":
                return defined_error("Category id cannot be empty.", "Defined Error", 499)
            # Checking Request Body ---------------------------------------- Finish
            
            # Check Data ---------------------------------------- Finish
            result = Categories.query.filter_by(id=category_id, workshop_id=workshop_id, is_delete=0).first()
            if not result:
                # return not_found(f"Kategori dengan Id {category_id} tidak dapat ditemukan.")
                return not_found(f"Category data with id {category_id} could not be found.")
            # Check Data ---------------------------------------- Finish
            
            # Delete Data ---------------------------------------- Start
            # Initialize
            timestamp = int(round(time.time()*1000))
            result.is_delete = 1
            result.deleted_at = timestamp

            # Save Data
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Delete Data ---------------------------------------- Finish
            
            # Delete Join Data ---------------------------------------- Start
            # Product
            product = Products.query.filter_by(category_id=category_id, workshop_id=workshop_id, is_delete=0).all()
            for item in product:
                item.is_delete = 1
                item.deleted_at = timestamp
            db.session.commit()
            # Delete Join Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(message="Data has been deleted!")
            
        except Exception as e:
            return bad_request(str(e))
    # DELETE CATEGORY ============================================================ End

    # VIEW CATEGORY ROW-COUNT ============================================================ Begin
    # VIEW CATEGORY ROW-COUNT ============================================================ End
# CATEGORY MODEL CLASS ============================================================ End