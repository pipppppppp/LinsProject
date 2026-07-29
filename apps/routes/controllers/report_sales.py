from flask import Blueprint, request, render_template
from flask_jwt_extended import jwt_required, get_jwt

from ..models.report_sales import ReportSalesModels
from ...utilities.responseHelpers import bad_request


# BLUEPRINT ============================================================ Begin
report_sales = Blueprint(
    name="report_sales",
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix="/report-sales",
)
# BLUEPRINT ============================================================ End


# REPORT SALES PAGE ============================================================ Begin
# [GET] https://127.0.0.1:5000/report-sales/
@report_sales.get("/")
@jwt_required()
def index():
    try:
        return render_template(
            title="Report Sales - POS Bengkel",
            template_name_or_list="report_sales.html",
            active_menu="report_sales",
        )
    except Exception as e:
        return bad_request(str(e))
# REPORT SALES PAGE ============================================================ End


# REPORT SUMMARY ============================================================ Begin
# [GET] https://127.0.0.1:5000/report-sales/summary
@report_sales.get("/summary")
@jwt_required()
def report_summary():
    try:

        role = str(get_jwt()["role"])
        user_id = str(get_jwt()["id"])
        ws_id = str(get_jwt()["ws_id"])

        response = ReportSalesModels.report_summary(
            role,
            user_id,
            ws_id,
            request.args.get("cashier_id", ""),
            request.args.get("start_date"),
            request.args.get("end_date"),
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# REPORT SUMMARY ============================================================ End


# SALES CHART ============================================================ Begin
# [GET] https://127.0.0.1:5000/report-sales/chart
@report_sales.get("/chart")
@jwt_required()
def sales_chart():
    try:

        role = str(get_jwt()["role"])
        user_id = str(get_jwt()["id"])
        ws_id = str(get_jwt()["ws_id"])

        response = ReportSalesModels.sales_chart(
            role,
            user_id,
            ws_id,
            request.args.get("cashier_id", ""),
            request.args.get("start_date"),
            request.args.get("end_date"),
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# SALES CHART ============================================================ End


# TOP PRODUCTS ============================================================ Begin
# [GET] https://127.0.0.1:5000/report-sales/top-products
@report_sales.get("/top-products")
@jwt_required()
def top_products():
    try:

        role = str(get_jwt()["role"])
        user_id = str(get_jwt()["id"])
        ws_id = str(get_jwt()["ws_id"])

        response = ReportSalesModels.top_products(
            role,
            user_id,
            ws_id,
            request.args.get("cashier_id", ""),
            request.args.get("start_date"),
            request.args.get("end_date"),
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# TOP PRODUCTS ============================================================ End


# TOP SERVICES ============================================================ Begin
# [GET] https://127.0.0.1:5000/report-sales/top-services
@report_sales.get("/top-services")
@jwt_required()
def top_services():
    try:

        role = str(get_jwt()["role"])
        user_id = str(get_jwt()["id"])
        ws_id = str(get_jwt()["ws_id"])

        response = ReportSalesModels.top_services(
            role,
            user_id,
            ws_id,
            request.args.get("cashier_id", ""),
            request.args.get("start_date"),
            request.args.get("end_date"),
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# TOP SERVICES ============================================================ End


# REPORT TABLE ============================================================ Begin
# [GET] https://127.0.0.1:5000/report-sales/table
@report_sales.get("/table")
@jwt_required()
def report_table():
    try:

        role = str(get_jwt()["role"])
        user_id = str(get_jwt()["id"])
        ws_id = str(get_jwt()["ws_id"])

        response = ReportSalesModels.report_table(
            role,
            user_id,
            ws_id,
            request.args.get("cashier_id", ""),
            request.args.get("start_date"),
            request.args.get("end_date"),
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# REPORT TABLE ============================================================ End


# EXPORT EXCEL ============================================================ Begin
# [POST] https://127.0.0.1:5000/report-sales/export/excel
@report_sales.post("/export/excel")
@jwt_required()
def export_excel():
    try:

        role = str(get_jwt()["role"])
        user_id = str(get_jwt()["id"])
        ws_id = str(get_jwt()["ws_id"])

        body = request.json

        response = ReportSalesModels.export_excel(
            role,
            user_id,
            ws_id,
            body.get("cashier_id", ""),
            body.get("start_date"),
            body.get("end_date"),
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# EXPORT EXCEL ============================================================ End


# EXPORT PDF ============================================================ Begin
# [POST] https://127.0.0.1:5000/report-sales/export/pdf
@report_sales.post("/export/pdf")
@jwt_required()
def export_pdf():
    try:

        role = str(get_jwt()["role"])
        user_id = str(get_jwt()["id"])
        ws_id = str(get_jwt()["ws_id"])

        body = request.json

        response = ReportSalesModels.export_pdf(
            role,
            user_id,
            ws_id,
            body.get("cashier_id", ""),
            body.get("start_date"),
            body.get("end_date"),
        )
        return response

    except Exception as e:
        return bad_request(str(e))
# EXPORT PDF ============================================================ End