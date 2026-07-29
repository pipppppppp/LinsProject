from datetime import datetime

from sqlalchemy import func
from apps.database.db_workshops import Workshops

from apps.database.db_products import Products
from apps.database.db_purchases import Purchases
from apps.database.db_suppliers import Suppliers
from apps.database.db_purchase_details import PurchaseDetails

from apps.utilities.responseHelpers import *
from apps.utilities.validators import role_validator
from apps.utilities.formatter import format_date

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from flask import send_file
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
      SimpleDocTemplate,
      Table,
      TableStyle,
      Paragraph,
      Spacer
)

# REPORT SALES HELPER ============================================================ Begin
def _report_purchase_helper(workshop_id, supplier_id="", start_date="", end_date="" ):

      purchases = Purchases.query.filter(
            Purchases.workshop_id == workshop_id,
            Purchases.is_delete == 0
      )

      # Filter Supplier
      if supplier_id != "":
            purchases = purchases.filter(
                  Purchases.supplier_id == supplier_id
            )

      # Filter Tanggal
      if start_date and end_date:
            purchases = purchases.filter(
                  Purchases.purchase_date >= start_date,
                  Purchases.purchase_date <= end_date
            )

      return purchases
# REPORT SALES HELPER ============================================================ End

# FILTER DATE HELPER ============================================================ Begin
def _get_filter_date(start_date="", end_date=""):

      today = datetime.now()

      # Default hari ini
      if not start_date or not end_date:

            start_datetime = datetime(
                  today.year,
                  today.month,
                  today.day,
                  0,
                  0,
                  0
            )

            end_datetime = datetime(
                  today.year,
                  today.month,
                  today.day,
                  23,
                  59,
                  59
            )

      # Berdasarkan filter user
      else:

            start_datetime = datetime.strptime(
                  start_date,
                  "%Y-%m-%d"
            )

            end_datetime = datetime.strptime(
                  end_date,
                  "%Y-%m-%d"
            ).replace(
                  hour=23,
                  minute=59,
                  second=59
            )

      return (
            int(start_datetime.timestamp()),
            int(end_datetime.timestamp())
      )
# FILTER DATE HELPER ============================================================ End

