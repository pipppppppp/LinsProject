from flask import Blueprint, render_template
from flask_jwt_extended import get_jwt, jwt_required

from apps.utilities.responseHelpers import bad_request

from ..models.dashboard_administrator import (
    DashboardAdministratorModels,
)


# BLUEPRINT ============================================================ Begin
dashboard_administrator = Blueprint(
    name="dashboard_administrator",
    import_name=__name__,
    template_folder="../../templates/pages/adminPages",
    url_prefix="/dashboard-administrator",
)
# BLUEPRINT ============================================================ End


# DASHBOARD ADMINISTRATOR PAGE ============================================================ Begin
# GET http://127.0.0.1:5000/dashboard-administrator/
@dashboard_administrator.get("/")
@jwt_required()
def index():
    try:
        # Return Page ========================================
        return render_template(
            template_name_or_list=(
                "dashboard_administrator.html"
            ),
            title=(
                "Dashboard Administrator - POS Bengkel"
            ),
            active_menu=(
                "dashboard_administrator"
            ),
        )

    except Exception as e:
        return bad_request(str(e))
# DASHBOARD ADMINISTRATOR PAGE ============================================================ End


# DASHBOARD SUMMARY ============================================================ Begin
# GET http://127.0.0.1:5000/dashboard-administrator/summary
@dashboard_administrator.get("/summary")
@jwt_required()
def dashboard_summary():
    try:
        # JWT Access Data ========================================
        role = str(
            get_jwt()["role"]
        )

        # Request Process ========================================
        response = (
            DashboardAdministratorModels
            .dashboard_summary(
                role
            )
        )

        # Return Response ========================================
        return response

    except Exception as e:
        return bad_request(str(e))
# DASHBOARD SUMMARY ============================================================ End