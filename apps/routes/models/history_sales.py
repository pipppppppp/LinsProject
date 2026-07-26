from datetime import datetime

from apps.database.db_payment import Payments
from apps.database.db_workshops import Workshops

from apps.utilities.responseHelpers import *
from apps.utilities.validators import role_validator
from apps.utilities.formatter import format_date


# Excle
from io import BytesIO
from flask import send_file
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

# pdf
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

# HISTORY SALES HELPER ============================================================ Begin
def _history_sales_helper(workshop_id, cashier_id="", start_date="", end_date="" ):

      payments = Payments.query.filter(
            Payments.workshop_id == workshop_id,
            Payments.is_delete == 0
      )

      # Cashier hanya melihat transaksi miliknya
      if cashier_id != "":
            payments = payments.filter(
            Payments.cashier_id == cashier_id
      )

      # filter tanggal
      if start_date != "" and end_date != "":
            payments=payments.filter(
                  Payments.payment_date >=start_date,
                  Payments.payment_date <= end_date
            )

      payments = payments.order_by(
            Payments.payment_date.desc()
      ).all()

      data = []

      for payment in payments:

            payment_date = format_date(payment.payment_date)

            data.append({
                  "id": payment.id,
                  "invoice": payment.invoice,
                  "payment_date": payment_date,
                  "customer_name": (payment.customers.customer_name if payment.customers else "Pelanggan Umum"),
                  "plate_number": (payment.vehicles.plate_number if payment.vehicles else "-"),
                  "cashier_name": (payment.cashier.username if payment.cashier else "-"),
                  "total": payment.total,
                  "paid": payment.paid,
                  "change": payment.change
            })

      return data
# HISTORY SALES HELPER ============================================================ End

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

