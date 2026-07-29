from flask import Blueprint, request, render_template
from flask_jwt_extended import jwt_required, get_jwt

from ..models.history_purchase import HistoryPurchaseModels
from ...utilities.responseHelpers import bad_request

# BLUEPRINT ================================================== Begin
history_purchase = Blueprint(
    name='history_purchase',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/history-purchase',
)
# BLUEPRINT ================================================== End

# HISTOERY PURCHASE PAGE OWNER============================================================ Begin
# [GET] https://127.0.0.1:5000/history_purchase/
@history_purchase.get('/')
@jwt_required()
def owner():
    try:
        return render_template(
            title='Riwayat Pembelian - POS Bengkel',
            template_name_or_list='report_purchase.html',
            active_menu="history_purchase",
        )
    except Exception as e:
        return bad_request(str(e))
# HISTORY PURCHASE PAGE  OWNER============================================================ End

# PURCHASE REPORT ============================================================ Begin
# [POST] https://127.0.0.1:5000/history_purchase/view
@history_purchase.post("/purchase/view")
@jwt_required()
def purchase_report():
    try:
        claims = get_jwt()

        user_role = claims["role"]
        workshop_id = claims["ws_id"]

        datas = request.get_json()

        return HistoryPurchaseModels.purchase_report(
            user_role,
            workshop_id,
            datas
        )

    except Exception as e:
        return bad_request(str(e))
# PURCHASE REPORT ============================================================ End

# EXPORT PURCHASE EXCEL ============================================================ Begin
@history_purchase.post("/purchase/export/excel")
@jwt_required()
def export_purchase_excel():
    try:
        claims = get_jwt()

        user_role = claims["role"]
        workshop_id = claims["ws_id"]

        datas = request.get_json()

        return HistoryPurchaseModels.export_purchase_excel(
            user_role,
            workshop_id,
            datas
        )

    except Exception as e:
        return bad_request(str(e))
# EXPORT PURCHASE EXCEL ============================================================ End

# EXPORT PURCHASE PDF ============================================================ Begin
@history_purchase.post("/purchase/export/pdf")
@jwt_required()
def export_purchase_pdf():
    try:
        claims = get_jwt()

        user_role = claims["role"]
        workshop_id = claims["ws_id"]

        datas = request.get_json()

        return HistoryPurchaseModels.export_purchase_pdf(
            user_role,
            workshop_id,
            datas
        )

    except Exception as e:
        return bad_request(str(e))
# EXPORT PURCHASE PDF ============================================================ End