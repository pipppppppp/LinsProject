from flask import Blueprint, request, render_template, session, redirect, url_for
from datetime import datetime
from ... import db
import pandas as pd

from ...database.db_purchases import Purchases
from ...database.db_purchase_details import PurchaseDetails
from ...database.db_suppliers import Suppliers
from ...database.db_products import Products

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
    # Protrksi role
    if session.get('role') != 'admin':
        return redirect(
            url_for('dashboard.index')
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
        current_date=datetime.now().strftime("%Y-%m-%d"),
        active_menu="purchase"
    )

# IMPORT FILE PEMBELIAN
@purchase.post('/import')
def import_purchase():

    try:

        file = request.files['file']

        df = pd.read_excel(file)

        data = []

        for _, row in df.iterrows():

            data.append({

                "nama_barang": row["nama_barang"],
                "qty": int(row["qty"]),
                "harga_beli": int(row["harga_beli"])

            })

        return {

            "status": True,
            "data": data

        }

    except Exception as e:

        return {

            "status": False,
            "message": str(e)

        }, 500

# ROUTE MENYIMPAN PEMBELIAN
@purchase.post('/add')
def addPurchase():

    try:

        # MENGAMBIL DATA JSON DARI JAVASCRIPT
        body = request.json

        supplier_id = body['supplier_id']

        tanggal = int(
            datetime.strptime(
                body['tanggal'],
                "%Y-%m-%d"  
            ).timestamp()
        )

        total = body['total']

        details = body['details']

        # SIMPAN DATA KE TABEL PURCHASES
        purchase = Purchases(
            admin_id=session.get(
                'user_id'
            ),
            
            supplier_id=supplier_id,

            tanggal=tanggal,

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