from flask import Blueprint, render_template, session, redirect, url_for
from flask import current_app as app
from flask_jwt_extended import jwt_required, get_jwt

from datetime import datetime, timedelta

from ...database.db_workshops import Workshops
from ...database.db_users import Users
from ...database.db_products import Products
from ...database.db_customers import Customers
from ...database.db_suppliers import Suppliers
from ...database.db_purchases import Purchases
from ...database.db_payment import Payments
from ...routes.controllers.report import calculate_profit

# BLUEPRINT ================================================== Begin
dashboard = Blueprint(
    name='dashboard',
    import_name=__name__,
    template_folder="../../templates/pages/adminPages",
    url_prefix='/dashboard',
)
# BLUEPRINT ================================================== End

# DASHBOARD PAGE ============================================================ Begin
# GET https://127.0.0.1:5000/dashboard/
@dashboard.get('/')
@jwt_required()
def index():
    try:
        claims = get_jwt()

        if claims["role"] == 0:
            return redirect(url_for("administrator.dashboard"))
        elif claims["role"] == 1:
            return render_template("dashboard.html")   # atau dashboard.index
        # elif claims["role"] == 2:
        #     return redirect(url_for("cashier.index"))
        workshop = Workshops.query.filter_by(
            owner_id=claims["id"],
            is_delete=0
        ).first()

        role_map = {
            0: "Administrator",
            1: "Owner",
            2: "Kasir"
        }
        print(workshop.is_active)
        print(type(workshop.is_active)) 
        return render_template(
            "dashboard.html",
            title="Dashboard POS Bengkel",
            active_menu="dashboard",

            username=claims["name"],
            email=claims["email"],
            role_name=role_map.get(int(claims["role"]), "-"),
            is_active=1,
            workshop_status=workshop.is_active if workshop else 0
        )
        # Return Page ======================================== 
        # return redirect(url_for('dashboard'))
        # if 'user_id' not in session:
    
        #     return redirect(
        #         url_for('auth.signin_page')
        #     )

        # Total data
        # total_items = Products.query.filter_by(
        #     is_delete=0
        # ).count()

        # total_customers = Customers.query.filter_by(
        #     is_delete=0
        # ).count()

        # total_suppliers = Suppliers.query.filter_by(
        #     is_delete=0
        # ).count()

        # total_transactions = (
        #     Purchases.query.filter_by(is_delete=0).count()
        #     +
        #     Payment.query.filter_by(is_delete=0).count()
        # )

        # low_stock = Products.query.filter(
        #     Products.stok <= 5
        # ).all()

        # =====================================
        # DASHBOARD SUMMARY
        # =====================================

        # now = datetime.now()

        # start_today = datetime(
        #     now.year,
        #     now.month,
        #     now.day
        # )

        # end_today = start_today + timedelta(
        #     days=1
        # )

        # sales_today = Payment.query.filter(
        #     Payment.tanggal.between(
        #         int(start_today.timestamp()),
        #         int(end_today.timestamp())
        #     )
        # ).all()

        # penjualan_hari_ini = sum(
        #     sale.total
        #     for sale in sales_today
        # )

        # purchases_today = Purchases.query.filter(
        #     Purchases.tanggal.between(
        #         int(start_today.timestamp()),
        #         int(end_today.timestamp())
        #     )
        # ).all()

        # pembelian_hari_ini = sum(
        #     purchase.total
        #     for purchase in purchases_today
        # )

        # start_month = datetime(
        #     now.year,
        #     now.month,
        #     1
        # )

        # if now.month == 12:

        #     end_month = datetime(
        #         now.year + 1,
        #         1,
        #         1
        #     )

        # else:

        #     end_month = datetime(
        #         now.year,
        #         now.month + 1,
        #         1
        #     )

        # sales_month = Payment.query.filter(
        #     Payment.tanggal.between(
        #         int(start_month.timestamp()),
        #         int(end_month.timestamp())
        #     )
        # ).all()

        # sale_ids = [
        #     sale.id
        #     for sale in sales_month
        # ]

        # profit = calculate_profit(
        #     sale_ids
        # )

        # omset_bulan = profit["omset"]
        # laba_bulan = profit["laba_bersih"]
       

        # =====================================
        # END DASHBOARD SUMMARY
        # =====================================

        # return render_template(

        #     title='Dashboard POS Bengkel',

        #     template_name_or_list='dashboard.html',

        #     active_menu="dashboard",

        #     username=session.get('username'),

        #     total_items=total_items,

        #     total_customers=total_customers,

        #     total_suppliers=total_suppliers,

        #     total_transactions=total_transactions,

        #     low_stock=low_stock,

        #     penjualan_hari_ini=penjualan_hari_ini,

        #     pembelian_hari_ini=pembelian_hari_ini,

        #     omset_bulan=omset_bulan,

        #     laba_bulan=laba_bulan
        # )

    except Exception as e:
        # return bad_request(str(e))
        # return "gagal boss! Durung dadi:)"
        # return render_template(
        #     title="Error $04 - Aplikasi e Hel",
        #     template_name_or_list='errorPages/404.html'
        # )
        
        print("ERROR DASHBOARD =", e)
        raise e
# DASHBOARD PAGE ============================================================ End
