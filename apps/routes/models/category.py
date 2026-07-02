from ... import db
from ...database.db_categories import Categories
from ...utilities.responseHelper import bad_request

import time

# CATEGORY MODEL CLASS ============================================================ Begin
class CategoryModels():
    # CREATE CATEGORY ============================================================ Begin
    def add_category(datas):
        try:
            # Insert Data ---------------------------------------- Start
            data = Categories(
                category=datas['category'],
                created_at=int(time.time()),
                updated_at=int(time.time())
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
            return "bad_request(str(e))"
    # CREATE CATEGORY ============================================================ End

    # GET ALL CATEGORY ============================================================ Begin
    def view_category():
        try:
            # Get Data ---------------------------------------- Start
            category = Categories.query.filter_by(
                is_delete=0
            ).all()
            # Get Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = []
            for rsl in category:
                data = {
                    "category_id" : rsl.id,
                    "category_name" : rsl.category,
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return response
        
        except Exception as e:
            return bad_request(str(e))
    # GET ALL CATEGORY ============================================================ End

    # UPDATE CATEGORY ============================================================ Begin
    def edit_category(datas, id):
        try:
            # Update Data ---------------------------------------- Start
            data = Categories.query.get_or_404(id)

            data.category = datas['category']
            data.updated_at = int(time.time())

            db.session.commit()
            # Update Data ---------------------------------------- Finish

            # Return Response ======================================== 
            # return success(message="Updated!")
            return {
                "status": True,
                "message": "Kategori berhasil diupdate"
            }
            
        except Exception as e:
            return "bad_request(str(e))"
    # UPDATE CATEGORY ============================================================ End

    # DELETE CATEGORY ============================================================ Begin
    def delete_category(id):
        try:
            # Delete Data ---------------------------------------- Start
            data = Categories.query.get_or_404(id)
            data.is_delete = 1
            data.deleted_at = int(time.time())

            db.session.commit()
            # Delete Data ---------------------------------------- Finish

            # Return Response ======================================== 
            # return success(message="Deleted!")
            return {
                "status": True,
                "message": "Kategori berhasil dihapus"
            }
            
        except Exception as e:
            return "bad_request(str(e))"
    # DELETE CATEGORY ============================================================ End

    # GET DETAIL CATEGORY ============================================================ Begin
    # GET DETAIL CATEGORY ============================================================ End

    # GET ROW-COUNT CATEGORY ============================================================ Begin
    # GET ROW-COUNT CATEGORY ============================================================ End
# CATEGORY MODEL CLASS ============================================================ End