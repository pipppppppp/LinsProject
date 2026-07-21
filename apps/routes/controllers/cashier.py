from flask import Blueprint, request, render_template
from flask_jwt_extended import jwt_required, get_jwt

from apps.utilities.responseHelpers import bad_request

from ..models.administrator import AdministratorModels


# BLUEPRINT ================================================== Begin
cashier = Blueprint(
    name='cashier',
    import_name=__name__,
    template_folder="../../templates/pages/adminPages",
    url_prefix='/cashier',
)
# BLUEPRINT ================================================== End


# DASHBOARD PAGE ============================================================ Begin
# GET http://127.0.0.1:5000/cashier/
@cashier.get('/dashboard')
@jwt_required()
def dashboard():
    try:
      role = str(get_jwt()["role"])

    #   response = AdministratorModels.dashboard(role)
      
      return render_template(
            title='Cashier - POS Bengkel',
            template_name_or_list='cashier.html',
            active_menu="cashier",
      )

    except Exception as e:
        return bad_request(str(e))
# DASHBOARD PAGE ============================================================ End
 