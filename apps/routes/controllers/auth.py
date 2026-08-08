from flask import Blueprint, request, redirect, url_for, render_template, session
from flask_jwt_extended import jwt_required, unset_jwt_cookies

from apps.routes.models.auth import AuthModels
from apps.utilities.responseHelpers import bad_request


# BLUEPRINT ================================================== Begin
auth = Blueprint(
    name='auth',
    import_name=__name__,
    template_folder="../../templates/pages/authPages",
    url_prefix='/auth',
)
# BLUEPRINT ================================================== End


# SIGNIN PAGE ============================================================ Begin
# GET https://127.0.0.1:5000/auth/signin [Done]
@auth.get('/signin')
def signin_page():
    try:
        # Return Page ======================================== 
        return render_template(
            title='Sign In - POS Bengkel',
            template_name_or_list='signin.html',
        )

    except Exception as e:
        return bad_request(str(e))
# SIGNIN PAGE ============================================================ End

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


# SIGNUP PAGE ============================================================ Begin
# GET https://127.0.0.1:5000/auth/signup
@auth.get('/signup')
def signup_page():
    try:
        # Return Page ======================================== 
        return render_template(
            title='Sign Up - POS Bengkel',
            template_name_or_list='signup.html',
        )

    except Exception as e:
        return bad_request(str(e))
# SIGNUP PAGE ============================================================ End


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


# VERIFY EMAIL ============================================================ Begin
# GET http://127.0.0.1:5000/auth/verify-email/<token>
@auth.get('/verify-email/<string:token>')
def verify_email(token):
    try:
        # Request Process ========================================
        response = AuthModels.verify_email(token)

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# VERIFY EMAIL ============================================================ End

# FORGOT PASSWORD PAGE ============================================================ Begin
@auth.get('/forgot-password')
def forgot_password_page():
    try:
        return render_template(
            title='Lupa Password - POS Bengkel',
            template_name_or_list='forgot_password.html',
        )

    except Exception as e:
        return bad_request(str(e))
# FORGOT PASSWORD PAGE ============================================================ End

# FORGOT PASSWORD ============================================================ Begin
# POST http://127.0.0.1:5000/auth/forgot-password
@auth.post('/forgot-password')
def forgot_password():
    try:
        # Request Data ========================================
        body = request.json

        # Request Process ========================================
        response = AuthModels.forgot_password(body)

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# FORGOT PASSWORD ============================================================ End

# RESET PASSWORD PAGE ============================================================ Begin
# GET http://127.0.0.1:5000/auth/reset-password/<token>
@auth.get('/reset-password/<string:token>')
def reset_password_page(token):
    try:
        return render_template(
            title='Reset Password - POS Bengkel',
            template_name_or_list='reset_password.html',
            token=token
        )

    except Exception as e:
        return bad_request(str(e))
# RESET PASSWORD PAGE ============================================================ End

# RESET PASSWORD ============================================================ Begin
# PUT http://127.0.0.1:5000/auth/reset-password/<token>
@auth.put('/reset-password/<string:token>')
def reset_password(token):
    try:
        # Request Data ========================================
        body = request.json

        # Request Process ========================================
        response = AuthModels.reset_password(
            token,
            body
        )

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# RESET PASSWORD ============================================================ End

# LOGOUT ============================================================ Begin
# POST https://127.0.0.1:5000/auth/signout [Done]
@auth.get('/signout')
@jwt_required()
def signout():
    try:
        session.clear()
        response = redirect(url_for('auth.signin_page'))
        unset_jwt_cookies(response)
        return response
    except Exception as e:
        return bad_request(str(e))
# LOGOUT ============================================================ End
