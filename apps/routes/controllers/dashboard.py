from flask import Blueprint, request, redirect, url_for, render_template, session
from flask import current_app as app
from flask_jwt_extended import jwt_required

from ..models.signin import SigninModels
from ...utilities.forms import SigninForm


# BLUEPRINT ================================================== Begin
dashboard = Blueprint(
    name='dashboard',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/dashboard',
)
# BLUEPRINT ================================================== End

# DASHBOARD PAGE ============================================================ Begin
# GET https://127.0.0.1:5000/dashboard/
@dashboard.get('/')
def index():
    try:
        # Return Page ======================================== 
        # return redirect(url_for('dashboard'))
        if 'user_id' not in session:
    
            return redirect(
                url_for('auth.signin_page')
            )

        return render_template(
            title='Dashboard POS Bengkel',
            template_name_or_list='dashboard.html',
            username=session.get('username')
        )

    except Exception as e:
        # return bad_request(str(e))
        # return "gagal boss! Durung dadi:)"
        return render_template(
            title="Error $04 - Aplikasi e Hel",
            template_name_or_list='errorPages/404.html'
        )
# SIGNIN PAGE ============================================================ End
