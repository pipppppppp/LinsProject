from flask import Blueprint, request, redirect, url_for, render_template, session
from flask_jwt_extended import jwt_required

from apps.routes.models.auth import AuthModels
from apps.utilities.responseHelpers import bad_request


# BLUEPRINT ================================================== Begin
auth = Blueprint(
    name='auth',
    import_name=__name__,
    template_folder="../../templates/pages",
    url_prefix='/auth',
)
# BLUEPRINT ================================================== End


# SIGNUP PAGE ============================================================ Begin
# GET https://127.0.0.1:5000/auth/signup
@auth.get('/signup')
def signup_page():
    try:
        # Return Page ======================================== 
        return render_template(
            title='Sign Up - POS Bengkel',
            template_name_or_list='authPages/signup.html',
        )

    except Exception as e:
        return bad_request(str(e))
# SIGNUP PAGE ============================================================ End


# SIGNIN PAGE ============================================================ Begin
# GET https://127.0.0.1:5000/auth/signin [Done]
@auth.get('/signin')
def signin_page():
    try:
        # Return Page ======================================== 
        return render_template(
            title='Sign In - POS Bengkel',
            template_name_or_list='authPages/signin.html',
        )

    except Exception as e:
        return bad_request(str(e))
# SIGNIN PAGE ============================================================ End


# SIGNUP PROCESS ============================================================ Begin
# POST https://127.0.0.1:5000/auth/signup/account [Done]
@auth.post('/signup/account')
def signup_process():
    try:
        # Request Data ========================================
        body = request.json

        # Request Process ======================================== 
        response = AuthModels.signup(body)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# SIGNUP PROCESS ============================================================ End


# SIGNIN PROCESS ============================================================ Begin
# POST https://127.0.0.1:5000/auth/signin/account [Done]
@auth.post('/signin/account')
def signin_process():
    try:
        # Request Data ======================================== 
        body = request.json

        # Request Process ======================================== 
        response = AuthModels.signin(body)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# SIGNIN PROCESS ============================================================ End


# LOGOUT ============================================================ Begin
# POST https://127.0.0.1:5000/auth/signout [Done]
@auth.get('/signout')
@jwt_required
def signout():
    try:
        session.clear()

        return redirect(
            url_for('auth.signin_page')
        )
    except Exception as e:
        return bad_request(str(e))
# LOGOUT ============================================================ End