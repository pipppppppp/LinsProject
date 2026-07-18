from flask import Blueprint, request, render_template, session, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt

import time

from apps.utilities.responseHelpers import bad_request

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
# GET http://127.0.0.1:5000/category/
@category.get('/')
@jwt_required()
def index():
    try:
        # # JWT Access Data ======================================== 
        # id = str(get_jwt()["id"])
        # role = str(get_jwt()["role"])

        # # Role Validation ======================================== 
        # if role != 'admin':
        #     return redirect(url_for('dashboard.index'))

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
# POST http://127.0.0.1:5000/category/add [Done]
@category.post('/add')
@jwt_required()
def create_category():
    try:
        # JWT Access Data ======================================== 
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        # Request Data ======================================== 
        body = request.json

        # Request Process ======================================== 
        response = CategoryModels.create_category(role, ws_id, body)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# ADD CATEGORY DATA ============================================================ End


# VIEW CATEGORY DATA ============================================================ Begin
# POST http://127.0.0.1:5000/category/view [Done]
@category.get('/view')
@jwt_required()
def read_category():
    try:
        # JWT Access Data ======================================== 
        ws_id = str(get_jwt()["ws_id"])

        # Request Process ======================================== 
        response = CategoryModels.read_category(ws_id)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# VIEW CATEGORY DATA ============================================================ End


# EDIT CATEGORY DATA ============================================================ Begin
# PUT http://127.0.0.1:5000/category/edit [Done]
@category.put('/edit')
@jwt_required()
def update_category():
    try:
        # JWT Access Data ======================================== 
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        # Request Data ========================================
        body = request.json

        # Request Process ======================================== 
        response = CategoryModels.update_category(role, ws_id, body)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# EDIT CATEGORY DATA ============================================================ End


# DELETE CATEGORY DATA ============================================================ Begin
# DELETE http://127.0.0.1:5000/category/delete [Done]
@category.delete('/delete')
@jwt_required()
def delete_category():
    try:
        # JWT Access Data ======================================== 
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        # Request Data ========================================
        body = request.json

        # Request Process ======================================== 
        response = CategoryModels.delete_category(role, ws_id, body)

        # Request Data ======================================== 
        return response
        
    except Exception as e:
        return bad_request(str(e))
# DELETE CATEGORY DATA ============================================================ End
