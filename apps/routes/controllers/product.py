from flask import Blueprint, request, render_template

from ..models.product import ProductModels
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
        # Role Validation ======================================== 
        if session.get('role') != 'admin':
            return redirect(url_for('dashboard.index'))

        # Return Page ======================================== 
        return render_template(
            title='Produk - POS Bengkel',
            template_name_or_list='product.html',
        )

    except Exception as e:
        return render_template(
            title="Error 404 - POS Bengkel",
            template_name_or_list='errorPages/404.html'
        )
# PRODUCT PAGE ============================================================ End


# ADD PRODUCT DATA ============================================================ Begin
# POST https://127.0.0.1:5000/product/add
@product.post('/add')
def createProduct():
    try:
        # Request Data ========================================
        body = request.json

        # Request Process ======================================== 
        response = ProductModels.add_product(body)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# ADD PRODUCT DATA ============================================================ End


# GET PRODUCT DATA ============================================================ Begin
# GET https://127.0.0.1:5000/product/view
@product.get('/view')
def getProduct():
    try:
        # Request Process ======================================== 
        response = ProductModels.view_product()

        # Return Page ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET PRODUCT DATA ============================================================ End


# UPDATE PRODUCT DATA ============================================================ Begin
# PUT https://127.0.0.1:5000/product/edit
@product.put('/edit/<int:id>')
def updateProduct(id):
    try:
        # Request Data ========================================
        body = request.json

        # Request Process ======================================== 
        response = ProductModels.edit_product(body, id)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# UPDATE PRODUCT DATA ============================================================ End


# DELETE PRODUCT DATA ============================================================ Begin
# DELETE https://127.0.0.1:5000/product/delete
@product.delete('/delete/<int:id>')
def deleteProduct(id):
    try:
        # Request Process ======================================== 
        response = ProductModels.delete_product(id)

        # Request Data ======================================== 
        return response
        
    except Exception as e:
        return bad_request(str(e))
# DELETE PRODUCT DATA ============================================================ End
