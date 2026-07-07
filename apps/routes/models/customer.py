from flask import session

from ... import db
from ...database.db_customer import Customers
from ...utilities.validators import CustomerValidator
from ...utilities.responseHelper import bad_request

import time

# CATEGORY MODEL CLASS ============================================================ Begin
class CustomerModels():
    # CREATE CATEGORY ============================================================ Begin
    def add_customer(datas):
        try:
            # Validation Data ---------------------------------------- Start
            validator = CustomerValidator().validate(datas, session["workshop_id"])
            if validator:
                return {
                    "status": False,
                    "message": validator
                }
            # Validation Data ---------------------------------------- Finish
            now = int(time.time())

            # Insert Data ---------------------------------------- Start
            data = Customers(
                workshop_id=session["workshop_id"],
                customer_name=datas["customer_name"],
                customer_address=datas["customer_address"],
                customer_phone=datas["customer_phone"],
                created_at=now,
                updated_at=now
            )

            db.session.add(data)
            db.session.commit()
            # Insert Data ---------------------------------------- Finish

            # Return Response ======================================== 
            # return success(statusCode=201)
            return {
                "status": True,
                "message": "Data berhasil ditambahkan"
            }
        
        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # CREATE CATEGORY ============================================================ End

    # GET ALL CATEGORY ============================================================ Begin
    def view_customer():
        try:
            # Get Data ---------------------------------------- Start
            customer = Customers.query.filter_by(
                workshop_id=session["workshop_id"],
                is_delete=0
            ).all()
            # Get Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = []
            for item in customer:
                data = {
                    "customer_id" : item.id,
                    "customer_name" : item.customer_name,
                    "customer_address" : item.customer_address,
                    "customer_phone" : item.customer_phone,
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return response
        
        except Exception as e:
            return bad_request(str(e))
    # GET ALL CATEGORY ============================================================ End

    # UPDATE CATEGORY ============================================================ Begin
    def edit_customer(datas, id):
        try:

            # Validation Data ---------------------------------------- Start
            validator = CustomerValidator().validate(datas, session["workshop_id"], is_create=False)
            if validator:
                return {
                    "status": False,
                    "message": validator
                }
            # Validation Data ---------------------------------------- Finish
            
            # Update Data ---------------------------------------- Start
            data = Customers.query.filter_by(
                id=id,
                workshop_id=session["workshop_id"],
                is_delete=0
            ).first()

            if data is None:
                return {
                    "status": False,
                    "message": "Customer/Member tidak ditemukan"
                }
            data.customer_name = datas["customer_name"]
            data.customer_address = datas["customer_address"]
            data.customer_phone = datas["customer_phone"]
            data.updated_at = int(time.time())

            db.session.commit()
            # Update Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return {
                "status": True,
                "message": "Data Member berhasil diupdate"
            }
            
        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # UPDATE CATEGORY ============================================================ End

    # DELETE CATEGORY ============================================================ Begin
    def delete_customer(id):
        try:
            # Delete Data ---------------------------------------- Start
            data = Customers.query.filter_by(
                id=id,
                workshop_id=session["workshop_id"],
                is_delete=0
            ).first()
            if data is None:
                return {
                    "status": False,
                    "message": "Customer/Member tidak ditemukan"
                }

            data.is_delete = 1
            data.deleted_at = int(time.time())

            db.session.commit()
            # Delete Data ---------------------------------------- Finish

            # Return Response ======================================== 
            # return success(message="Deleted!")
            return {
                "status": True,
                "message": "Data Member berhasil dihapus"
            }
            
        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # DELETE CATEGORY ============================================================ End

# CATEGORY MODEL CLASS ============================================================ End