from flask import Blueprint, request, render_template, session, redirect, url_for
import time

from ..models.category import CategoryModels

# BLUEPRINT ================================================== Begin
category = Blueprint(
    name='category',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/category',
)
# BLUEPRINT ================================================== End


# CATEGORY PAGE ============================================================ Begin
# GET https://127.0.0.1:5000/category/
@category.get('/')
@jwt_required()
def index():
    try:
        # Role Validation ======================================== 
        if session.get('role') != 'admin':
            return redirect(url_for('dashboard.index'))

        # Return Page ======================================== 
        return render_template(
            title='Kategori - POS Bengkel',
            template_name_or_list='category.html',
            active_menu="category",
        )

    except Exception as e:
        return render_template(
            title="Error 404 - POS Bengkel",
            template_name_or_list='errorPages/404.html'
        )
# CATEGORY PAGE ============================================================ End


# ADD CATEGORY DATA ============================================================ Begin
# POST https://127.0.0.1:5000/category/add
@category.post('/add')
def createCategory():
    try:
        # Request Data ========================================
        body = request.json

        # Request Process ======================================== 
        response = CategoryModels.add_category(body)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return render_template(
            title="Error $04 - Aplikasi e Hel",
            template_name_or_list='errorPages/404.html'
        )
# ADD CATEGORY DATA ============================================================ End


# ADD CATEGORY DATA ============================================================ Begin
# POST https://127.0.0.1:5000/category/view
@category.get('/view')
def getCategory():
    try:
        # Request Process ======================================== 
        response = CategoryModels.view_category()

        # Request Data ======================================== 
        return response

    except Exception as e:
        return render_template(
            title="Error $04 - Aplikasi e Hel",
            template_name_or_list='errorPages/404.html'
        )
# ADD CATEGORY DATA ============================================================ End


# UPDATE CATEGORY DATA ============================================================ Begin
# PUT https://127.0.0.1:5000/category/edit
@category.put('/edit/<int:id>')
def updateCategory(id):
    try:
        # Request Data ========================================
        body = request.json

        # Request Process ======================================== 
        response = CategoryModels.edit_category(body, id)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return render_template(
            title="Error $04 - Aplikasi e Hel",
            template_name_or_list='errorPages/404.html'
        )
# UPDATE CATEGORY DATA ============================================================ End


# DELETE CATEGORY DATA ============================================================ Begin
# DELETE https://127.0.0.1:5000/category/delete
@category.delete('/delete/<int:id>')
def deleteCategory(id):
    try:
        # Request Process ======================================== 
        response = CategoryModels.delete_category(id)

        # Request Data ======================================== 
        return response
        
    except Exception as e:
        return {
            "status": False,
            "message": str(e)
        }, 500
# DELETE CATEGORY DATA ============================================================ End
