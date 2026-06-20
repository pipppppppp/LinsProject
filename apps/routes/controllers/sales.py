from flask import Blueprint, request, render_template, session, redirect, url_for
from datetime import datetime
from ... import db

from ...database.db_sales import Sales
from ...database.db_sale_details import SaleDetails
from ...database.db_services import Services
from ...database.db_sale_service_details import SaleServiceDetails
from ...database.db_customer import Customers
from ...database.db_items import Items

import time

sales = Blueprint(
    name='sales',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/sales',
)

@sales.get('/')
def index():

    # Cek login
    if 'user_id' not in session:
        return redirect(
            url_for('auth.signin_page')
        )

    # Ambil customer
    customers = Customers.query.filter_by(
        is_delete=0
    ).all()

    # Ambil barang
    items = Items.query.filter_by(
        is_delete=0
    ).all()

    # Ambil service
    services = Services.query.filter_by(
        is_delete=0
    ).all()

    return render_template(
        template_name_or_list='sales.html',
        title='Penjualan Barang',
        customers=customers,
        items=items,
        services=services,
        current_date=datetime.now().strftime("%Y-%m-%d"),
        active_menu="sales"
    )

@sales.post('/add')
def addSales():

    try:

        # Ambil data dari javascript
        body = request.json

        # Customer yang dipilih
        customer_id = body['customer_id']

        tanggal = int(
            datetime.strptime(
                body['tanggal'],
                "%Y-%m-%d"
            ).timestamp()
        )

        # Total penjualan
        total = body['total']

        # Detail barang
        details = body['details']

        # Detail Jasa
        service_details = body.get('service_details',[])

        # Simpan header penjualan
        sale = Sales(

            customer_id=customer_id,

            tanggal=tanggal,

            total=total,

            created_at=int(time.time()),

            updated_at=int(time.time())

        )

        db.session.add(sale)

        # Buat ID sale tanpa commit
        db.session.flush()

        # Validasi stok terlebih dahulu
        for item in details:

            item_data = Items.query.get(
                item['item_id']
            )

            qty = int(
                item['qty']
            )

            if item_data.stok < qty:

                return {
                    "status": False,
                    "message": f"Stok {item_data.nama_barang} tidak mencukupi"
                }, 400

        # Simpan detail penjualan
        for item in details:

            detail = SaleDetails(

                sale_id=sale.id,

                item_id=item['item_id'],

                qty=item['qty'],

                harga_jual=item['harga_jual'],

                subtotal=item['subtotal']

            )

            db.session.add(detail)

            # Ambil barang
            item_data = Items.query.get(
                item['item_id']
            )

            # Kurangi stok
            item_data.stok -= int(
                item['qty']
            )

        # Simpan detail jasa
        for service in service_details:

            detail_service = SaleServiceDetails(

                sale_id=sale.id,

                service_id=service['service_id'],

                qty=service['qty'],

                harga_jasa=service['harga_jasa'],

                subtotal=service['subtotal']

            )

            db.session.add(
                detail_service
            )

        db.session.commit()

        return {
            "status": True,
            "message": "Penjualan berhasil disimpan"
        }

    except Exception as e:

        db.session.rollback()

        return {
            "status": False,
            "message": str(e)
        }, 500

@sales.get('/history')
def history():

    # Cek login
    if 'user_id' not in session:
        return redirect(
            url_for('auth.signin_page')
        )

    # Ambil semua penjualan
    sales_data = Sales.query.filter_by(
        is_delete=0
    ).all()

    # Ambil customer
    for sale in sales_data:

        sale.customer = Customers.query.get(
            sale.customer_id
        )
    
        sale.tanggal_format = datetime.fromtimestamp(
            sale.tanggal
        ).strftime("%d-%m-%Y")

        sale.total_format = f"Rp {sale.total:,}".replace(",", ".")
        
    return render_template(
        template_name_or_list='sales_history.html',
        title='Riwayat Penjualan',
        sales=sales_data,
        active_menu="sales_history"
    )

@sales.get('/detail/<int:id>')
def detail(id):

    # Cek login
    if 'user_id' not in session:
        return redirect(
            url_for('auth.signin_page')
        )

    # Ambil detail penjualan barang
    details = SaleDetails.query.filter_by(
        sale_id=id
    ).all()

    # Ambil data barang
    for detail in details:

        detail.item = Items.query.get(
            detail.item_id
        )

    # Ambil detail penjualan jasa
    service_details = SaleServiceDetails.query.filter_by(
        sale_id=id
    ).all()

    # Ambil data jasa
    for service in service_details:
    
        service.service = Services.query.get(
            service.service_id
        )

    return render_template(
        template_name_or_list='sales_detail.html',
        title='Detail Penjualan',
        details=details,
        service_details=service_details
    )