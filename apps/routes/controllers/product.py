from flask import Blueprint, request, render_template
import time

from ... import db
from ..models.product import view_product, add_product, edit_product, delete_product
from ..models.category import view_category
from ...utilities.responseHelper import bad_request

# BLUEPRINT ================================================== Begin
product = Blueprint(
    name='product',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/product',
)
# BLUEPRINT ================================================== End


# PRODUCT PAGE ============================================================ Begin
# GET https://127.0.0.1:5000/product/
@product.get('/')
def index():
    try:
        # Request Process ======================================== 
        products = view_product()
        categories = view_category()

        # Return Page ======================================== 
        return render_template(
            title='TITLE_DASHBD',
            template_name_or_list='stock.html',
            products=products,
            categories=categories,
        )

    except Exception as e:
        return render_template(
            title="Error $04 - Aplikasi e Hel",
            template_name_or_list='errorPages/404.html'
        )
# PRODUCT PAGE ============================================================ End


# PRODUCT PAGE ============================================================ Begin
# GET https://127.0.0.1:5000/product/view
@product.get('/view')
def getProduct():
    try:
        # Request Process ======================================== 
        response = view_product()
        # categories = view_category()

        # Return Page ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# PRODUCT PAGE ============================================================ End


# ADD PRODUCT DATA ============================================================ Begin
# POST https://127.0.0.1:5000/product/add
@product.post('/add')
def createProduct():
    try:
        # Request Data ========================================
        body = request.json

        # Request Process ======================================== 
        response = add_product(body)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# ADD PRODUCT DATA ============================================================ End


# UPDATE PRODUCT DATA ============================================================ Begin
# PUT https://127.0.0.1:5000/product/update
@product.put('/update/<int:id>')
def updateProduct(id):
    try:
        # Request Data ========================================
        body = request.json

        # Request Process ======================================== 
        response = edit_product(body, id)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# UPDATE PRODUCT DATA ============================================================ End


# DELETE PRODUCT DATA ============================================================ Begin
# DELETE https://127.0.0.1:5000/product/update
@product.delete('/delete/<int:id>')
def deleteProduct(id):
    try:
        # Request Process ======================================== 
        response = delete_product(id)

        # Request Data ======================================== 
        return response
        
    except Exception as e:
        return bad_request(str(e))
# DELETE PRODUCT DATA ============================================================ End
