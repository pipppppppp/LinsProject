from flask import Blueprint, request, render_template, session, redirect, url_for
from datetime import datetime
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
        purchases=purchases,
        active_menu="purchase"
    )

# ROUTE MENYIMPAN PEMBELIAN
@purchase.post('/add')
def addPurchase():

    try:

        # MENGAMBIL DATA JSON DARI JAVASCRIPT
        body = request.json

        # ID SUPPLIER YANG DIPILIH
        supplier_id = body['supplier_id']

        # TOTAL SELURUH PEMBELIAN
        total = body['total']

        # DETAIL BARANG YANG DIBELI
        details = body['details']

        # SIMPAN DATA KE TABEL PURCHASES
        purchase = Purchases(

            supplier_id=supplier_id,

            tanggal=int(time.time()),

            total=total,

            created_at=int(time.time()),

            updated_at=int(time.time())
        )

        # MENAMBAHKAN DATA KE SESSION SQLALCHEMY
        db.session.add(purchase)

        # MEMBUAT ID PURCHASE TANPA COMMIT
        db.session.flush()

            # LOOPING SEMUA BARANG YANG DIBELI
        for item in details:
            # SIMPAN KE TABEL PURCHASE DETAILS
            detail = PurchaseDetails(

                # ID PEMBELIAN
                purchase_id=purchase.id,

                # ID BARANG
                item_id=item['item_id'],

                # JUMLAH BARANG
                qty=item['qty'],

                # HARGA BELI
                harga_beli=item['harga_beli'],

                # TOTAL PER BARANG
                subtotal=item['subtotal']
            )

            # SIMPAN KE SESSION
            db.session.add(detail)

                        # AMBIL DATA BARANG DARI DATABASE
            item_data = Items.query.get(
                item['item_id']
            )

            # MENAMBAHKAN STOK
            item_data.stok += int(
                item['qty']
            )

        # MENYIMPAN SEMUA PERUBAHAN KE DATABASE
        db.session.commit()

        return {
            "status": True,
            "message": "Pembelian berhasil disimpan"
        }

    except Exception as e:

        # MEMBATALKAN SEMUA PERUBAHAN
        db.session.rollback()

        return {
            "status": False,
            "message": str(e)
        }, 500

@purchase.get('/history')
def history():

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
        template_name_or_list='purchase_history.html',
        title='Riwayat Pembelian',
        purchases=purchases,
        active_menu="purchase_history"
    )

@purchase.get('/detail/<int:id>')
def detail(id):

    if 'user_id' not in session:
        return redirect(
            url_for('auth.signin_page')
        )

    details = PurchaseDetails.query.filter_by(
        purchase_id=id
    ).all()

    for detail in details:

        detail.item = Items.query.get(
            detail.item_id
        )

    return render_template(
        template_name_or_list='purchase_detail.html',
        title='Detail Pembelian',
        details=details,
        active_menu="purchase_detail"
    )