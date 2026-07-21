from flask import Blueprint, request, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt

from ..models.purchase import PurchaseModels
from ...utilities.responseHelpers import bad_request

# BLUEPRINT ================================================== Begin
purchase = Blueprint(
    name='purchase',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/purchase',
)
# BLUEPRINT ================================================== End

# CUSTOMER PAGE ============================================================ Begin
# [GET] https://127.0.0.1:5000/purchase/
@purchase.get('/')
@jwt_required()
def index():
    try:
        return render_template(
            title='Purchase - POS Bengkel',
            template_name_or_list='purchase.html',
            active_menu="purchase",
        )
    except Exception as e:
        return bad_request(str(e))
# CUSTOMER PAGE ============================================================ End

# CREATE PURCHASE ============================================================ Begin
@purchase.post("/add")
@jwt_required()
def create_purchase():
    claims = get_jwt()

    return PurchaseModels.create_purchase(
        claims["role"],
        claims["ws_id"],
        request.get_json()
    )
# CREATE PURCHASE ============================================================ End

# READ PURCHASE ============================================================ Begin
# GET https://127.0.0.1:5000/purchase/view
@purchase.get("/view")
@jwt_required()
def read_purchase():
    claims = get_jwt()

    return PurchaseModels.read_purchase(
        claims["role"],
        claims["ws_id"]
    )
# READ PURCHASE ============================================================ End

# READ PURCHASE DETAIL ============================================================ Begin
# [PUT] https://127.0.0.1:5000/purchase/detail/<id>
@purchase.get("/detail/<int:id>")
@jwt_required()
def read_purchase_detail(id):
    claims = get_jwt()

    return PurchaseModels.read_purchase_detail(
        claims["role"],
        claims["ws_id"],
        id
    )
# READ PURCHASE DETAIL ============================================================ End

# UPDATE PURCHASE ============================================================ Begin
# [PUT] https://127.0.0.1:5000/purchase/edit/<id>
@purchase.put("/edit/<int:id>")
@jwt_required()
def update_purchase(id):
    claims = get_jwt()

    return PurchaseModels.update_purchase(
        claims["role"],
        claims["ws_id"],
        id,
        request.get_json()
    )
# UPDATE PURCHASE ============================================================ End

# DELETE PURCHASE ============================================================ Begin
# [DELETE] https://127.0.0.1:5000/purchase/delete/<id>
@purchase.delete("/delete/<int:id>")
@jwt_required()
def delete_purchase(id):
    claims = get_jwt()

    return PurchaseModels.delete_purchase(
        claims["role"],
        claims["ws_id"],
        id
    )
# DELETE PURCHASE ============================================================ End

# IMPORT PURCHASE ============================================================ Begin
# [DELETE] https://127.0.0.1:5000/customer/import
@purchase.post("/import")
@jwt_required()
def import_purchase():
    try:
        # Get JWT ---------------------------------------- Start
        claims = get_jwt()
        # Get JWT ---------------------------------------- Finish

        # Get Request ---------------------------------------- Start
        supplier_id = request.form.get("supplier_id")
        purchase_date = request.form.get("purchase_date")
        file = request.files.get("file")
        # Get Request ---------------------------------------- Finish

        # Return Response ========================================
        return PurchaseModels.import_purchase(
            claims["role"],
            claims["ws_id"],
            supplier_id,
            purchase_date,
            file
        )

    except Exception as e:
        return bad_request(str(e))
# IMPORT PURCHASE ============================================================ End

# @purchase.route("/history")
# @jwt_required()
# def history():
#     try:

#         return render_template(
#             "purchase_history.html",
#             title="Riwayat Pembelian - POS Bengkel",
#             active_menu="purchase_history",
#         )
        
#     except Exception as e:
#         return {
#             "status": False,
#             "message": str(e)
#         }, 500