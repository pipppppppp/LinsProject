from datetime import datetime

from apps.database.db_payment import Payments
from apps.database.db_workshops import Workshops
from apps.database.db_purchases import Purchases
from apps.database.db_suppliers import Suppliers
from apps.database.db_purchase_details import PurchaseDetails

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

# HISTORY PURCHASE HELPER ============================================================ Begin
def _history_purchase_helper(workshop_id, supplier_id="", start_date="", end_date=""):

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
      if start_date != "" and end_date != "":
            purchases = purchases.filter(
                  Purchases.purchase_date >= start_date,
                  Purchases.purchase_date <= end_date
            )

      purchases = purchases.order_by(
            Purchases.purchase_date.desc()
      ).all()

      data = []

      for purchase in purchases:

            purchase_date = format_date(
                  purchase.purchase_date
            )

            data.append({
                  "id": purchase.id,
                  "purchase_date": purchase_date,
                  "supplier_name": (
                        purchase.suppliers.name
                        if purchase.suppliers
                        else "-"
                  ),
                  "total": purchase.total
            })

      return data
# HISTORY PURCHASE HELPER ============================================================ End

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
            int(start_datetime.timestamp() * 1000),
            int(end_datetime.timestamp() * 1000)
      )
# FILTER DATE HELPER ============================================================ End

# HISTORY SALES ============================================================ Begin
class HistoryPurchaseModels:
    # HISTORY PURCHASE ============================================================ Begin
    def read_history_purchase(user_role, workshop_id, supplier_id="", start_date=None, end_date=None):
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
            
            print("START :", start_date)
            print("END   :", end_date)
            # Filter Date ---------------------------------------- Finish

            # Get History ---------------------------------------- Start
            result = _history_purchase_helper(
                  workshop_id,
                  supplier_id=supplier_id,
                  start_date=start_date,
                  end_date=end_date
            )
            # Get History ---------------------------------------- Finish
            print("WORKSHOP :", workshop_id)
            print("TOTAL PURCHASE :", Purchases.query.count())
            # Summary ---------------------------------------- Start
            query = Purchases.query.filter(
                  Purchases.workshop_id == workshop_id,
                  Purchases.is_delete == 0,
                  Purchases.purchase_date >= start_date,
                  Purchases.purchase_date <= end_date
            )

            if supplier_id != "":
                  query = query.filter(
                        Purchases.supplier_id == int(supplier_id)
                  )

            filter_purchase = query.all()

            all_purchase = Purchases.query.filter_by(
                  workshop_id=workshop_id,
                  is_delete=0
            ).all()

            for p in all_purchase:
                  print(
                              "ID:", p.id,
                              "DATE:", p.purchase_date,
                              "TYPE:", type(p.purchase_date)
                        )
            print("FILTER PURCHASE :", len(filter_purchase))

            for purchase in filter_purchase:
                  print(
                        purchase.id,
                        purchase.purchase_date,
                        purchase.workshop_id,
                        purchase.supplier_id
                  )

            total_purchase = len(filter_purchase)

            total_expense = sum(
                  purchase.total
                  for purchase in filter_purchase
            )
            # Summary ---------------------------------------- Finish

            # Pembelian Hari Ini ---------------------------------------- Start
            today = datetime.now()

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

            today_query = Purchases.query.filter(
                  Purchases.workshop_id == workshop_id,
                  Purchases.is_delete == 0,
                  Purchases.purchase_date >= int(today_start.timestamp()),
                  Purchases.purchase_date <= int(today_end.timestamp())
            )

            if supplier_id != "":
                  today_query = today_query.filter(
                        Purchases.supplier_id == int(supplier_id)
                  )

            today_purchase = sum(
                  purchase.total
                  for purchase in today_query.all()
            )
            # Pembelian Hari Ini ---------------------------------------- Finish

            # Supplier Aktif ---------------------------------------- Start
            active_supplier = len(
                  set(
                        purchase.supplier_id
                        for purchase in filter_purchase
                  )
            )
            # Supplier Aktif ---------------------------------------- Finish

            # Response ---------------------------------------- Start
            return success_data(
                  data={
                        "history": result,
                        "total_purchase": total_purchase,
                        "total_expense": total_expense,
                        "today_purchase": today_purchase,
                        "active_supplier": active_supplier
                  },
                  status_code=200
            )
            # Response ---------------------------------------- Finish

        except Exception as e:
            return bad_request(str(e))
    # HISTORY PURCHASE ============================================================ End
      
    # DETAIL HISTORY PURCHASE ============================================================ Begin
    def detail_history_purchase(user_role, workshop_id, purchase_id):
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

            # Check Purchase ---------------------------------------- Start
            purchase = Purchases.query.filter(
                  Purchases.id == purchase_id,
                  Purchases.workshop_id == workshop_id,
                  Purchases.is_delete == 0
            ).first()

            if not purchase:
                  return not_found(
                        "Purchase could not be found."
                  )
            # Check Purchase ---------------------------------------- Finish

            # Purchase Detail ---------------------------------------- Start
            products = []

            for item in purchase.purchase_details:

                  products.append({
                        "id": item.id,
                        "product_id": item.product_id,
                        "product_name": item.products.product_name,
                        "quantity": item.quantity,
                        "unit_cost": item.unit_cost,
                        "subtotal": item.subtotal
                  })
            # Purchase Detail ---------------------------------------- Finish

            # Initialize Data ---------------------------------------- Start
            result = {
                  "id": purchase.id,
                  "purchase_date": format_date(
                        purchase.purchase_date
                  ),
                  "supplier_id": purchase.supplier_id,
                  "supplier_name": (
                        purchase.suppliers.name
                        if purchase.suppliers
                        else "-"
                  ),
                  "total": purchase.total,
                  "products": products
            }
            # Initialize Data ---------------------------------------- Finish

            return success_data(
                  data=result,
                  status_code=200
            )

        except Exception as e:
                return bad_request(str(e))
    # DETAIL HISTORY PURCHASE ============================================================ End

# HISTORY SALES ============================================================ End