from flask import Blueprint, request, render_template
from flask_jwt_extended import get_jwt, jwt_required

from apps.utilities.responseHelpers import bad_request

from ..models.subscription_payment_history import (
    SubscriptionPaymentHistoryModels,
)


# BLUEPRINT ============================================================ Begin
subscription_payment_history = Blueprint(
    name="subscription_payment_history",
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix="/subscription-payment-history",
)
# BLUEPRINT ============================================================ End


# PAYMENT HISTORY PAGE ============================================================ Begin
# GET http://127.0.0.1:5000/subscription-payment-history/
@subscription_payment_history.get("/")
@jwt_required()
def index():
    try:
        # Return Page ========================================
        return render_template(
            template_name_or_list=(
                "subscription_payment_history.html"
            ),
            title=(
                "Riwayat Pembayaran - POS Bengkel"
            ),
            active_menu=(
                "subscription_payment_history"
            ),
        )

    except Exception as e:
        return bad_request(str(e))
# PAYMENT HISTORY PAGE ============================================================ End


# VIEW PAYMENT HISTORY ============================================================ Begin
# GET http://127.0.0.1:5000/subscription-payment-history/view
@subscription_payment_history.get("/view")
@jwt_required()
def read_payment_history():
    try:
        # JWT Access Data ========================================
        role = str(
            get_jwt()["role"]
        )

        # Request Parameters ========================================
        status = request.args.get(
            "status",
            "all"
        )

        # Request Process ========================================
        response = (
            SubscriptionPaymentHistoryModels
            .read_payment_history(
                role,
                status
            )
        )

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# VIEW PAYMENT HISTORY ============================================================ End


# DETAIL PAYMENT ============================================================ Begin
# GET http://127.0.0.1:5000/subscription-payment-history/detail/1
@subscription_payment_history.get("/detail/<int:payment_id>")
@jwt_required()
def detail_payment(payment_id):
    try:
        # JWT Access Data ========================================
        role = str(
            get_jwt()["role"]
        )

        # Request Process ========================================
        response = (
            SubscriptionPaymentHistoryModels
            .detail_payment(
                role,
                payment_id
            )
        )

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# DETAIL PAYMENT ============================================================ End