from flask import Blueprint, render_template, session, redirect, url_for, request
from datetime import datetime, timedelta

from ...database.db_purchases import Purchases
from ...database.db_suppliers import Suppliers
from ...database.db_sales import Sales
from ...database.db_sale_details import SaleDetails
from ...database.db_sale_service_details import SaleServiceDetails
from ...database.db_customer import Customers
from ...database.db_items import Items
from ...database.db_categories import Categories

# Library import pdf
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from flask import make_response


report = Blueprint(
    name='report',
    import_name=__name__,
    template_folder="../../templates/pages/appPages",
    url_prefix='/report',
)

# ==========================
# HELPER FUNCTION
# ==========================

# Filter Periode
def filter_sales_by_periode(
    sales,
    periode,
    start_date,
    end_date
):

    if periode == "today":

        now = datetime.now()

        start = datetime(
            now.year,
            now.month,
            now.day
        )

        end = start + timedelta(
            days=1
        )

        sales = sales.filter(
            Sales.tanggal.between(
                int(start.timestamp()),
                int(end.timestamp())
            )
        )
    elif periode == "week":
    
        now = datetime.now()

        start = now - timedelta(
            days=now.weekday()
        )

        start = datetime(
            start.year,
            start.month,
            start.day
        )

        end = start + timedelta(
            days=7
        )

        sales = sales.filter(
            Sales.tanggal.between(
                int(start.timestamp()),
                int(end.timestamp())
            )
        )
    elif periode == "month":
        now = datetime.now()
        start = datetime(
            now.year,
            now.month,
            1
        )
        if now.month == 12 :
            end = datetime(
                now.year + 1,
                1,
                1
            )
        else:
            end = datetime(
                now.year,
                now.month + 1,
                1
            )
        sales = sales.filter(
            Sales.tanggal.between(
                int(start.timestamp()),
                int(end.timestamp())
            )
        )
    elif periode == "year":
        now = datetime.now()
        start = datetime(
            now.year,
            1,
            1
        )

        end = datetime(
            now.year + 1,
            1,
            1
        )

        sales = sales.filter(
            Sales.tanggal.between(
                int(start.timestamp()),
                int(end.timestamp())
            )
        )
    elif (periode == "custom"
        and start_date
        and end_date
    ):

        start = int(
            datetime.strptime(
                start_date,
                "%Y-%m-%d"
            ).timestamp()
        )

        end = int(
            datetime.strptime(
                end_date,
                "%Y-%m-%d"
            ).timestamp()
        )+86400
    # karena 1 hari = 86400 detik, digunakan supaya tanggal tansaksi terakhir juga terbaca

        sales = sales.filter(
            Sales.tanggal.between(
                start,
                end
            )
        )

    return sales

