from flask import Blueprint, request, redirect, url_for, render_template
from flask import current_app as app
from flask_jwt_extended import jwt_required

from ..models.signin import SigninModels
from ...utilities.forms import SigninForm


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
        return render_template(
            title='TITLE_DASHBD',
            template_name_or_list='category.html',
            # active='dashboard.index'
        )

    except Exception as e:
        # return bad_request(str(e))
        # return "gagal boss! Durung dadi:)"
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
        # Return Page ======================================== 
        # return redirect(url_for('dashboard'))
        print("okee")
        print(request.json)
        js = {"message": "iyaaa"}
        return js

    except Exception as e:
        # return bad_request(str(e))
        # return "gagal boss! Durung dadi:)"
        return render_template(
            title="Error $04 - Aplikasi e Hel",
            template_name_or_list='errorPages/404.html'
        )
# ADD CATEGORY DATA ============================================================ End
