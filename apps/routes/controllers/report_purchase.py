from flask import Blueprint, request, render_template
from flask_jwt_extended import jwt_required, get_jwt

from ..models.report_purchase import ReportPurchaseModels
from ...utilities.responseHelpers import bad_request


# BLUEPRINT ============================================================ Begin
report_purchase = Blueprint(
    name="report_purchase",
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix="/report-purchase",
)
# BLUEPRINT ============================================================ End


# REPORT SALES PAGE ============================================================ Begin
# [GET] https://127.0.0.1:5000/report-sales/
@report_purchase.get("/")
@jwt_required()
def index():
    try:
        return render_template(
            title="Report Sales - POS Bengkel",
            template_name_or_list="report_purchase.html",
            active_menu="report_purchase",
        )
    except Exception as e:
        return bad_request(str(e))
# REPORT SALES PAGE ============================================================ End


# REPORT SUMMARY ============================================================ Begin
# [GET] https://127.0.0.1:5000/report-purchase/summary
@report_purchase.get("/summary")
@jwt_required()
def report_summary():
    try:

      role = str(get_jwt()["role"])
      user_id = str(get_jwt()["id"])
      ws_id = str(get_jwt()["ws_id"])

      supplier_id = request.args.get("supplier_id", "")
      start_date = request.args.get("start_date")
      end_date = request.args.get("end_date")

      response = ReportPurchaseModels.report_summary(
            role,
            user_id,
            ws_id,
            supplier_id,
            request.args.get("start_date"),
            request.args.get("end_date"),
      )

      return response

    except Exception as e:
        return bad_request(str(e))
# REPORT SUMMARY ============================================================ End


# SALES CHART ============================================================ Begin
# [GET] https://127.0.0.1:5000/report-purchase/chart
@report_purchase.get("/chart")
@jwt_required()
def sales_chart():
    try:

      role = str(get_jwt()["role"])
      user_id = str(get_jwt()["id"])
      ws_id = str(get_jwt()["ws_id"])

      supplier_id = request.args.get("supplier_id", "")
      start_date = request.args.get("start_date")
      end_date = request.args.get("end_date")

      return ReportPurchaseModels.purchase_chart(
        role,
        user_id,
        ws_id,
        supplier_id,
        start_date,
        end_date
      )

      return response

    except Exception as e:
        return bad_request(str(e))
# SALES CHART ============================================================ End


# TOP SUPPLIER ============================================================ Begin
# [GET] https://127.0.0.1:5000/report-purchase/top-products
@report_purchase.get("/top-suppliers")
@jwt_required()
def top_supplier():
    try:

      role = str(get_jwt()["role"])
      user_id = str(get_jwt()["id"])
      ws_id = str(get_jwt()["ws_id"])

      supplier_id = request.args.get("supplier_id", "")
      start_date = request.args.get("start_date")
      end_date = request.args.get("end_date")
      response = ReportPurchaseModels.top_suppliers(
            role,
            user_id,
            ws_id,
            supplier_id,
            start_date,
            end_date
      )

      return response

    except Exception as e:
        return bad_request(str(e))
# TOP SUPPLIER ============================================================ End


# TOP SERVICES ============================================================ Begin
# [GET] https://127.0.0.1:5000/report-purchase/top-services
@report_purchase.get("/top-products")
@jwt_required()
def top_products():
      try:
            claims = get_jwt()

            role = claims.get("role")
            user_id = claims.get("id")
            ws_id = claims.get("ws_id")

            supplier_id = request.args.get("supplier_id", "")
            start_date = request.args.get("start_date")
            end_date = request.args.get("end_date")

            return ReportPurchaseModels.top_product(
                  role,
                  user_id,
                  ws_id,
                  supplier_id,
                  start_date,
                  end_date
            )

            return response

      except Exception as e:
            return bad_request(str(e))
# TOP SERVICES ============================================================ End


# REPORT TABLE ============================================================ Begin
# [GET] https://127.0.0.1:5000/report-purchase/table
@report_purchase.get("/table")
@jwt_required()
def report_table():
    try:

        role = str(get_jwt()["role"])
        user_id = str(get_jwt()["id"])
        ws_id = str(get_jwt()["ws_id"])

        supplier_id = request.args.get("supplier_id", "")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        return ReportPurchaseModels.report_table(
            role,
            user_id,
            ws_id,
            supplier_id,
            start_date,
            end_date
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# REPORT TABLE ============================================================ End


# EXPORT EXCEL ============================================================ Begin
# [POST] https://127.0.0.1:5000/report-purchase/export/excel
@report_purchase.post("/export/excel")
@jwt_required()
def export_excel():
    try:

        role = str(get_jwt()["role"])
        user_id = str(get_jwt()["id"])
        ws_id = str(get_jwt()["ws_id"])

        body = request.json

        response = ReportPurchaseModels.export_excel(
            role,
            user_id,
            ws_id,
            body.get("supplier_id", ""),
            body.get("start_date"),
            body.get("end_date"),
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# EXPORT EXCEL ============================================================ End


# EXPORT PDF ============================================================ Begin
# [POST] https://127.0.0.1:5000/report-purchase/export/pdf
@report_purchase.post("/export/pdf")
@jwt_required()
def export_pdf():
    try:

        role = str(get_jwt()["role"])
        user_id = str(get_jwt()["id"])
        ws_id = str(get_jwt()["ws_id"])

        body = request.json

        response = ReportPurchaseModels.export_pdf(
            role,
            user_id,
            ws_id,
            body.get("supplier_id", ""),
            body.get("start_date"),
            body.get("end_date"),
        )
        return response

    except Exception as e:
        return bad_request(str(e))
# EXPORT PDF ============================================================ End