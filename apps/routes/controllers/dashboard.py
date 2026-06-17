from flask import Blueprint, request, redirect, url_for, render_template, session
from flask import current_app as app
from flask_jwt_extended import jwt_required

from ..models.signin import SigninModels
from ...utilities.forms import SigninForm

from ...database.db_items import Items
from ...database.db_customer import Customers
from ...database.db_suppliers import Suppliers
from ...database.db_purchases import Purchases
from ...database.db_sales import Sales

# BLUEPRINT ================================================== Begin
dashboard = Blueprint(
    name='dashboard',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/dashboard',
)
# BLUEPRINT ================================================== End

# DASHBOARD PAGE ============================================================ Begin
# GET https://127.0.0.1:5000/dashboard/
@dashboard.get('/')
def index():
    try:
        # Return Page ======================================== 
        # return redirect(url_for('dashboard'))
        if 'user_id' not in session:
    
            return redirect(
                url_for('auth.signin_page')
            )

        # Total data
        total_items = Items.query.filter_by(
            is_delete=0
        ).count()

        total_customers = Customers.query.filter_by(
            is_delete=0
        ).count()

        total_suppliers = Suppliers.query.filter_by(
            is_delete=0
        ).count()

        total_transactions = (
            Purchases.query.filter_by(is_delete=0).count()
            +
            Sales.query.filter_by(is_delete=0).count()
        )

        low_stock = Items.query.filter(
            Items.stok <= 5
        ).all()

        return render_template(
            title='Dashboard POS Bengkel',
            template_name_or_list='dashboard.html',

            username=session.get('username'),

            total_items=total_items,
            total_customers=total_customers,
            total_suppliers=total_suppliers,
            total_transactions=total_transactions,
            low_stock=low_stock
        )

    except Exception as e:
        # return bad_request(str(e))
        # return "gagal boss! Durung dadi:)"
        return render_template(
            title="Error $04 - Aplikasi e Hel",
            template_name_or_list='errorPages/404.html'
        )
# SIGNIN PAGE ============================================================ End
