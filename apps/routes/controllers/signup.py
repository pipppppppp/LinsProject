from flask import Blueprint, render_template, request

from ..models.signup import SignupModels
# from ...utilities.forms import RegisterForm


# BLUEPRINT ================================================== Begin
signup = Blueprint(
    name='signup',
    import_name=__name__,
    template_folder="../../templates/pages",
    url_prefix='/signup',
)
# BLUEPRINT ================================================== End

# REGISTER PAGE ============================================================ Begin
# GET http://127.0.0.1:5000/register/
@signup.get("/")
def index():
    try:

        return render_template(
            title="Register",
            template_name_or_list="authPages/register-page.html"
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