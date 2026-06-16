from flask import Blueprint, request, render_template, session, redirect, url_for

from ... import db

from ...database.db_purchases import Purchases
from ...database.db_purchase_details import PurchaseDetails
from ...database.db_suppliers import Suppliers
from ...database.db_items import Items

import time

purchase = Blueprint(
    name='purchase',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/purchase',
)

@purchase.get('/')
def index():

    if 'user_id' not in session:
        return redirect(
            url_for('auth.signin_page')
        )

    suppliers = Suppliers.query.filter_by(
        is_delete=0
    ).all()

    items = Items.query.filter_by(
        is_delete=0
    ).all()

    purchases = Purchases.query.filter_by(
        is_delete=0
    ).all()

    return render_template(
        template_name_or_list='purchase.html',
        title='Pembelian Barang',
        suppliers=suppliers,
        items=items,
        purchases=purchases
    )