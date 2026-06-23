from ... import db
from ...database.db_items import Items
from ...database.db_categories import Categories
from ...utilities.responseHelper import success, bad_request

import time

# PRODUCT MODEL CLASS ============================================================ Begin
class ProductModels():
    # CREATE PRODUCT ============================================================ Begin
    def add_product(datas):
        try:
            # Insert Data ---------------------------------------- Start
            data = Items(
                category_id=datas['product_category'],
                nama_barang=datas['product_name'],
                stok=datas['product_stock'],
                harga_beli=datas['product_purchase'],
                harga_jual=datas['product_price'],
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
            return bad_request(str(e))
    # CREATE PRODUCT ============================================================ End

    # GET ALL PRODUCT ============================================================ Begin
    def view_product():
        try:
            # Get Data ---------------------------------------- Start
            products = Items.query.filter_by(is_delete=0).all()
            categories = Categories.query.filter_by(is_delete=0).all()
            # Get Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = []
            for item in products:
                data = {
                    "product_id" : item.id,
                    "product_name" : item.nama_barang,
                    "product_ctg_id" : [cat.id for cat in categories if cat.id == item.category_id],
                    "product_category" : [cat.category for cat in categories if cat.id == item.category_id],
                    "product_stock" : item.stok,
                    "product_purchase" : item.harga_jual,
                    "product_price" : item.harga_beli,
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return response
        
        except Exception as e:
            return bad_request(str(e))
    # GET ALL PRODUCT ============================================================ End

    # UPDATE PRODUCT ============================================================ Begin
    def edit_product(datas, id):
        try:
            # Update Data ---------------------------------------- Start
            data = Items.query.get_or_404(id)

            data.category_id = datas['product_category']
            data.nama_barang = datas['product_name']
            data.stok = datas['product_stock']
            data.harga_beli = datas['product_purchase']
            data.harga_jual = datas['product_price']
            data.updated_at = int(time.time())

            db.session.commit()
            # Update Data ---------------------------------------- Finish

            # Return Response ======================================== 
            # return success(message="Updated!")
            return {
                "status": True,
                "message": "Produk berhasil diupdate"
            }
            
        except Exception as e:
            return bad_request(str(e))
    # UPDATE PRODUCT ============================================================ End

    # DELETE PRODUCT ============================================================ Begin
    def delete_product(id):
        try:
            # Delete Data ---------------------------------------- Start
            data = Items.query.get_or_404(id)

            data.is_delete = 1
            data.deleted_at = int(time.time())

            db.session.commit()
            # Delete Data ---------------------------------------- Finish

            # Return Response ======================================== 
            # return success(message="Deleted!")
            return {
                "status": True,
                "message": "Produk berhasil dihapus"
            }
            
        except Exception as e:
            return bad_request(str(e))
    # DELETE PRODUCT ============================================================ End

    # GET DETAIL PRODUCT ============================================================ Begin
    # GET DETAIL PRODUCT ============================================================ End

    # GET ROW-COUNT PRODUCT ============================================================ Begin
    # GET ROW-COUNT PRODUCT ============================================================ End
# PRODUCT MODEL CLASS ============================================================ End