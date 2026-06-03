from flask import Blueprint, request, redirect, url_for, render_template
from flask import current_app as app
from flask_jwt_extended import jwt_required

from ..models.signin import SigninModels
from ...utilities.forms import SigninForm
from ... import db
from ...database.db_categories import Categories
import time

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
def index():
    try:
        # Return Page ======================================== 
        # return redirect(url_for('dashboard'))
        categories = Categories.query.filter_by(
            is_delete=0
        ).all()

        return render_template(
            title='TITLE_DASHBD',
            template_name_or_list='category.html',
            categories=categories
            # active='dashboard.index'
        )

    except Exception as e:

        return render_template(
            title="Error $04 - Aplikasi e Hel",
            template_name_or_list='errorPages/404.html'
        )
# CATEGORY PAGE ============================================================ End


# ADD CATEGORY DATA ============================================================ Begin
# POST https://127.0.0.1:5000/category/add
@category.post('/add')
def createCategory():
    try:
        body = request.json

        data = Categories(
            category=body['category'],
            created_at=int(time.time()),
            updated_at=int(time.time())
        )

        db.session.add(data)
        db.session.commit()

        return {
            "status": True,
            "message": "Data berhasil ditambahkan"
        }

    except Exception as e:
        return render_template(
            title="Error $04 - Aplikasi e Hel",
            template_name_or_list='errorPages/404.html'
        )

# ADD CATEGORY DATA ============================================================ End

@category.put('/update/<int:id>')
def updateCategory(id):

    try:

        body = request.json

        data = Categories.query.get_or_404(id)

        data.category = body['category']
        data.updated_at = int(time.time())

        db.session.commit()

        return {
            "status": True,
            "message": "Kategori berhasil diupdate"
        }

    except Exception as e:
        return render_template(
            title="Error $04 - Aplikasi e Hel",
            template_name_or_list='errorPages/404.html'
        )

@category.delete('/delete/<int:id>')
def deleteCategory(id):

    try:

        data = Categories.query.get_or_404(id)

        data.is_delete = 1
        data.deleted_at = int(time.time())

        db.session.commit()

        return {
            "status": True,
            "message": "Kategori berhasil dihapus"
        }
        
    except Exception as e:
        return {
            "status": False,
            "message": str(e)
        }, 500