# Profit Function
def calculate_profit(sale_ids):

    omset = 0

    laba_barang = 0

    laba_jasa = 0

    # ==========================
    # BARANG
    # ==========================

    sale_details = SaleDetails.query.filter(
        SaleDetails.sale_id.in_(
            sale_ids
        )
    ).all()
        
    for detail in sale_details:

        item = Items.query.get(
            detail.item_id
        )

        omset += detail.subtotal
        # Hitung Laba (harga jual - harga beli)*banyak barang
        laba_barang += ((detail.harga_jual -item.harga_beli)* detail.qty)

    # ==========================
    # JASA
    # ==========================

    service_details = SaleServiceDetails.query.filter(
        SaleServiceDetails.sale_id.in_(
            sale_ids
        )
    ).all()

    for service in service_details:

       omset += service.subtotal

       laba_jasa += service.subtotal

    laba_kotor = (laba_barang + laba_jasa)

    laba_bersih = (laba_kotor)

    return {
        

        "omset": omset,

        "laba_barang": laba_barang,

        "laba_jasa": laba_jasa,

        "laba_kotor": laba_kotor,

        "laba_bersih": laba_bersih
    
    }


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

        
        purchase.total_format = (
            f"Rp {purchase.total:,}"
        ).replace(",", ".")

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

    periode = request.args.get(
        'periode',
        'today'
    )

    start_date = request.args.get(
        'start_date'
    )

    end_date = request.args.get(
        'end_date'
    )
    query = Sales.query.filter_by(
        is_delete=0
    )

    query = filter_sales_by_periode(
        query,
        periode,
        start_date,
        end_date
    )

    sales = query.all()
    for sale in sales:

        sale.customer = Customers.query.get(
            sale.customer_id
        )

        sale.tanggal_format = datetime.fromtimestamp(
            sale.tanggal
        ).strftime("%d-%m-%Y")

        sale.total_format = (
            f"Rp {sale.total:,}"
        ).replace(",", ".")

    total_penjualan = sum(
        sale.total
        for sale in sales
    )

    return render_template(
        template_name_or_list='report_sales.html',
        title='Laporan Penjualan',
        sales=sales,
        total_penjualan=total_penjualan,
        periode=periode,
        start_date=start_date,
        end_date=end_date,
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

        item.harga_beli_format = (
            f"Rp {item.harga_beli:,}"
        ).replace(",", ".")

        item.harga_jual_format = (
            f"Rp {item.harga_jual:,}"
        ).replace(",", ".")

    return render_template(
        template_name_or_list='report_stock.html',
        title='Laporan Stok Barang',
        items=items,
        active_menu="stock_report"
    )

@report.get('/profit')
def profit_page():

    if 'user_id' not in session:
        return redirect(
            url_for('auth.signin_page')
        )

    return render_template(
        'report_profit.html',
        title='Laporan Keuntungan',
        active_menu='profit_report'
    )

@report.get('/profit/data')
def profit_data():

    try:

        periode = request.args.get(
            'periode',
            'today'
        )

        start_date = request.args.get(
            'start_date'
        )

        end_date = request.args.get(
            'end_date'
        )

        sales = Sales.query.filter_by(
            is_delete=0
        )

        sales = filter_sales_by_periode(
            sales,
            periode,
            start_date,
            end_date
        )
        
        sales = sales.all()
        for sale in sales:
            print(
            datetime.fromtimestamp(
                sale.tanggal
            )
        )
        sale_ids = [
            sale.id
            for sale in sales
        ]

        result = calculate_profit(
            sale_ids
        )

        return {
            "status": True,
            "data": result
        }
    
    except Exception as e:

        return {
            "status": False,
            "message": str(e)
        }, 500

@report.get('/profit/chart')
def profit_chart():

    data = []

    tahun = datetime.now().year

    for bulan in range(1, 13):

        start = datetime(
            tahun,
            bulan,
            1
        )

        if bulan == 12:

            end = datetime(
                tahun + 1,
                1,
                1
            )

        else:

            end = datetime(
                tahun,
                bulan + 1,
                1
            )

        sales = Sales.query.filter(
            Sales.is_delete == 0,
            Sales.tanggal.between(
                int(start.timestamp()),
                int(end.timestamp())
            )
        ).all()

        sale_ids = [
            sale.id
            for sale in sales
        ]

        result = calculate_profit(
            sale_ids
        )

        data.append({
            
            "bulan": start.strftime(
                "%b"
            ),

            "laba_barang": result[
                "laba_barang"
            ],

            "laba_jasa": result[
                "laba_jasa"
            ],
            "laba": result[
                "laba_kotor"
            ]

        })

    return {
        "status": True,
        "data": data
    }

@report.get('/profit/pdf')
def export_profit_pdf():
    periode = request.args.get(
        'periode',
        'today'
    )

    start_date = request.args.get(
        'start_date'
    )

    end_date = request.args.get(
        'end_date'
    )
    sales = Sales.query.filter_by(
        is_delete=0
    )

    sales = filter_sales_by_periode(
        sales,
        periode,
        start_date,
        end_date
    )

    sales = sales.all()

    sale_ids = [
        sale.id
        for sale in sales
    ]

    result = calculate_profit(
        sale_ids
    )

    response = make_response()

    response.headers[
        'Content-Type'
    ] = 'application/pdf'

    response.headers[
        'Content-Disposition'
    ] = (
        'attachment; '
        'filename=laporan_keuntungan.pdf'
    )

    pdf = SimpleDocTemplate(
        response.stream
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(

        Paragraph(
            "Laporan Keuntungan Bengkel",
            styles['Title']
        )

    )
    elements.append(
        Paragraph(
            f"Tanggal Cetak : {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles['Normal']
        )
    )
    elements.append(
        Spacer(1, 20)
    )

    data = [

        ["Keterangan", "Nilai"],

        [
            "Omset",
            f"Rp {result['omset']:,}"
        ],

        [
            "Laba Barang",
            f"Rp {result['laba_barang']:,}"
        ],

        [
            "Laba Jasa",
            f"Rp {result['laba_jasa']:,}"
        ],

        [
            "Laba Bersih",
            f"Rp {result['laba_bersih']:,}"
        ]

    ]
    if periode == "custom":
    
        elements.append(

            Paragraph(
                f"Periode : {start_date} s/d {end_date}",
                styles['Normal']
            )

        )
    table = Table(data)

    table.setStyle(

        TableStyle([

            (
                'BACKGROUND',
                (0,0),
                (-1,0),
                colors.grey
            ),

            (
                'GRID',
                (0,0),
                (-1,-1),
                1,
                colors.black
            )

        ])

    )

    elements.append(
        table
    )

    pdf.build(
        elements
    )
    print("PERIODE =", periode)
    print("START =", start_date)
    print("END =", end_date)
    print("SALE IDS =", sale_ids)
    print(result)
    return response