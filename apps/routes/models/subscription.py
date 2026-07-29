# **************************************************************
# IMPORT LIBRARY | START
# **************************************************************
import hashlib
import hmac

from decimal import Decimal, InvalidOperation
from flask import current_app

from apps import db
from apps.database.db_subscription_payment import SubscriptionPayments
from apps.database.db_workshops import Workshops
from apps.utilities.midtrans import get_snap
from apps.utilities.responseHelpers import *
from apps.utilities.formatter import format_datetime, format_rupiah
from apps.utilities.validators import owner_validator
from apps.utilities.utilities import current_timestamp
# **************************************************************
# IMPORT LIBRARY | END
# **************************************************************


# **************************************************************
# SUBSCRIPTION PACKAGE | START
# **************************************************************
SUBSCRIPTION_PACKAGES = {
    "monthly": {
        "name": "Langganan POS Bengkel 1 Bulan",
        "amount": 50000,
        "duration_days": 30,
    },
}
# **************************************************************
# SUBSCRIPTION PACKAGE | END
# **************************************************************


# **************************************************************
# SUBSCRIPTION MODEL CLASS | START
# **************************************************************
class SubscriptionModels:

    # CREATE SUBSCRIPTION PAYMENT ============================================================ Begin
    def create_payment(user_role, workshop_id, datas):
        try:
            # ACCESS VALIDATION ==================================
            access = owner_validator(user_role)

            if not access:
                return authorization_error()

            # REQUEST VALIDATION =================================
            if datas is None:
                return invalid_params()

            if "package" not in datas:
                return parameter_error(
                    "Missing package in request body."
                )

            package_code = str(datas["package"]).strip().lower()

            if package_code not in SUBSCRIPTION_PACKAGES:
                return parameter_error(
                    "Paket langganan tidak tersedia."
                )

            # CHECK WORKSHOP =====================================
            workshop = Workshops.query.filter_by(
                id=workshop_id,
                is_delete=0
            ).first()

            if not workshop:
                return not_found(
                    "Workshop could not be found."
                )
            # Check Active Subscription ---------------------------------------- Start
            timestamp = current_timestamp()

            subscription_end = int(
                workshop.subscription_end or 0
            )

            renewal_period = (
                7
                * 24
                * 60
                * 60
                * 1000
            )

            if (
                int(workshop.subscription_status or 0) == 1
                and subscription_end > timestamp + renewal_period
            ):
                return parameter_error(
                    "Langganan masih aktif dan belum dapat diperpanjang."
                )
            # Check Active Subscription ---------------------------------------- Finish
          
            # Check Pending Payment ---------------------------------------- Start
            pending_payment = SubscriptionPayments.query.filter_by(
                workshop_id=workshop.id,
                transaction_status="pending",
                is_delete=0
            ).order_by(
                SubscriptionPayments.created_at.desc()
            ).first()

            if pending_payment:
                data = {
                    "payment_id": pending_payment.id,
                    "order_id": pending_payment.order_id,
                    "package": "monthly",
                    "package_name": SUBSCRIPTION_PACKAGES[
                        "monthly"
                    ]["name"],
                    "amount": int(pending_payment.amount),
                    "snap_token": pending_payment.snap_token,
                    "transaction_status": (
                        pending_payment.transaction_status
                    ),
                    "is_existing": True
                }

                return success_data(
                    data=data,
                    status_code=200
                )
            # Check Pending Payment ---------------------------------------- Finish

            # INITIALIZE PACKAGE =================================
            package = SUBSCRIPTION_PACKAGES[package_code]

            timestamp = current_timestamp()

            order_id = (
                f"SUB-{workshop_id}-{timestamp}"
            )

            amount = package["amount"]

            # MIDTRANS TRANSACTION DATA ==========================
            transaction_data = {
                "transaction_details": {
                    "order_id": order_id,
                    "gross_amount": amount,
                },
                "item_details": [
                    {
                        "id": package_code,
                        "price": amount,
                        "quantity": 1,
                        "name": package["name"],
                    }
                ],
            }

            # CREATE SNAP TOKEN ==================================
            snap = get_snap()

            snap_response = snap.create_transaction(
                transaction_data
            )

            snap_token = snap_response.get("token")
            redirect_url = snap_response.get("redirect_url")

            if not snap_token:
                return bad_request(
                    "Gagal mendapatkan Snap Token dari Midtrans."
                )

            # INSERT PAYMENT =====================================
            payment = SubscriptionPayments(
                workshop_id=workshop.id,
                order_id=order_id,
                amount=amount,
                transaction_status="pending",
                snap_token=snap_token,
                created_at=timestamp,
                updated_at=timestamp,
                is_delete=0,
            )

            try:
                db.session.add(payment)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))

            # RESPONSE DATA ======================================
            data = {
                "payment_id": payment.id,
                "order_id": payment.order_id,
                "package": package_code,
                "package_name": package["name"],
                "amount": int(payment.amount),
                "snap_token": payment.snap_token,
                "redirect_url": redirect_url,
                "transaction_status": payment.transaction_status,
            }

            return success_data(
                data=data,
                status_code=201
            )

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # CREATE SUBSCRIPTION PAYMENT ============================================================ End

    # HANDLE MIDTRANS NOTIFICATION ============================================================ Begin
    def handle_notification(datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas is None:
                return invalid_params()

            required_data = [
                "order_id",
                "status_code",
                "gross_amount",
                "transaction_status",
                "signature_key"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )
            # Checking Request Body ---------------------------------------- Finish

            # Initialize Notification Data ---------------------------------------- Start
            order_id = str(datas["order_id"])
            status_code = str(datas["status_code"])
            gross_amount = str(datas["gross_amount"])
            transaction_status = str(
                datas["transaction_status"]
            ).lower()

            signature_key = str(datas["signature_key"])

            transaction_id = datas.get("transaction_id")
            payment_type = datas.get("payment_type")

            fraud_status = str(
                datas.get("fraud_status", "")
            ).lower()
            # Initialize Notification Data ---------------------------------------- Finish

            # Signature Validation ---------------------------------------- Start
            signature_source = (
                order_id
                + status_code
                + gross_amount
                + current_app.config["MIDTRANS_SERVER_KEY"]
            )

            generated_signature = hashlib.sha512(
                signature_source.encode("utf-8")
            ).hexdigest()

            if not hmac.compare_digest(
                generated_signature,
                signature_key
            ):
                return authorization_error()
            # Signature Validation ---------------------------------------- Finish

            # Check Subscription Payment ---------------------------------------- Start
            payment = SubscriptionPayments.query.filter_by(
                order_id=order_id,
                is_delete=0
            ).with_for_update().first()

            if not payment:
                return not_found(
                    "Subscription payment could not be found."
                )
            # Check Subscription Payment ---------------------------------------- Finish

            # Amount Validation ---------------------------------------- Start
            try:
                notification_amount = Decimal(gross_amount)
                payment_amount = Decimal(payment.amount)

            except InvalidOperation:
                return parameter_error(
                    "Invalid gross amount."
                )

            if notification_amount != payment_amount:
                return parameter_error(
                    "Nominal pembayaran tidak sesuai."
                )
            # Amount Validation ---------------------------------------- Finish

            # Check Workshop ---------------------------------------- Start
            workshop = Workshops.query.filter_by(
                id=payment.workshop_id,
                is_delete=0
            ).first()

            if not workshop:
                return not_found(
                    "Workshop could not be found."
                )
            # Check Workshop ---------------------------------------- Finish

            # Payment Status Validation ---------------------------------------- Start
            previous_status = str(
                payment.transaction_status
            ).lower()

            already_paid = previous_status in [
                "settlement",
                "capture"
            ]

            fraud_accepted = fraud_status in [
                "",
                "accept"
            ]

            payment_success = (
                status_code == "200"
                and transaction_status in [
                    "settlement",
                    "capture"
                ]
                and fraud_accepted
            )

            # Prevent old notification from changing successful payment
            if already_paid and not payment_success:
                return success(status_code=200)
            # Payment Status Validation ---------------------------------------- Finish

            # Update Subscription Payment ---------------------------------------- Start
            timestamp = current_timestamp()

            payment.transaction_id = (
                transaction_id or payment.transaction_id
            )

            payment.payment_type = (
                payment_type or payment.payment_type
            )

            payment.transaction_status = transaction_status
            payment.updated_at = timestamp

            if payment_success and payment.paid_at is None:
                payment.paid_at = timestamp
            # Update Subscription Payment ---------------------------------------- Finish

            # Activate Subscription ---------------------------------------- Start
            if payment_success and not already_paid:
                duration_days = SUBSCRIPTION_PACKAGES[
                    "monthly"
                ]["duration_days"]

                duration_milliseconds = (
                    duration_days
                    * 24
                    * 60
                    * 60
                    * 1000
                )

                current_subscription_end = int(
                    workshop.subscription_end or 0
                )

                if current_subscription_end > timestamp:
                    subscription_start = current_subscription_end

                else:
                    subscription_start = timestamp

                workshop.subscription_status = 1
                workshop.subscription_end = (
                    subscription_start
                    + duration_milliseconds
                )

                workshop.updated_at = timestamp
            # Activate Subscription ---------------------------------------- Finish

            # Save Data ---------------------------------------- Start
            try:
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Save Data ---------------------------------------- Finish

            # Return Response ========================================
            return success(status_code=200)

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # HANDLE MIDTRANS NOTIFICATION ============================================================ End

    # READ SUBSCRIPTION STATUS ============================================================ Begin
    def read_status(user_role, workshop_id):
        try:
            # Access Validation ---------------------------------------- Start
            access = owner_validator(user_role)

            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Check Workshop ---------------------------------------- Start
            workshop = Workshops.query.filter_by(
                id=workshop_id,
                is_delete=0
            ).first()

            if not workshop:
                return not_found(
                    "Workshop could not be found."
                )
            # Check Workshop ---------------------------------------- Finish

            # Check Subscription Expiration ---------------------------------------- Start
            timestamp = current_timestamp()

            subscription_end = int(
                workshop.subscription_end or 0
            )

            if (
                int(workshop.subscription_status) == 1
                and subscription_end > 0
                and subscription_end <= timestamp
            ):
                workshop.subscription_status = 2
                workshop.updated_at = timestamp

                try:
                    db.session.commit()

                except Exception as e:
                    db.session.rollback()
                    return parameter_error(str(e))
            # Check Subscription Expiration ---------------------------------------- Finish

            # Initialize Subscription Status ---------------------------------------- Start
            status_labels = {
                0: "Belum Aktif",
                1: "Aktif",
                2: "Kedaluwarsa"
            }

            subscription_status = int(
                workshop.subscription_status or 0
            )

            remaining_days = 0

            if (
                subscription_status == 1
                and subscription_end > timestamp
            ):
                remaining_milliseconds = (
                    subscription_end - timestamp
                )

                milliseconds_per_day = 24 * 60 * 60 * 1000
                
                remaining_days = max(
                    1,
                    (
                        remaining_milliseconds
                        + milliseconds_per_day
                        - 1
                    ) // milliseconds_per_day
                )
            # Initialize Subscription Status ---------------------------------------- Finish

            # Get Latest Payment ---------------------------------------- Start
            latest_payment = SubscriptionPayments.query.filter_by(
                workshop_id=workshop.id,
                is_delete=0
            ).order_by(
                SubscriptionPayments.created_at.desc()
            ).first()

            payment_data = None

            if latest_payment:
                payment_data = {
                    "id": latest_payment.id,
                    "order_id": latest_payment.order_id,
                    "amount": int(latest_payment.amount),
                    "transaction_status": latest_payment.transaction_status,
                    "payment_type": latest_payment.payment_type,
                    "paid_at": latest_payment.paid_at,
                    "paid_at_format": format_datetime(
                        latest_payment.paid_at
                    ) if latest_payment.paid_at else "-"
                }
            # Get Latest Payment ---------------------------------------- Finish

            # Initialize Response Data ---------------------------------------- Start
            data = {
                "workshop_id": workshop.id,
                "workshop_name": workshop.workshop_name,
                "subscription_status": subscription_status,
                "subscription_status_label": status_labels.get(
                    subscription_status,
                    "Tidak Diketahui"
                ),
                "subscription_end": (
                    subscription_end
                    if subscription_end > 0
                    else None
                ),
                "subscription_end_format": (
                    format_datetime(subscription_end)
                    if subscription_end > 0
                    else "-"
                ),
                "remaining_days": int(remaining_days),
                "latest_payment": payment_data
            }
            # Initialize Response Data ---------------------------------------- Finish

            # Return Response ========================================
            return success_data(
                data=data,
                status_code=200
            )

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # READ SUBSCRIPTION STATUS ============================================================ End

    # SYNC PAYMENT STATUS ============================================================ Begin
    def sync_status(user_role, workshop_id):
        try:
            # Access Validation ---------------------------------------- Start
            access = owner_validator(user_role)

            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Check Workshop ---------------------------------------- Start
            workshop = Workshops.query.filter_by(
                id=workshop_id,
                is_delete=0
            ).first()

            if not workshop:
                return not_found(
                    "Workshop could not be found."
                )
            # Check Workshop ---------------------------------------- Finish

            # Get Latest Payment ---------------------------------------- Start
            payment = SubscriptionPayments.query.filter_by(
                workshop_id=workshop.id,
                is_delete=0
            ).order_by(
                SubscriptionPayments.created_at.desc()
            ).first()

            if not payment:
                return not_found(
                    "Subscription payment could not be found."
                )
            # Get Latest Payment ---------------------------------------- Finish

            # Get Status From Midtrans ---------------------------------------- Start
            snap = get_snap()

            status_response = snap.transactions.status(
                payment.order_id
            )

            if not status_response:
                return bad_request(
                    "Gagal mendapatkan status transaksi dari Midtrans."
                )

            response_order_id = str(
                status_response.get("order_id", "")
            )

            if response_order_id != payment.order_id:
                return parameter_error(
                    "Order ID transaksi tidak sesuai."
                )
            # Get Status From Midtrans ---------------------------------------- Finish

            # Process Transaction Status ---------------------------------------- Start
            process_response = (
                SubscriptionModels.handle_notification(
                    status_response
                )
            )

            if process_response.status_code != 200:
                return process_response
            # Process Transaction Status ---------------------------------------- Finish

            # Reload Updated Data ---------------------------------------- Start
            db.session.expire_all()

            updated_payment = (
                SubscriptionPayments.query.filter_by(
                    order_id=payment.order_id,
                    is_delete=0
                ).first()
            )

            updated_workshop = Workshops.query.filter_by(
                id=workshop.id,
                is_delete=0
            ).first()
            # Reload Updated Data ---------------------------------------- Finish

            # Initialize Response Data ---------------------------------------- Start
            subscription_end = int(
                updated_workshop.subscription_end or 0
            )

            data = {
                "order_id": updated_payment.order_id,
                "transaction_status": (
                    updated_payment.transaction_status
                ),
                "transaction_id": (
                    updated_payment.transaction_id
                ),
                "payment_type": (
                    updated_payment.payment_type
                ),
                "paid_at": updated_payment.paid_at,
                "subscription_status": int(
                    updated_workshop.subscription_status or 0
                ),
                "subscription_end": (
                    subscription_end
                    if subscription_end > 0
                    else None
                ),
                "subscription_end_format": (
                    format_datetime(subscription_end)
                    if subscription_end > 0
                    else "-"
                )
            }
            # Initialize Response Data ---------------------------------------- Finish

            # Return Response ========================================
            return success_data(
                data=data,
                status_code=200
            )

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # SYNC PAYMENT STATUS ============================================================ End

    # READ PAYMENT HISTORY ============================================================ Begin
    def read_history(user_role, workshop_id):
        try:
            # Access Validation ---------------------------------------- Start
            access = owner_validator(user_role)

            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Check Workshop ---------------------------------------- Start
            workshop = Workshops.query.filter_by(
                id=workshop_id,
                is_delete=0
            ).first()

            if not workshop:
                return not_found(
                    "Workshop could not be found."
                )
            # Check Workshop ---------------------------------------- Finish

            # Get Subscription Payments ---------------------------------------- Start
            payments = SubscriptionPayments.query.filter_by(
                workshop_id=workshop.id,
                is_delete=0
            ).order_by(
                SubscriptionPayments.created_at.desc()
            ).all()
            # Get Subscription Payments ---------------------------------------- Finish

            # Initialize Payment Status ---------------------------------------- Start
            status_labels = {
                "pending": "Menunggu Pembayaran",
                "settlement": "Berhasil",
                "capture": "Berhasil",
                "cancel": "Dibatalkan",
                "deny": "Ditolak",
                "expire": "Kedaluwarsa",
                "refund": "Dikembalikan"
            }

            payment_type_labels = {
                "bank_transfer": "Transfer Bank",
                "credit_card": "Kartu Kredit",
                "gopay": "GoPay",
                "qris": "QRIS",
                "shopeepay": "ShopeePay",
                "cstore": "Convenience Store",
                "echannel": "Mandiri Bill Payment"
            }
            # Initialize Payment Status ---------------------------------------- Finish

            # Initialize Response Data ---------------------------------------- Start
            history = []

            for payment in payments:
                transaction_status = str(
                    payment.transaction_status or ""
                ).lower()

                payment_type = str(
                    payment.payment_type or ""
                ).lower()

                history.append({
                    "id": payment.id,
                    "order_id": payment.order_id,
                    "transaction_id": (
                        payment.transaction_id or "-"
                    ),
                    "amount": int(payment.amount),
                    "amount_format": format_rupiah(
                        payment.amount
                    ),
                    "payment_type": (
                        payment.payment_type or "-"
                    ),
                    "payment_type_label": (
                        payment_type_labels.get(
                            payment_type,
                            payment.payment_type or "-"
                        )
                    ),
                    "transaction_status": (
                        transaction_status
                    ),
                    "transaction_status_label": (
                        status_labels.get(
                            transaction_status,
                            transaction_status or "-"
                        )
                    ),
                    "paid_at": payment.paid_at,
                    "paid_at_format": (
                        format_datetime(payment.paid_at)
                        if payment.paid_at
                        else "-"
                    ),
                    "created_at": payment.created_at,
                    "created_at_format": format_datetime(
                        payment.created_at
                    )
                })
            # Initialize Response Data ---------------------------------------- Finish

            # Return Response ========================================
            return success_data(
                data={
                    "total": len(history),
                    "history": history
                },
                status_code=200
            )

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # READ PAYMENT HISTORY ============================================================ End
# **************************************************************
# SUBSCRIPTION MODEL CLASS | END
# **************************************************************