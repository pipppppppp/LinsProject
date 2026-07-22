from flask import Blueprint, request, render_template
from flask_jwt_extended import jwt_required, get_jwt

from ..models.cashier import CashierModels
from ...utilities.responseHelpers import bad_request

# BLUEPRINT ================================================== Begin
cashier = Blueprint(
    name='cashier',
    import_name=__name__,
    template_folder="././templates/pages/adminPages",
    url_prefix='/cashier',
)
# BLUEPRINT ================================================== End


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

# HISTORY ============================================================ Begin
@cashier.get("/history")
@jwt_required()
def history():
    try:
        claims = get_jwt()
        ws_id = int(get_jwt()["ws_id"])

        return CashierModels.history(ws_id)

    except Exception as e:
        return bad_request(str(e))
# HISTORY ============================================================ End

# DETAIL ============================================================ Begin
@cashier.get("/detail/<int:payment_id>")
@jwt_required()
def detail(payment_id):
    try:
        claims = get_jwt()
        ws_id = int(get_jwt()["ws_id"])

        return CashierModels.detail(
            payment_id,
            ws_id
        )

    except Exception as e:
        return bad_request(str(e))
# DETAIL ============================================================ End

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