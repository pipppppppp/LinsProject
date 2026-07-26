from flask import Blueprint, request, render_template
from flask_jwt_extended import jwt_required, get_jwt

from ..models.cashier import CashierModels
from ...utilities.responseHelpers import bad_request

# BLUEPRINT ================================================== Begin
cashier = Blueprint(
    name='cashier',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/cashier',
)
# BLUEPRINT ================================================== End

print(cashier.template_folder)
# CASHIER PAGE ============================================================ Begin
@cashier.get('/')
@jwt_required()
def index():
    try:

        return render_template(
            title="Kasir - POS Bengkel",
            template_name_or_list="cashier.html",
            active_menu="cashier",
        )

    except Exception as e:
        return bad_request(str(e))
# CASHIER PAGE ============================================================ End

# CASHIER PAGE ============================================================ Begin
@cashier.get("/customer")
@jwt_required()
def customer():
    try:

        return render_template(
            title="Kasir - POS Bengkel",
            template_name_or_list="customer_cashier.html",
            active_menu="customer",
        )

    except Exception as e:
        return bad_request(str(e))

# CASHIER PAGE ============================================================ End

# SEARCH ITEM ============================================================ Begin
@cashier.get("/search")
@jwt_required()
def search_item():
    try:
        claims = get_jwt()
        ws_id = int(get_jwt()["ws_id"])

        keyword = request.args.get("keyword", "").strip()

        return CashierModels.search_items(
            keyword,
            ws_id
        )

    except Exception as e:
        return bad_request(str(e))
# SEARCH ITEM ============================================================ End

# CHECKOUT ============================================================ Begin
@cashier.post("/checkout")
@jwt_required()
def checkout():
    try:
        claims = get_jwt()
        ws_id = int(get_jwt()["ws_id"])
        
        body = request.json

        return CashierModels.checkout(body)

    except Exception as e:
        return bad_request(str(e))
# CHECKOUT ============================================================ End

# PRINT RECEIPT ============================================================ Begin
@cashier.get("/receipt/<int:payment_id>")
@jwt_required()
def receipt(payment_id):
    try:
        claims = get_jwt()
        ws_id = int(get_jwt()["ws_id"])

        return CashierModels.print_receipt(
            payment_id,
            ws_id
        )

    except Exception as e:
        return bad_request(str(e))
# PRINT RECEIPT ============================================================ End

# HISTORY SALES CASHIER PAGE ============================================================ Begin
# [GET] https://127.0.0.1:5000//cashier/history-sales
@cashier.get("/history-sales")
@jwt_required()
def history_sales():
    try:
        return render_template(
            title="History Sales - POS Bengkel",
            template_name_or_list="cashier_history_sales.html",
            active_menu="history_sales",
        )

    except Exception as e:
        return bad_request(str(e))
# HISTORY CASHIER PAGE ============================================================ End
