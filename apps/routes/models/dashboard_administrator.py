from sqlalchemy import func

from apps import db
from apps.database.db_workshops import Workshops
from apps.database.db_subscription_payment import (
    SubscriptionPayments,
)

from apps.utilities.responseHelpers import *
from apps.utilities.validators import administrator_validator


# DASHBOARD ADMINISTRATOR MODEL CLASS ============================================================ Begin
class DashboardAdministratorModels():

    # DASHBOARD SUMMARY ============================================================ Begin
    def dashboard_summary(user_role):
        try:
            # Access Validation ---------------------------------------- Start
            access = administrator_validator(
                user_role
            )

            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Workshop Summary ---------------------------------------- Start
            total_workshop = Workshops.query.filter_by(
                is_delete=0
            ).count()

            active_workshop = Workshops.query.filter_by(
                is_delete=0,
                is_active=1
            ).count()

            inactive_workshop = Workshops.query.filter_by(
                is_delete=0,
                is_active=0
            ).count()
            # Workshop Summary ---------------------------------------- Finish

            # Subscription Revenue ---------------------------------------- Start
            total_revenue = db.session.query(
                func.coalesce(
                    func.sum(
                        SubscriptionPayments.amount
                    ),
                    0
                )
            ).filter(
                SubscriptionPayments.is_delete == 0,
                SubscriptionPayments.transaction_status.in_([
                    "settlement",
                    "capture",
                    "success"
                ])
            ).scalar()
            # Subscription Revenue ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            response = {
                "total_workshop": total_workshop,
                "active_workshop": active_workshop,
                "inactive_workshop": inactive_workshop,
                "total_revenue": int(
                    total_revenue or 0
                )
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ========================================
            return success_data(response)

        except Exception as e:
            return bad_request(str(e))
    # DASHBOARD SUMMARY ============================================================ End

# DASHBOARD ADMINISTRATOR MODEL CLASS ============================================================ End