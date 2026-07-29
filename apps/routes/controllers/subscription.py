from flask import Blueprint, request, render_template, current_app
from flask_jwt_extended import jwt_required, get_jwt

from ..models.subscription import SubscriptionModels
from ...utilities.responseHelpers import bad_request, authorization_error
from ...utilities.validators import owner_validator


# BLUEPRINT ============================================================ Begin
subscription = Blueprint(
    name="subscription",
    import_name=__name__,
    url_prefix="/subscription"
)
# BLUEPRINT ============================================================ End

# SUBSCRIPTION PAGE ============================================================ Begin
# [GET] http://127.0.0.1:5000/subscription/
@subscription.get("/")
@jwt_required()
def index():
    try:
        # JWT Access Data ========================================
        role = str(get_jwt()["role"])

        # Access Validation ========================================
        access = owner_validator(role)

        if not access:
            return authorization_error()

        # Return Page ========================================
        return render_template(
            title="Langganan - POS Bengkel",
            template_name_or_list="subscription.html",
            active_menu="subscription",
            midtrans_client_key=current_app.config[
                "MIDTRANS_CLIENT_KEY"
            ]
        )

    except Exception as e:
        return bad_request(str(e))
# SUBSCRIPTION PAGE ============================================================ End

# CREATE SUBSCRIPTION PAYMENT ============================================================ Begin
# [POST] http://127.0.0.1:5000/subscription/create-payment
@subscription.post("/create-payment")
@jwt_required()
def create_subscription_payment():
    try:
        # JWT Access Data ========================================
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        # Request Process ========================================
        body = request.get_json(silent=True)

        response = SubscriptionModels.create_payment(
            role,
            ws_id,
            body
        )

        return response

    except Exception as e:
        return bad_request(str(e))
# CREATE SUBSCRIPTION PAYMENT ============================================================ End

# MIDTRANS NOTIFICATION ============================================================ Begin
# [POST] http://127.0.0.1:5000/subscription/notification
@subscription.post("/notification")
def midtrans_notification():
    try:
        # Request Data ========================================
        body = request.get_json(silent=True)

        # Request Process ========================================
        response = SubscriptionModels.handle_notification(body)

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# MIDTRANS NOTIFICATION ============================================================ End

# READ SUBSCRIPTION STATUS ============================================================ Begin
# [GET] http://127.0.0.1:5000/subscription/status
@subscription.get("/status")
@jwt_required()
def read_subscription_status():
    try:
        # JWT Access Data ========================================
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        # Request Process ========================================
        response = SubscriptionModels.read_status(
            role,
            ws_id
        )

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# READ SUBSCRIPTION STATUS ============================================================ End

# SYNC PAYMENT STATUS ============================================================ Begin
# [POST] http://127.0.0.1:5000/subscription/sync-status
@subscription.post("/sync-status")
@jwt_required()
def sync_subscription_status():
    try:
        # JWT Access Data ========================================
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        # Request Process ========================================
        response = SubscriptionModels.sync_status(role, ws_id)

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# SYNC PAYMENT STATUS ============================================================ End

# READ PAYMENT HISTORY ============================================================ Begin
# [GET] http://127.0.0.1:5000/subscription/history
@subscription.get("/history")
@jwt_required()
def read_subscription_history():
    try:
        # JWT Access Data ========================================
        role = str(get_jwt()["role"])
        ws_id = str(get_jwt()["ws_id"])

        # Request Process ========================================
        response = SubscriptionModels.read_history(
            role,
            ws_id
        )

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# READ PAYMENT HISTORY ============================================================ End