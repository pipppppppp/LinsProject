from flask import Blueprint, render_template, session, redirect, url_for
from datetime import datetime

from ...database.db_purchases import Purchases
from ...database.db_suppliers import Suppliers
from ...database.db_sales import Sales
from ...database.db_customer import Customers
from ...database.db_items import Items
from ...database.db_categories import Categories

report = Blueprint(
    name='report',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/report',
)

@report.get('/purchase')
def purchase_report():

    if 'user_id' not in session:
        return redirect(
            url_for('auth.signin_page')
        )

    purchases = Purchases.query.filter_by(
        is_delete=0
    ).all()

    for purchase in purchases:

        purchase.supplier = Suppliers.query.get(
            purchase.supplier_id
        )

        purchase.tanggal_format = datetime.fromtimestamp(
            purchase.tanggal
        ).strftime("%d-%m-%Y")

    return render_template(
        template_name_or_list='report_purchase.html',
        title='Laporan Pembelian',
        purchases=purchases,
        active_menu="purchase_report"
    )

@report.get('/sales')
def sales_report():

    if 'user_id' not in session:
        return redirect(
            url_for('auth.signin_page')
        )

    sales = Sales.query.filter_by(
        is_delete=0
    ).all()

    for sale in sales:

        sale.customer = Customers.query.get(
            sale.customer_id
        )

        sale.tanggal_format = datetime.fromtimestamp(
            sale.tanggal
        ).strftime("%d-%m-%Y")

    return render_template(
        template_name_or_list='report_sales.html',
        title='Laporan Penjualan',
        sales=sales,
        active_menu="sales_report"
    )

@report.get('/stock')
def stock_report():

    if 'user_id' not in session:
        return redirect(
            url_for('auth.signin_page')
        )

    items = Items.query.filter_by(
        is_delete=0
    ).all()

    for item in items:
    
        item.category = Categories.query.get(
            item.category_id
    )

    return render_template(
        template_name_or_list='report_stock.html',
        title='Laporan Stok Barang',
        items=items,
        active_menu="stock_report"
    )