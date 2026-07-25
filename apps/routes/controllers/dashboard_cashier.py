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
from ..models.dashboard_cashier import DashboardCashierModels
from apps.routes.controllers.report import *

# BLUEPRINT ================================================== Begin
dashboard_cashier = Blueprint(
    name='dashboard_cashier',
    import_name=__name__,
    template_folder="../../templates/pages/cashierPages",
    url_prefix='/dashboard-cashier',
)
# BLUEPRINT ================================================== End

# DASHBOARD PAGE ============================================================ Begin
# GET https://127.0.0.1:5000/dashboard_cashier/
@dashboard_cashier.get('/')
@jwt_required()
def index():
    try:
      return render_template(
            title='Kasir - POS Bengkel',
            template_name_or_list='dashboard_cashier.html',
            active_menu="dashboard_cashier",
      )

    except Exception as e:
        return bad_request(str(e))
# DASHBOARD PAGE ============================================================ End

# DASHBOARD SUMMARY ============================================================ Begin
# [GET] https://127.0.0.1:5000/dashboard_cashier/summary
@dashboard_cashier.get('/summary')
@jwt_required()
def dashboard_summary():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])
        user_id = str(get_jwt()["id"])

        response = DashboardCashierModels.dashboard_summary(role, ws_id, user_id)

        return response

    except Exception as e:
        return bad_request(str(e))
# DASHBOARD SUMMARY ============================================================ End

# PAYMENT CHART ============================================================ Begin
# [POST] https://127.0.0.1:5000/dashboard_cashier/payment-chart
@dashboard_cashier.post('/payment-chart')
@jwt_required()
def payment_chart():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])
        user_id = str(get_jwt()["id"])

        body = request.json

        response = DashboardCashierModels.payments_chart(
            role,
            ws_id,
            user_id,
            body["start_date"],
            body["end_date"]
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# PAYMENT CHART ============================================================ End

# TOP PRODUCTS ============================================================ Begin
# [POST] https://127.0.0.1:5000/dashboard_cashier/top-products
@dashboard_cashier.post('/top-products')
@jwt_required()
def top_products():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])
        user_id = str(get_jwt()["id"])

        body = request.json

        response = DashboardCashierModels.top_products(
            role,
            ws_id,
            user_id,
            body["start_date"],
            body["end_date"]
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# TOP PRODUCTS ============================================================ End

# TOP SERVICES ============================================================ Begin
# [POST] https://127.0.0.1:5000/dashboard_cashier/top-services
@dashboard_cashier.post('/top-services')
@jwt_required()
def top_services():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])
        user_id = str(get_jwt()["id"])

        body = request.json

        response = DashboardCashierModels.top_services(
            role,
            ws_id,
            user_id,
            body["start_date"],
            body["end_date"]
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# TOP SERVICES ============================================================ End

# LOW STOCK ============================================================ Begin
# [GET] https://127.0.0.1:5000/dashboard_cashier/low-stock
@dashboard_cashier.get('/low-stock')
@jwt_required()
def low_stock():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        response = DashboardCashierModels.low_stock(role, ws_id)

        return response

    except Exception as e:
        return bad_request(str(e))
# LOW STOCK ============================================================ End

# RECENT TRANSACTIONS ============================================================ Begin
# [GET] https://127.0.0.1:5000/dashboard_cashier/recent-transactions
@dashboard_cashier.get('/recent-transactions')
@jwt_required()
def recent_transactions():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])
        user_id = str(get_jwt()["id"])

        response = DashboardCashierModels.recent_transactions(role, ws_id, user_id)

        return response

    except Exception as e:
        return bad_request(str(e))
# RECENT TRANSACTIONS ============================================================ End

# DEPOSIT SUMMARY ============================================================ Begin
# [GET] https://127.0.0.1:5000/dashboard_cashier/recent-transactions
@dashboard_cashier.get("/deposit-summary")
@jwt_required()
def deposit_summary():
    try:
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])
        user_id = str(get_jwt()["id"])

        response = DashboardCashierModels.deposit_summary(
            role,
            ws_id,
            user_id
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# DEPOSIT SUMMARY ============================================================ End

# CASHIER PROFILE ============================================================ Begin
# [GET] https://127.0.0.1:5000/dashboard_cashier/recent-transactions
@dashboard_cashier.get("/profile")
@jwt_required()
def cashier_profile():
    try:
        role = str(get_jwt()["role"])
        user_id = str(get_jwt()["id"])

        response = DashboardCashierModels.cashier_profile(
            role,
            user_id
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# CASHIER PROFILE ============================================================ End
