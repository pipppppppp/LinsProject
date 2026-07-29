from flask import Blueprint, render_template, request
from flask_jwt_extended import jwt_required, get_jwt

from ..models.history_purchase import HistoryPurchaseModels
from ...utilities.responseHelpers import bad_request

# BLUEPRINT ============================================================ Begin
history_purchase = Blueprint(
    name="history_purchase",
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix="/history-purchase"
)
# BLUEPRINT ============================================================ End

# HISTORY PURCHASE PAGE ============================================================ Begin
# [GET] https://127.0.0.1:5000/history_purchase/
@history_purchase.get("/")
@jwt_required()
def index():
    try:

        return render_template(
            title="Riwayat Pembelian - POS Bengkel",
            template_name_or_list="history_purchase.html",
            active_menu="history_purchase"
        )

    except Exception as e:
        return bad_request(str(e))
# HISTORY PURCHASE PAGE ============================================================ End

# READ HISTORY PURCHASE ============================================================ Begin
# [POST] https://127.0.0.1:5000/history_purchase/view
@history_purchase.get("/view")
@jwt_required()
def read_history_purchase():
    try:

        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        supplier_id = request.args.get("supplier_id", "")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        response = HistoryPurchaseModels.read_history_purchase(
            role,
            ws_id,
            supplier_id,
            start_date,
            end_date
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# READ HISTORY PURCHASE ============================================================ End

# DETAIL HISTORY PURCHASE ============================================================ Begin
@history_purchase.get("/detail/<int:id>")
@jwt_required()
def detail_history_purchase(id):
    try:

        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        response = HistoryPurchaseModels.detail_history_purchase(
            role,
            ws_id,
            id
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# DETAIL HISTORY PURCHASE ============================================================ End

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