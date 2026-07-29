from apps import db
from apps.database.db_users import Users
from apps.database.db_workshops import Workshops
from apps.database.db_subscription_payment import SubscriptionPayments

from apps.utilities.responseHelpers import *
from apps.utilities.validators import administrator_validator
from apps.utilities.formatter import format_datetime


# SUBSCRIPTION PAYMENT HISTORY MODEL CLASS ============================================================ Begin
class SubscriptionPaymentHistoryModels():

    # VIEW PAYMENT HISTORY ============================================================ Begin
    def read_payment_history(user_role, status="all"):
        try:
            # Access Validation ---------------------------------------- Start
            access = administrator_validator(user_role)

            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Initialize Query ---------------------------------------- Start
            query = (
                db.session.query(
                    SubscriptionPayments,
                    Workshops,
                    Users
                )
                .join(
                    Workshops,
                    SubscriptionPayments.workshop_id
                    == Workshops.id
                )
                .join(
                    Users,
                    Workshops.owner_id
                    == Users.id
                )
                .filter(
                    SubscriptionPayments.is_delete == 0
                )
            )

            status = str(
                status or "all"
            ).strip().lower()
            # Initialize Query ---------------------------------------- Finish

            # Status Filter ---------------------------------------- Start
            if status == "success":
                query = query.filter(
                    SubscriptionPayments.transaction_status.in_([
                        "settlement",
                        "capture",
                        "success"
                    ])
                )

            elif status == "pending":
                query = query.filter(
                    SubscriptionPayments.transaction_status
                    == "pending"
                )

            elif status == "failed":
                query = query.filter(
                    SubscriptionPayments.transaction_status.in_([
                        "deny",
                        "cancel",
                        "failure",
                        "expire",
                        "expired"
                    ])
                )
            # Status Filter ---------------------------------------- Finish

            # Get Payment History ---------------------------------------- Start
            payments = query.order_by(
                SubscriptionPayments.created_at.desc()
            ).all()
            # Get Payment History ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            history = []

            for payment, workshop, owner in payments:
                history.append({
                    "payment_id": payment.id,
                    "workshop_id": workshop.id,
                    "owner_id": owner.id,
                    "order_id": payment.order_id,
                    "transaction_id": (
                        payment.transaction_id
                        if payment.transaction_id
                        else "-"
                    ),
                    "workshop_name": workshop.workshop_name,
                    "owner_name": (
                        owner.owner_name
                        if owner.owner_name
                        else "-"
                    ),
                    "owner_email": (
                        owner.email
                        if owner.email
                        else "-"
                    ),
                    "amount": int(
                        payment.amount or 0
                    ),
                    "payment_type": (
                        payment.payment_type
                        if payment.payment_type
                        else "-"
                    ),
                    "transaction_status": (
                        payment.transaction_status
                        if payment.transaction_status
                        else "-"
                    ),
                    "paid_at": (
                        format_datetime(
                            payment.paid_at
                        )
                        if payment.paid_at
                        else "-"
                    ),
                    "created_at": (
                        format_datetime(
                            payment.created_at
                        )
                        if payment.created_at
                        else "-"
                    )
                })
            # Response Data ---------------------------------------- Finish

            # Return Response ========================================
            return success_data(history)

        except Exception as e:
            return bad_request(str(e))
    # VIEW PAYMENT HISTORY ============================================================ End


    # DETAIL PAYMENT ============================================================ Begin
    def detail_payment(user_role, payment_id):
        try:
            # Access Validation ---------------------------------------- Start
            access = administrator_validator(user_role)

            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Check Payment ---------------------------------------- Start
            result = (
                db.session.query(
                    SubscriptionPayments,
                    Workshops,
                    Users
                )
                .join(
                    Workshops,
                    SubscriptionPayments.workshop_id
                    == Workshops.id
                )
                .join(
                    Users,
                    Workshops.owner_id
                    == Users.id
                )
                .filter(
                    SubscriptionPayments.id == payment_id,
                    SubscriptionPayments.is_delete == 0
                )
                .first()
            )

            if not result:
                return not_found(
                    "Subscription payment could not be found."
                )
            # Check Payment ---------------------------------------- Finish

            # Initialize Data ---------------------------------------- Start
            payment, workshop, owner = result
            # Initialize Data ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            response = {
                "payment_id": payment.id,
                "workshop_id": workshop.id,
                "owner_id": owner.id,
                "order_id": payment.order_id,
                "transaction_id": (
                    payment.transaction_id
                    if payment.transaction_id
                    else "-"
                ),
                "workshop_name": workshop.workshop_name,
                "workshop_email": (
                    workshop.workshop_email
                    if workshop.workshop_email
                    else "-"
                ),
                "workshop_phone": workshop.workshop_phone,
                "owner_name": (
                    owner.owner_name
                    if owner.owner_name
                    else "-"
                ),
                "owner_email": owner.email,
                "amount": int(
                    payment.amount or 0
                ),
                "payment_type": (
                    payment.payment_type
                    if payment.payment_type
                    else "-"
                ),
                "transaction_status": (
                    payment.transaction_status
                    if payment.transaction_status
                    else "-"
                ),
                "paid_at": (
                    format_datetime(
                        payment.paid_at
                    )
                    if payment.paid_at
                    else "-"
                ),
                "created_at": (
                    format_datetime(
                        payment.created_at
                    )
                    if payment.created_at
                    else "-"
                )
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ========================================
            return success_data(response)

        except Exception as e:
            return bad_request(str(e))
    # DETAIL PAYMENT ============================================================ End

# SUBSCRIPTION PAYMENT HISTORY MODEL CLASS ============================================================ End