# HISTORY SALES ============================================================ Begin
class HistorySalesModels():
      # HISTORY SALES ============================================================ Begin
      def read_history_sales(user_role, user_id, workshop_id, start_date=None, end_date=None):
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
                  today = datetime.now()

                  # Default filter = hari ini
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

                  # Filter berdasarkan tanggal yang dipilih
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

                  # Konversi ke timestamp
                  start_date = int(start_datetime.timestamp())
                  end_date = int(end_datetime.timestamp())
                  # Filter Date ---------------------------------------- Finish

                  # Get History ---------------------------------------- Start
                  if str(user_role) == "2":
            
                        result = _history_sales_helper(workshop_id, cashier_id=user_id, start_date=start_date, end_date=end_date)

                  else:
                        result = _history_sales_helper(workshop_id, start_date=start_date, end_date=end_date)
                  # Get History ---------------------------------------- Finish

                  # Filter Summary ---------------------------------------- Start
                  query = Payments.query.filter(
                        Payments.workshop_id == workshop_id,
                        Payments.is_delete == 0,
                        Payments.payment_date >= start_date,
                        Payments.payment_date <= end_date
                  )

                  if str(user_role) == "2":
                        query = query.filter(
                              Payments.cashier_id == user_id
                        )

                  filter_payments = query.all()

                  today_transaction = len(filter_payments)

                  today_total = sum(
                        payment.total for payment in filter_payments
                  )
                  # Filter Summary ---------------------------------------- Finish
                  # Penjualan Hari Ini ---------------------------------------- Start
                  today_start = datetime(
                        today.year,
                        today.month,
                        today.day,
                        0,
                        0,
                        0
                  )

                  today_end = datetime(
                        today.year,
                        today.month,
                        today.day,
                        23,
                        59,
                        59
                  )

                  today_query = Payments.query.filter(
                        Payments.workshop_id == workshop_id,
                        Payments.is_delete == 0,
                        Payments.payment_date >= int(today_start.timestamp()),
                        Payments.payment_date <= int(today_end.timestamp())
                  )

                  if str(user_role) == "2":
                        today_query = today_query.filter(
                              Payments.cashier_id == user_id
                        )

                  today_sales = sum(
                        payment.total for payment in today_query.all()
                  )
                  # Penjualan Hari Ini ---------------------------------------- End
                  # Response ---------------------------------------- Start
                  return success_data(
                        data={
                              "history": result,
                              "today_transaction": today_transaction,
                              "today_total": today_total,
                              "today_sales": today_sales
                        },
                        status_code=200
                  )
                  # Response ---------------------------------------- Finish
            except Exception as e:
                  return bad_request(str(e))
      # HISTORY SALES ============================================================ End

      # DETAIL HISTORY SALES ============================================================ Begin
      def detail_history_sales(user_role, user_id, workshop_id, payment_id):
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

                  # Check Payment ---------------------------------------- Start
                  payment = Payments.query.filter(
                        Payments.id == payment_id,
                        Payments.workshop_id == workshop_id,
                        Payments.is_delete == 0
                  ).first()

                  if not payment:
                        return not_found(
                        "Transaction could not be found."
                        )
                  # Check Payment ---------------------------------------- Finish

                  # Authorization ---------------------------------------- Start
                  if str(user_role) == "2":
                        if payment.cashier_id != user_id:
                              return authorization_error()
                  # Authorization ---------------------------------------- Finish

                  payment_date = format_date(payment.payment_date)
                  # Product Detail ---------------------------------------- Start
                  products = []

                  for item in payment.sale_details:

                        products.append({
                        "id": item.id,
                        "product_id": item.product_id,
                        "product_name": item.products.product_name,
                        "quantity": item.quantity,
                        "unit_price": item.unit_price,
                        "subtotal": item.subtotal
                        })
                  # Product Detail ---------------------------------------- Finish

                  # Service Detail ---------------------------------------- Start
                  services = []

                  for item in payment.sale_service_details:

                        services.append({
                        "id": item.id,
                        "service_id": item.service_id,
                        "service_name": item.services.name,
                        "quantity": item.quantity,
                        "service_price": item.service_price,
                        "subtotal": item.subtotal
                        })
                  # Service Detail ---------------------------------------- Finish

                  # Initialize Data ---------------------------------------- Start
                  result = {
                        "id": payment.id,
                        "invoice": payment.invoice,
                        "payment_date": payment_date,
                        "customer_name": payment.customers.customer_name if payment.customers else "Pelangan Umum",
                        "customer_phone": payment.customers.customer_phone if payment.customers else "-",
                        "plate_number": payment.vehicles.plate_number if payment.vehicles else "-",
                        "vehicle_brand": payment.vehicles.vehicle_brand if payment.vehicles else "-",
                        "vehicle_type": payment.vehicles.vehicle_type if payment.vehicles else "-",
                        "cashier_name": payment.cashier.username if payment.cashier else "-",
                        "total": payment.total,
                        "paid": payment.paid,
                        "change": payment.change,
                        "products": products,
                        "services": services
                  }
                  # Initialize Data ---------------------------------------- Finish

                  return success_data(
                        data=result,
                        status_code=200
                  )

            except Exception as e:
                  return bad_request(str(e))
      # DETAIL HISTORY SALES ============================================================ End

      # EXPORT EXCEL ============================================================ Begin
      def export_excel(user_role, user_id, workshop_id, start_date=None, end_date=None):
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
                  history = _history_sales_helper(
                        workshop_id,
                        start_date=start_date,
                        end_date=end_date
                  )
                  # Get History ---------------------------------------- Finish

                  # Summary ---------------------------------------- Start
                  total_transaction = len(history)

                  total_sales = sum(
                        item["total"] for item in history
                  )
                  # Summary ---------------------------------------- Finish

                  # Create Workbook ---------------------------------------- Start
                  workbook = Workbook()
                  worksheet = workbook.active
                  worksheet.title = "History Sales"
                  worksheet.merge_cells("A1:H1")

                  worksheet["A1"] = "LAPORAN RIWAYAT PENJUALAN"

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
                  for index, item in enumerate(history, start=1):
                        worksheet.append([
                              index,
                              item["invoice"],
                              item["payment_date"],
                              item["customer_name"],
                              item["plate_number"],
                              item["cashier_name"],
                              f"Rp {item['total']:,}".replace(",", "."),
                              f"Rp {item['paid']:,}".replace(",", "."),
                              f"Rp {item['change']:,}".replace(",", ".")
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
                        download_name="history_sales_report.xlsx",
                        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                  )                        
                  # Response File ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # EXPORT EXCEL ============================================================ End

      # EXPORT PDF ============================================================ Begin
      def export_pdf(user_role, user_id, workshop_id, start_date=None, end_date=None):
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

                  # Get History ---------------------------------------- Start
                  history = _history_sales_helper(
                        workshop_id,
                        start_date=start_date,
                        end_date=end_date
                  )
                  # Get History ---------------------------------------- Finish
                  # Summary ---------------------------------------- Start
                  total_transaction = len(history)

                  total_sales = sum(
                        item["total"] for item in history
                  )
                  # Summary ---------------------------------------- Finish
                  # Generate PDF ---------------------------------------- Start
                  
                  table_data = [
                        [
                              "No",
                              "Invoice",
                              "Date",
                              "Customer",
                              "Cashier",
                              "Total"
                        ]
                  ]

                  for index, item in enumerate(history, start=1):
      
                        table_data.append([
                              index,
                              item["invoice"],
                              item["payment_date"],
                              item["customer_name"],
                              item["cashier_name"],
                              f"Rp {item['total']:,}".replace(",", ".")
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
                        "<b>LAPORAN RIWAYAT PENJUALAN</b>",
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
                              1 * cm,    # No
                              4.5 * cm,  # Invoice
                              2.8 * cm,  # Tanggal
                              5 * cm,    # Customer
                              3.5 * cm,  # Cashier
                              3.2 * cm   # Total
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
                        download_name="history_sales_report.pdf",
                        mimetype="application/pdf"
                  )
                  # Return File ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # EXPORT PDF ============================================================ End
# HISTORY SALES ============================================================ End