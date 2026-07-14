from flask import Blueprint, render_template, request

from ..models.signup import SignupModels
# from ...utilities.forms import RegisterForm


# BLUEPRINT ================================================== Begin
auth = Blueprint(
    name='auth',
    import_name=__name__,
    template_folder="../../templates/pages",
    url_prefix='/auth',
)
# BLUEPRINT ================================================== End

# REGISTER PAGE ============================================================ Begin
# GET http://127.0.0.1:5000/register/
@signup.get("/signup")
def signup_page():
    try:

        return render_template(
            title="Register",
            template_name_or_list="authPages/signup.html"
        )

    except Exception as e:

        return {
            "status": False,
            "message": str(e)
        }, 400
# REGISTER PAGE ============================================================ End

# REGISTER PROCESS ============================================================ Begin
# POST http://127.0.0.1:5000/register/account
@signup.post("/account")
def signup_process():

    try:

        # Request Data ========================================
        body = request.json

        # Request Process ========================================
        response = RegisterModels.register(body)

        # Return Response ========================================
        return response

    except Exception as e:

        return {
            "status": False,
            "message": str(e)
        }, 400

# REGISTER PROCESS ============================================================ End