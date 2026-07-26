from flask import Blueprint, render_template, session, redirect, url_for
from flask import current_app as app
from flask_jwt_extended import jwt_required, get_jwt

from datetime import datetime, timedelta

from apps.database.db_workshops import Workshops
from apps.database.db_users import Users
from apps.database.db_products import Products
from apps.database.db_customers import Customers
from apps.database.db_suppliers import Suppliers
from apps.database.db_purchases import Purchases
from apps.database.db_payment import Payments
from ..models.dashboard import DashboardModels
from apps.routes.controllers.report import *

# BLUEPRINT ================================================== Begin
dashboard = Blueprint(
    name='dashboard',
    import_name=__name__,
    template_folder="../../templates/pages/adminPages",
    url_prefix='/dashboard',
)
# BLUEPRINT ================================================== End

# DASHBOARD PAGE ============================================================ Begin
# GET https://127.0.0.1:5000/dashboard/
@dashboard.get('/')
@jwt_required()
def index():
    try:
        claims = get_jwt()
        
        if claims["role"] == 0:
            return redirect(url_for("administrator.dashboard"))
        # elif claims["role"] == 1:
        #     return render_template("dashboard.html")   # atau dashboard.index
        elif claims["role"] == 2:
            return redirect(url_for("dashboard_cashier.index"))

        workshop = Workshops.query.filter_by(
            owner_id=claims["id"],
            is_delete=0
        ).first()

        role_map = {
            0: "Administrator",
            1: "Owner",
            2: "Kasir"
        }

        return render_template(
            "dashboard.html",
            title="Dashboard POS Bengkel",
            active_menu="dashboard",

            username=claims["name"],
            email=claims["email"],
            role_name=role_map.get(int(claims["role"]), "-"),
            is_active=1,
            workshop_status=workshop.is_active if workshop else 0
        )
    except Exception as e:
        return bad_request(str(e))
# DASHBOARD PAGE ============================================================ End

# DASHBOARD SUMMARY ============================================================ Begin
# [GET] https://127.0.0.1:5000/dashboard/summary
@dashboard.get('/summary')
@jwt_required()
def dashboard_summary():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])
        name = str(get_jwt()["name"])

        response = DashboardModels.dashboard_summary(role, ws_id, name)

        return response

    except Exception as e:
        return bad_request(str(e))
# DASHBOARD SUMMARY ============================================================ End

# SALES CHART ============================================================ Begin
# [POST] https://127.0.0.1:5000/dashboard/payment-chart
@dashboard.post('/payment-chart')
@jwt_required()
def payment_chart():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        body = request.json

        response = DashboardModels.payments_chart(
            role,
            ws_id,
            body["start_date"],
            body["end_date"]
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# SALES CHART ============================================================ End

# PURCHASE CHART ============================================================ Begin
# [POST] https://127.0.0.1:5000/dashboard/purchase-chart
@dashboard.post('/purchase-chart')
@jwt_required()
def purchase_chart():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        body = request.json

        response = DashboardModels.purchase_chart(
            role,
            ws_id,
            body["start_date"],
            body["end_date"]
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# PURCHASE CHART ============================================================ End

# TOP PRODUCTS ============================================================ Begin
# [POST] https://127.0.0.1:5000/dashboard/top-products
@dashboard.post('/top-products')
@jwt_required()
def top_products():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        body = request.json

        response = DashboardModels.top_products(
            role,
            ws_id,
            body["start_date"],
            body["end_date"]
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# TOP PRODUCTS ============================================================ End

# TOP SERVICES ============================================================ Begin
# [POST] https://127.0.0.1:5000/dashboard/top-services
@dashboard.post('/top-services')
@jwt_required()
def top_services():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        body = request.json

        response = DashboardModels.top_services(
            role,
            ws_id,
            body["start_date"],
            body["end_date"]
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# TOP SERVICES ============================================================ End

# LOW STOCK ============================================================ Begin
# [GET] https://127.0.0.1:5000/dashboard/low-stock
@dashboard.get('/low-stock')
@jwt_required()
def low_stock():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        response = DashboardModels.low_stock(role, ws_id)

        return response

    except Exception as e:
        return bad_request(str(e))
# LOW STOCK ============================================================ End

# RECENT TRANSACTIONS ============================================================ Begin
# [GET] https://127.0.0.1:5000/dashboard/recent-transactions
@dashboard.get('/recent-transactions')
@jwt_required()
def recent_transactions():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        response = DashboardModels.recent_transactions(role, ws_id)

        return response

    except Exception as e:
        return bad_request(str(e))
# RECENT TRANSACTIONS ============================================================ End