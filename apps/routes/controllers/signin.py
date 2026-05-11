from flask import Blueprint, request, redirect, url_for, render_template
from flask import current_app as app
from flask_jwt_extended import jwt_required

from ..models.signin import SigninModels
from ...utilities.forms import SigninForm


# BLUEPRINT ================================================== Begin
auth = Blueprint(
    name='auth',
    import_name=__name__,
    template_folder="../../templates/pages",
    url_prefix='/auth',
)
# BLUEPRINT ================================================== End

# SIGNIN PAGE ============================================================ Begin
# GET https://127.0.0.1:5000/auth/signin
@auth.get('/signin')
def signin_page():
    try:
        # Return Page ======================================== 
        return redirect(url_for('login'))

    except Exception as e:
        # return bad_request(str(e))
        # return "gagal boss! Durung dadi:)"
        return render_template(
            title="Error $04 - Aplikasi e Hel",
            template_name_or_list='errorPages/404.html'
        )
# SIGNIN PAGE ============================================================ End


# SIGNIN PROCESS ============================================================ Begin
# GET https://127.0.0.1:5000/auth/signin/account
@auth.post('/signin/account')
def signin_process():
    try:
        # Request Data ======================================== 
        datas = SigninForm()

        # Request Data ======================================== 
        response = SigninModels.signin(datas)

        # Request Data ======================================== 
        return response

    except Exception as e:
        # return bad_request(str(e))
        # return "gagal boss! Durung dadi:)"
        return render_template(
            title="Error $04 - Aplikasi e Hel",
            template_name_or_list='errorPages/404.html'
        )
# SIGNIN PROCESS ============================================================ End
