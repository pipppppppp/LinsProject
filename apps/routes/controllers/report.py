from flask import Blueprint, request, render_template
from flask_jwt_extended import jwt_required, get_jwt

from ..models import report as report_models
from ...utilities.responseHelpers import bad_request

# BLUEPRINT ================================================== Begin
report = Blueprint(
    name='report',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/report',
)
# BLUEPRINT ================================================== End

# CUSTOMER PAGE ============================================================ Begin
# [GET] https://127.0.0.1:5000/report/
@report.get('/')
@jwt_required()
def index_rpurchase():
    try:
        return render_template(
            title='Customer - POS Bengkel',
            template_name_or_list='report_purchase.html',
            active_menu="report",
        )
    except Exception as e:
        return bad_request(str(e))
# CUSTOMER PAGE ============================================================ End

# PURCHASE REPORT ============================================================ Begin
# [POST] https://127.0.0.1:5000/purchase/view
@report.post("/purchase/view")
@jwt_required()
def purchase_report():
    try:
        claims = get_jwt()

        user_role = claims["role"]
        workshop_id = claims["ws_id"]

        datas = request.get_json()

        return report_models.purchase_report(
            user_role,
            workshop_id,
            datas
        )

    except Exception as e:
        return bad_request(str(e))
# PURCHASE REPORT ============================================================ End

# EXPORT PURCHASE EXCEL ============================================================ Begin
@report.post("/purchase/export/excel")
@jwt_required()
def export_purchase_excel():
    try:
        claims = get_jwt()

        user_role = claims["role"]
        workshop_id = claims["ws_id"]

        datas = request.get_json()

        return report_models.export_purchase_excel(
            user_role,
            workshop_id,
            datas
        )

    except Exception as e:
        return bad_request(str(e))
# EXPORT PURCHASE EXCEL ============================================================ End

# EXPORT PURCHASE PDF ============================================================ Begin
@report.post("/purchase/export/pdf")
@jwt_required()
def export_purchase_pdf():
    try:
        claims = get_jwt()

        user_role = claims["role"]
        workshop_id = claims["ws_id"]

        datas = request.get_json()

        return report_models.export_purchase_pdf(
            user_role,
            workshop_id,
            datas
        )

    except Exception as e:
        return bad_request(str(e))
# EXPORT PURCHASE PDF ============================================================ End