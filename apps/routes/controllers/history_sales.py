from flask import Blueprint, render_template, request
from flask_jwt_extended import jwt_required, get_jwt

from ..models.history_sales import HistorySalesModels
from ...utilities.responseHelpers import bad_request

# BLUEPRINT ============================================================ Begin
history_sales = Blueprint(
    name="history_sales",
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix="/history-sales",
)
# BLUEPRINT ============================================================ End


# HISTORY SALES PAGE OWNER============================================================ Begin
# [GET] https://127.0.0.1:5000/history-sales/
@history_sales.get("/")
@jwt_required()
def owner():
    try:
        return render_template(
            title="Riwayat Penjualan - POS Bengkel",
            template_name_or_list="owner_history_sales.html",
            active_menu="owner_history_sales",
        )

    except Exception as e:
        return bad_request(str(e))
# HISTORY SALES PAGE OWNER============================================================ End

# HISTORY SALES CASHIER PAGE ============================================================ Begin
# [GET] https://127.0.0.1:5000/history-sales/cashier
@history_sales.get("/cashier")
@jwt_required()
def cashier():
    try:
        return render_template(
            title="Cashier History Sales - POS Bengkel",
            template_name_or_list="cashier_history_sales.html",
            active_menu="cashier_history_sales",
        )

    except Exception as e:
        return bad_request(str(e))
# HISTORY CASHIER PAGE ============================================================ End


# READ HISTORY SALES ============================================================ Begin
# [GET] https://127.0.0.1:5000/history-sales/view
@history_sales.get("/view")
@jwt_required()
def read_history_sales():
    try:

        claims = get_jwt()

        user_role = claims["role"]
        user_id = claims["id"]
        workshop_id = claims["ws_id"]

        # Filter tanggal
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        cashier_id = request.args.get("cashier_id", "")

        return HistorySalesModels.read_history_sales(
            user_role,
            user_id,
            workshop_id,
            cashier_id,
            start_date,
            end_date
        )

    except Exception as e:
        return bad_request(str(e))
# READ HISTORY SALES ============================================================ End

# DETAIL HISTORY SALES ============================================================ Begin
# [GET] https://127.0.0.1:5000/history-sales/detail/1
@history_sales.get("/detail/<int:payment_id>")
@jwt_required()
def detail_history_sales(payment_id):
    try:

        claims = get_jwt()

        user_role = claims["role"]
        user_id = claims["id"]
        workshop_id = claims["ws_id"]

        return HistorySalesModels.detail_history_sales(
            user_role,
            user_id,
            workshop_id,
            payment_id
        )

    except Exception as e:
        return bad_request(str(e))
# DETAIL HISTORY SALES ============================================================ End

# EXPORT EXCEL ============================================================ Begin
# [GET] https://127.0.0.1:5000/history-sales/excle
@history_sales.post("/excel")
@jwt_required()
def export_excel():

      jwt = get_jwt()

      result = HistorySalesModels.export_excel(
            user_role=jwt["role"],
            user_id=jwt["id"],
            workshop_id=jwt["ws_id"],
            start_date=request.json.get("start_date"),
            end_date=request.json.get("end_date")
      )

      return result
# EXPORT EXCEL ============================================================ End

# EXPORT PDF ============================================================ Begin
# [GET] https://127.0.0.1:5000/history-sales/pdf
@history_sales.post("/pdf")
@jwt_required()
def export_pdf():

      jwt = get_jwt()

      result = HistorySalesModels.export_pdf(
            user_role=jwt["role"],
            user_id=jwt["id"],
            workshop_id=jwt["ws_id"],
            start_date=request.json.get("start_date"),
            end_date=request.json.get("end_date")
      )

      return result
# EXPORT PDF ============================================================ End