# REPORT SALES ============================================================ Begin
class ReportPurchaseModels():
      # REPORT SUMMARY ============================================================ Begin
      def report_summary(user_role,user_id,workshop_id,supplier_id="",start_date=None,end_date=None):
            try:

                  # Access Validation ---------------------------------------- Start
                  access = role_validator(user_role)

                  if not access:
                        return authorization_error()
                  # Access Validation ---------------------------------------- Finish

                  # Check Workshop ---------------------------------------- Start
                  workshop = Workshops.query.filter_by(
                        id=workshop_id,
                        is_delete=0
                  ).first()

                  if not workshop:
                        return not_found(
                              "Workshop could not be found."
                        )
                  # Check Workshop ---------------------------------------- Finish

                  # Filter Date ---------------------------------------- Start
                  start_date, end_date = _get_filter_date(
                        start_date,
                        end_date
                  )
                  # Filter Date ---------------------------------------- Finish

                  # Get Data ---------------------------------------- Start
                  purchases = _report_purchase_helper(
                        workshop_id,
                        supplier_id=supplier_id,
                        start_date=start_date,
                        end_date=end_date
                  ).all()
                  # Get Data ---------------------------------------- Finish

                  # Summary ---------------------------------------- Start
                  total_transaction = len(purchases)

                  total_purchase = sum(
                        purchase.total for purchase in purchases
                  )

                  average_purchase = (
                        total_purchase / total_transaction
                        if total_transaction > 0
                        else 0
                  )

                  active_supplier = len(
                        set(
                        purchase.supplier_id
                        for purchase in purchases
                        if purchase.supplier_id
                        )
                  )
                  # Summary ---------------------------------------- Finish

                  # Response ---------------------------------------- Start
                  return success_data(
                        data={
                        "total_transaction": total_transaction,
                        "total_purchase": total_purchase,
                        "average_purchase": average_purchase,
                        "active_supplier": active_supplier
                        },
                        status_code=200
                  )
                  # Response ---------------------------------------- Finish

            except Exception as e:
                  print("REPORT PURCHASE SUMMARY ERROR :", e)
                  raise
                  # return bad_request(str(e))
      # REPORT SUMMARY ============================================================ End

      # PURCHASE CHART ============================================================ Begin
      def purchase_chart(user_role, user_id, workshop_id, supplier_id="", start_date=None, end_date=None):
            try:

                  # Access Validation ---------------------------------------- Start
                  access = role_validator(user_role)

                  if not access:
                        return authorization_error()
                  # Access Validation ---------------------------------------- Finish

                  # Check Workshop ---------------------------------------- Start
                  workshop = Workshops.query.filter_by(
                        id=workshop_id,
                        is_delete=0
                  ).first()

                  if not workshop:
                        return not_found(
                              "Workshop could not be found."
                        )
                  # Check Workshop ---------------------------------------- Finish

                  # Filter Date ---------------------------------------- Start
                  start_date, end_date = _get_filter_date(
                        start_date,
                        end_date
                  )
                  # Filter Date ---------------------------------------- Finish

                  # Initialize Query ---------------------------------------- Start
                  query = _report_purchase_helper(
                        workshop_id,
                        supplier_id=supplier_id,
                        start_date=start_date,
                        end_date=end_date
                  )
                  # Initialize Query ---------------------------------------- Finish

                  # Chart Query ---------------------------------------- Start
                  purchases = query.with_entities(
                        Purchases.purchase_date,
                        func.sum(Purchases.total).label("total_purchase")
                  ).group_by(
                        Purchases.purchase_date
                  ).order_by(
                        Purchases.purchase_date.asc()
                  ).all()

                  chart = []

                  for purchase in purchases:

                        chart.append({
                              "date": format_date(
                                    purchase.purchase_date
                              ),
                              "total_purchase": purchase.total_purchase
                        })
                  # Chart Query ---------------------------------------- Finish
                  
                  # Response ---------------------------------------- Start
                  return success_data(
                        data={
                              "chart": chart
                        },
                        status_code=200
                  )
                  # Response ---------------------------------------- Finish         
            except Exception as e:
                  return bad_request(str(e))
      # PURCHASE CHART ============================================================ End

      # TOP SUPPLIERS ============================================================ Begin
      def top_suppliers(user_role,user_id,workshop_id,supplier_id="",start_date=None,end_date=None):
            try:

                  # Access Validation ---------------------------------------- Start
                  access = role_validator(user_role)

                  if not access:
                        return authorization_error()
                  # Access Validation ---------------------------------------- Finish

                  # Check Workshop ---------------------------------------- Start
                  workshop = Workshops.query.filter_by(
                        id=workshop_id,
                        is_delete=0
                  ).first()

                  if not workshop:
                        return not_found(
                              "Workshop could not be found."
                        )
                  # Check Workshop ---------------------------------------- Finish

                  # Filter Date ---------------------------------------- Start
                  start_date, end_date = _get_filter_date(
                        start_date,
                        end_date
                  )
                  # Filter Date ---------------------------------------- Finish

                  # Get Data ---------------------------------------- Start
                  query = _report_purchase_helper(
                        workshop_id,
                        supplier_id=supplier_id,
                        start_date=start_date,
                        end_date=end_date
                  )
                  # Get Data ---------------------------------------- Finish

                  # Top Suppliers ---------------------------------------- Start
                  suppliers = query.with_entities(
                        Suppliers.supplier_name,
                        func.sum(Purchases.total).label("total_purchase")
                  ).join(
                        Suppliers,
                        Purchases.supplier_id == Suppliers.id
                  ).group_by(
                        Suppliers.id,
                        Suppliers.supplier_name
                  ).order_by(
                        func.sum(Purchases.total).desc()
                  ).limit(5).all()

                  data = []

                  for supplier in suppliers:

                        data.append({
                              "supplier_name": supplier.supplier_name,
                              "total_purchase": supplier.total_purchase
                        })
                  # Top Suppliers ---------------------------------------- Finish
                  
                  # Response ---------------------------------------- Start
                  return success_data(
                        data={
                              "top_suppliers": data
                        },
                        status_code=200
                  )
                  # Response ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # TOP SUPPLIERS ============================================================ End

      # TOP SERVICES ============================================================ Begin
      def top_product(user_role,user_id,workshop_id,supplier_id="",start_date=None,end_date=None):
            try:

                 # Access Validation ---------------------------------------- Start
                  access = role_validator(user_role)

                  if not access:
                        return authorization_error()
                  # Access Validation ---------------------------------------- Finish

                  # Check Workshop ---------------------------------------- Start
                  workshop = Workshops.query.filter_by(
                        id=workshop_id,
                        is_delete=0
                  ).first()

                  if not workshop:
                        return not_found(
                              "Workshop could not be found."
                        )
                  # Check Workshop ---------------------------------------- Finish

                  # Filter Date ---------------------------------------- Start
                  start_date, end_date = _get_filter_date(
                        start_date,
                        end_date
                  )
                  # Filter Date ---------------------------------------- Finish

                  # Get Data ---------------------------------------- Start
                  query = _report_purchase_helper(
                        workshop_id,
                        supplier_id=supplier_id,
                        start_date=start_date,
                        end_date=end_date
                  )
                  # Get Data ---------------------------------------- Finish

                  # Top Products ---------------------------------------- Start
                  products = query.join(
                        PurchaseDetails,
                        Purchases.id == PurchaseDetails.purchase_id
                  ).join(
                        Products,
                        PurchaseDetails.product_id == Products.id
                  ).with_entities(
                        Products.product_name,
                        func.sum(
                              PurchaseDetails.quantity
                        ).label("total_quantity")
                  ).group_by(
                        Products.id,
                        Products.product_name
                  ).order_by(
                        func.sum(
                              PurchaseDetails.quantity
                        ).desc()
                  ).limit(5).all()

                  data = []

                  for product in products:

                        data.append({
                              "product_name": product.product_name,
                              "total_quantity": product.total_quantity
                        })
                  # Top Products ---------------------------------------- Finish

                  # Response ---------------------------------------- Start
                  return success_data(
                        data={
                              "top_suppliers": data
                        },
                        status_code=200
                  )
                  # Response ---------------------------------------- Finish
            except Exception as e:
                  return bad_request(str(e))
      # TOP PRODUCTS ============================================================ End

      # REPORT TABLE ============================================================ Begin
      def report_table(user_role,user_id,workshop_id,supplier_id="",start_date=None,end_date=None):
            try:

                 # Access Validation ---------------------------------------- Start
                  access = role_validator(user_role)

                  if not access:
                        return authorization_error()
                  # Access Validation ---------------------------------------- Finish

                  # Check Workshop ---------------------------------------- Start
                  workshop = Workshops.query.filter_by(
                        id=workshop_id,
                        is_delete=0
                  ).first()

                  if not workshop:
                        return not_found(
                              "Workshop could not be found."
                        )
                  # Check Workshop ---------------------------------------- Finish

                  # Filter Date ---------------------------------------- Start
                  start_date, end_date = _get_filter_date(
                        start_date,
                        end_date
                  )
                  # Filter Date ---------------------------------------- Finish

                  # Get Data ---------------------------------------- Start
                  purchases = _report_purchase_helper(
                        workshop_id,
                        supplier_id=supplier_id,
                        start_date=start_date,
                        end_date=end_date
                  ).order_by(
                        Purchases.purchase_date.desc()
                  ).all()   
                  # Get Data ---------------------------------------- Finish

                  # Report ---------------------------------------- Start
                  report = []

                  for purchase in purchases:

                        report.append({
                              "id": purchase.id,
                              "invoice": purchase.invoice,
                              "purchase_date": format_date(
                                    purchase.purchase_date
                              ),
                              "supplier_name": (
                                    purchase.suppliers.supplier_name
                                    if purchase.suppliers
                                    else "-"
                              ),
                              "total": purchase.total
                        })
                  # Report ---------------------------------------- Finish
                  
                  # Response ---------------------------------------- Finish
                  return success_data(
                        data={
                              "report": report
                        },
                        status_code=200
                  )
            except Exception as e:
                  return bad_request(str(e))
      # REPOT TABLE ============================================================ End

      # EXPORT EXCEL ============================================================ Begin
      def export_excel(user_role, user_id, workshop_id, supplier_id="", start_date=None, end_date=None):
            try:

                  # Access Validation ---------------------------------------- Start
                  access = role_validator(user_role)

                  if not access:
                        return authorization_error()

                  # Hanya owner
                  if str(user_role) != "1":
                        return authorization_error()
                  # Access Validation ---------------------------------------- Finish

                  # Check Workshop ---------------------------------------- Start
                  workshop = Workshops.query.filter_by(
                        id=workshop_id,
                        is_delete=0
                  ).first()

                  if not workshop:
                        return not_found("Workshop could not be found.")
                  # Check Workshop ---------------------------------------- Finish

                  # Filter Date ---------------------------------------- Start
                  start_date, end_date = _get_filter_date(
                        start_date,
                        end_date
                  )
                  # Filter Date ---------------------------------------- Finish

                  # Get History ---------------------------------------- Start
                  query = _report_sales_helper(
                        workshop_id,
                        supplier_id=user_id if str(user_role) == "2" else supplier_id,
                        start_date=start_date,
                        end_date=end_date
                  )

                  purchases = query.order_by(
                        Payments.purchase_date.desc()
                  ).all()
                  # Get History ---------------------------------------- Finish

                  # Summary ---------------------------------------- Start
                  total_transaction = len(purchases)

                  total_sales = sum(
                        payment.total for payment in purchases
                  )
                  # Summary ---------------------------------------- Finish

                  # Create Workbook ---------------------------------------- Start
                  workbook = Workbook()
                  worksheet = workbook.active
                  worksheet.title = "Report Sales"
                  worksheet.merge_cells("A1:I1")

                  worksheet["A1"] = "LAPORAN PENJUALAN"

                  worksheet["A1"].font = Font(
                        bold=True,
                        size=16
                  )

                  worksheet["A1"].alignment = Alignment(
                        horizontal="center"
                  )

                  worksheet.append([])

                  worksheet.append([
                        "Nama Bengkel",
                        workshop.workshop_name
                  ])

                  worksheet.append([
                        "Periode",
                        f"{format_date(start_date)} s.d. {format_date(end_date)}"
                  ])

                  worksheet.append([])

                  worksheet.append([
                        "No",
                        "Invoice",
                        "Tanggal",
                        "Customer",
                        "Plat Nomor",
                        "Kasir",
                        "Total",
                        "Bayar",
                        "Kembalian"
                  ])
                  # Create Workbook ---------------------------------------- Finish

                  # Fill Data ---------------------------------------- Start
                  for index, payment in enumerate(purchases, start=1):
                       worksheet.append([
                              index,
                              payment.invoice,
                              format_date(payment.purchase_date),
                              payment.customers.customer_name if payment.customers else "Pelanggan Umum",
                              payment.vehicles.plate_number if payment.vehicles else "-",
                              payment.cashier.username if payment.cashier else "-",
                              f"Rp {payment.total:,}".replace(",", "."),
                              f"Rp {payment.paid:,}".replace(",", "."),
                              f"Rp {payment.change:,}".replace(",", ".")
                        ])
                  # Fill Data ---------------------------------------- Finish
                  worksheet.append([])

                  worksheet.append([
                        "Jumlah Transaksi",
                        total_transaction
                  ])

                  worksheet.append([
                        "Total Penjualan",
                        f"Rp {total_sales:,}".replace(",", ".")
                  ])

                  # Response File ---------------------------------------- Start
                  buffer = BytesIO()
                  workbook.save(buffer)

                  buffer.seek(0)

                  return send_file(
                        buffer,
                        as_attachment=True,
                        download_name="sales_report.xlsx",
                        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                  )                        
                  # Response File ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # EXPORT EXCEL ============================================================ End

      # EXPORT PDF ============================================================ Begin
      def export_pdf(user_role, user_id, workshop_id, supplier_id="", start_date=None, end_date=None):
            try:

                  # Access Validation ---------------------------------------- Start
                  access = role_validator(user_role)
                  if not access:
                        return authorization_error()
                  # Hanya owner yang boleh export pdf
                  if str(user_role) != "1":
                        return authorization_error()
                  # Access Validation ---------------------------------------- Finish

                  # Check Workshop ---------------------------------------- Start
                  workshop = Workshops.query.filter_by(
                        id=workshop_id,
                        is_delete=0
                  ).first()

                  if not workshop:
                        return not_found(
                        "Workshop could not be found."
                        )
                  # Check Workshop ---------------------------------------- Finish

                  # Filter Date ---------------------------------------- Start
                  start_date, end_date = _get_filter_date(
                        start_date,
                        end_date
                  )
                  # Filter Date ---------------------------------------- Finish

                  # Get Report Data ---------------------------------------- Start
                  query = _report_sales_helper(
                        workshop_id,
                        supplier_id=user_id if str(user_role) == "2" else supplier_id,
                        start_date=start_date,
                        end_date=end_date
                  )

                  purchases = query.order_by(
                        Payments.purchase_date.desc()
                  ).all()
                  # Get Report Data ---------------------------------------- Finish
                  # Summary ---------------------------------------- Start
                  total_transaction = len(purchases)

                  total_sales = sum(
                        purchases.total for purchases in purchases
                  )
                  # Summary ---------------------------------------- Finish
                  # Generate PDF ---------------------------------------- Start
                  
                  table_data = [
                        [
                              "No",
                              "Invoice",
                              "Tanggal",
                              "Customer",
                              "Plat Nomor",
                              "Kasir",
                              "Total"

                        ]
                  ]

                  for index, purchases in enumerate(purchases, start=1):
      
                        table_data.append([
                              index,
                              purchases.invoice,
                              format_date(purchases.purchase_date),
                              purchases.customers.customer_name if purchases.customers else "Pelanggan Umum",
                              purchases.vehicles.plate_number if purchases.vehicles else "-",
                              purchases.cashier.username if purchases.cashier else "-",
                              f"Rp {purchases.total:,}".replace(",", ".")
                        ])
                  
                  # Initialize PDF ---------------------------------------- Start
                  buffer = BytesIO()

                  document = SimpleDocTemplate(
                        buffer,
                        pagesize=A4,
                        leftMargin=1.5 * cm,
                        rightMargin=1.5 * cm,
                        topMargin=2 * cm,
                        bottomMargin=2 * cm
                  )

                  styles = getSampleStyleSheet()

                  elements = []
                  # judul
                  elements.append(
                        Paragraph(
                        "<b>LAPORAN PENJUALAN</b>",
                        styles["Title"]
                        )
                  )
                  elements.append(
                        Paragraph(
                        f"<b>Nama Bengkel :</b> {workshop.workshop_name}",
                        styles["Normal"]
                        )
                  )

                  elements.append(
                        Paragraph(
                        f"<b>Periode Laporan:</b> "
                        f"{format_date(start_date)} "
                        f"s.d "
                        f"{format_date(end_date)}",
                        styles["Normal"]
                        )
                  )

                  elements.append(Spacer(1, 0.4 * cm))

                  # data table
                  table = Table(
                        table_data,
                        colWidths=[
                              1 * cm,      # No
                              4 * cm,      # Invoice
                              2.8 * cm,    # Tanggal
                              4 * cm,      # Customer
                              3 * cm,      # Plat Nomor
                              3 * cm,      # Kasir
                              3 * cm       # Total
                        ],
                        repeatRows=1
                  )

                  table.setStyle(
                  TableStyle([
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0d6efd")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 10),

                        ("ALIGN", (0, 0), (0, -1), "CENTER"),   # No
                        ("ALIGN", (1, 0), (4, -1), "LEFT"),     # Invoice- cashier
                        ("ALIGN", (5, 0), (5, -1), "RIGHT"),    # Total

                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                        ("TOPPADDING", (0, 1), (-1, -1), 6),
                        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
                        ])
                  )

                  elements.append(table)

                  elements.append(Spacer(1,0.5*cm))

                  elements.append(
                        Paragraph(
                              f"<b>Jumlah Transaksi :</b> {total_transaction}",
                              styles["Normal"]
                        )
                  )

                  elements.append(
                        Paragraph(
                              f"<b>Total Penjualan :</b> Rp {total_sales:,}".replace(",", "."),
                              styles["Normal"]
                        )
                  )

                  document.build(elements)

                  buffer.seek(0)
                  # Initialize PDF ---------------------------------------- Finish

                  # Generate PDF ---------------------------------------- Finish

                  # Return File ---------------------------------------- Start
                  return send_file(
                        buffer,
                        as_attachment=True,
                        download_name="sales_report.pdf",
                        mimetype="application/pdf"
                  )
                  # Return File ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # EXPORT PDF ============================================================ End

# REPORT SALES ============================================================ End