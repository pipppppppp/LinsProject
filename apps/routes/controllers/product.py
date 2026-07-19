from flask import Blueprint, request, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt

from apps.utilities.responseHelpers import bad_request

from ..models.product import ProductModels


# BLUEPRINT ================================================== Begin
product = Blueprint(
    name='product',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/product',
)
# BLUEPRINT ================================================== End


# PRODUCT PAGE ============================================================ Begin
# GET http://127.0.0.1:5000/product/
@product.get('/')
@jwt_required()
def index():
    try:
        # JWT Access Data ========================================
        # id = str(get_jwt()["id"])
        # role = str(get_jwt()["role"])

        # # Role Validation ========================================
        # if role != "admin":
        #     return redirect(url_for("dashboard.index"))

        # Return Page ========================================
        return render_template(
            title="Produk - POS Bengkel",
            template_name_or_list="product.html",
            active_menu="product",
        )

    except Exception:
        return render_template(
            title="Error 404 - POS Bengkel",
            template_name_or_list="errorPages/404.html"
        )
# PRODUCT PAGE ============================================================ End


# ADD PRODUCT DATA ============================================================ Begin
# POST http://127.0.0.1:5000/product/add
@product.post('/add')
@jwt_required()
def create_product():
    try:
        # JWT Access Data ========================================
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        # Request Data ========================================
        body = request.json

        # Request Process ========================================
        response = ProductModels.create_product(role, ws_id, body)

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# ADD PRODUCT DATA ============================================================ End


# VIEW PRODUCT DATA ============================================================ Begin
# GET http://127.0.0.1:5000/product/view
@product.get('/view')
@jwt_required()
def read_product():
    try:
        # JWT Access Data ========================================
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        # Request Process ========================================
        response = ProductModels.read_product(role, ws_id)

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# VIEW PRODUCT DATA ============================================================ End


# EDIT PRODUCT DATA ============================================================ Begin
# PUT http://127.0.0.1:5000/product/edit
@product.put('/edit')
@jwt_required()
def update_product():
    try:
        # JWT Access Data ========================================
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        # Request Data ========================================
        body = request.json
        product_id = body["id"]

        # Request Process ========================================
        response = ProductModels.update_product(role, ws_id, product_id, body)

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# EDIT PRODUCT DATA ============================================================ End


# DELETE PRODUCT DATA ============================================================ Begin
# DELETE http://127.0.0.1:5000/product/delete
@product.delete('/delete')
@jwt_required()
def delete_product():
    try:
        # JWT Access Data ========================================
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        # Request Data ========================================
        body = request.json
        product_id = body["product_id"]

        # Request Process ========================================
        response = ProductModels.delete_product(role, ws_id, product_id)

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE PRODUCT DATA ============================================================ End
