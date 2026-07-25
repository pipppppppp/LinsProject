from sqlalchemy import func
from datetime import datetime

from ... import db

from ...database.db_users import Users
from ...database.db_payment import Payments
from ...database.db_products import Products
from ...database.db_services import Services
from ...database.db_sale_details import SaleDetails
from ...database.db_sale_service_details import SaleServiceDetails
from ...database.db_customers import Customers
from ...database.db_cash_deposits import CashDeposits
from ...database.db_workshops import Workshops

from ...utilities.validators import role_validator
from ...utilities.formatter import format_date

from apps.utilities.responseHelpers import *

# DASHBOARD MODEL CLASS ============================================================ Begin
class DashboardCashierModels():

      # DASHBOARD SUMMARY ============================================================ Begin
      def dashboard_summary(user_role, workshop_id, user_id):
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
                  # Today Timestamp ---------------------------------------- Start
                  today = datetime.now().date()

                  start_date = int(datetime.combine(
                        today,
                        datetime.min.time()
                  ).timestamp())

                  end_date = int(datetime.combine(
                        today,
                        datetime.max.time()
                  ).timestamp())
                  # Today Timestamp ---------------------------------------- Finish

                  # Total Sales ---------------------------------------- Start
                  total_sales = db.session.query(
                        func.coalesce(func.sum(Payments.total), 0)
                  ).filter(
                        Payments.workshop_id == workshop_id,
                        Payments.payment_date >= start_date,
                        Payments.payment_date <= end_date,
                        Payments.is_delete == 0
                  ).scalar()
                  # Total Sales ---------------------------------------- Finish

                  # Total Transaction ---------------------------------------- Start
                  total_transaction = Payments.query.filter(
                        Payments.workshop_id == workshop_id,
                        Payments.payment_date >= start_date,
                        Payments.payment_date <= end_date,
                        Payments.is_delete == 0
                  ).count()
                  # Total Transaction ---------------------------------------- Finish

                  # Customer Today ---------------------------------------- Start
                  today_customer = Payments.query.filter(
                        Payments.workshop_id == workshop_id,
                        Payments.payment_date >= start_date,
                        Payments.payment_date <= end_date,
                        Payments.customer_id.isnot(None),
                        Payments.is_delete == 0
                  ).count()
                  # Customer Today ---------------------------------------- Finish

                  # Deposit Status ---------------------------------------- Start
                  deposit = CashDeposits.query.filter(
                        CashDeposits.workshop_id == workshop_id,
                        CashDeposits.user_id == user_id,
                        CashDeposits.is_deleted == 0,
                        CashDeposits.deposit_date >= start_date,
                        CashDeposits.deposit_date <= end_date
                  ).order_by(
                        CashDeposits.deposit_date.desc()
                  ).first()

                  if deposit is None:
                        deposit_status = "Belum Setor"
                  else:
                        if deposit.status == 0:
                              deposit_status = "Menunggu"

                        elif deposit.status == 1:
                              deposit_status = "Disetujui"

                        elif deposit.status == 2:
                              deposit_status = "Ditolak"

                        else:
                              deposit_status = "-"
                  # Deposit Status ---------------------------------------- Finish

                  # Initialize Data ---------------------------------------- Start
                  data = {
                        "total_sales": total_sales,
                        "total_transaction": total_transaction,
                        "today_customer": today_customer,
                        "deposit_status": deposit_status
                  }
                  # Initialize Data ---------------------------------------- Finish

                  # Return Response ---------------------------------------- Start
                  return success_data(data=data, status_code=200)
                  # Return Response ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # DASHBOARD SUMMARY ============================================================ End

      # PAYMENT CHART ============================================================ Begin
      def payments_chart(user_role, workshop_id, user_id, start_date, end_date):
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

                  # Get Data ---------------------------------------- Start
                  payments = db.session.query(
                        Payments.payment_date,
                        func.sum(Payments.total).label("total")
                  ).filter(
                        Payments.workshop_id == workshop_id,
                        Payments.cashier_id == user_id,
                        Payments.is_delete == 0
                  )
                  if start_date is not None:
                        payments = payments.filter(Payments.payment_date >= start_date)

                  if end_date is not None:
                        payments = payments.filter(Payments.payment_date <= end_date)

                  payments = payments.group_by(
                        Payments.payment_date
                  ).order_by(
                        Payments.payment_date
                  ).all()
                  # Get Data ---------------------------------------- Finish

                  # Initialize Data ---------------------------------------- Start
                  data = []

                  for payment in payments:
                        data.append({
                              "date": format_date(payment.payment_date),
                              "total": int(payment.total)
                        })
                  # Initialize Data ---------------------------------------- Finish

                  # Return Response ---------------------------------------- Start
                  return success_data(data=data, status_code=200)
                  # Return Response ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # PAYMENT CHART ============================================================ End

      # TOP PRODUCTS ============================================================ Begin
      def top_products(user_role, workshop_id, user_id, start_date, end_date, limit=5):
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

                  # Get Data ---------------------------------------- Start
                  products = db.session.query(
                        Products.id,
                        Products.product_name,
                        func.sum(SaleDetails.quantity).label("total_sold")
                  ).join(
                        SaleDetails,
                        Products.id == SaleDetails.product_id
                  ).join(
                        Payments,
                        Payments.id == SaleDetails.payment_id
                  ).filter(
                        Payments.workshop_id == workshop_id,
                        Payments.cashier_id == user_id,
                        Payments.is_delete == 0,
                        Products.is_delete == 0
                  )
                  if start_date is not None:
                        products = products.filter(Payments.payment_date >= start_date)

                  if end_date is not None:
                        products = products.filter(Payments.payment_date <= end_date)

                  products = products.group_by(
                        Products.id,
                        Products.product_name
                  ).order_by(
                        func.sum(SaleDetails.quantity).desc()
                  ).limit(limit).all()
                  # Get Data ---------------------------------------- Finish

                  # Initialize Data ---------------------------------------- Start
                  data = []

                  for product in products:
                        data.append({
                              "id": product.id,
                              "product_name": product.product_name,
                              "total_sold": int(product.total_sold)
                        })
                  # Initialize Data ---------------------------------------- Finish

                  # Return Response ---------------------------------------- Start
                  return success_data(data=data, status_code=200)
                  # Return Response ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # TOP PRODUCTS ============================================================ End

      # TOP SERVICES ============================================================ Begin
      def top_services(user_role, workshop_id, user_id, start_date, end_date, limit=5):
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

                  # Get Data ---------------------------------------- Start
                  query = db.session.query(
                        Services.id,
                        Services.name,
                        func.sum(
                              SaleServiceDetails.quantity
                        ).label("total_service")
                  ).join(
                        SaleServiceDetails,
                        Services.id == SaleServiceDetails.service_id
                  ).join(
                        Payments,
                        Payments.id == SaleServiceDetails.payment_id
                  ).filter(
                        Payments.workshop_id == workshop_id,
                        Payments.cashier_id == user_id,
                        Payments.is_delete == 0,
                        Services.is_delete == 0
                  )

                  if start_date is not None:
                        query = query.filter(
                              Payments.payment_date >= start_date
                        )

                  if end_date is not None:
                        query = query.filter(
                              Payments.payment_date <= end_date
                        )

                  services = query.group_by(
                        Services.id,
                        Services.name
                  ).order_by(
                        func.sum(
                              SaleServiceDetails.quantity
                        ).desc()
                  ).limit(limit).all()
                  # Get Data ---------------------------------------- Finish

                  # Initialize Data ---------------------------------------- Start
                  data = []

                  for service in services:
                        data.append({
                              "id": service.id,
                              "name": service.name,
                              "total_service": int(service.total_service)
                        })
                  # Initialize Data ---------------------------------------- Finish

                  # Return Response ---------------------------------------- Start
                  return success_data(data=data, status_code=200)
                  # Return Response ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # TOP SERVICES ============================================================ End

      # LOW STOCK ============================================================ Begin
      def low_stock(user_role, workshop_id, limit=5, minimum_stock=5):
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

                  # Get Data ---------------------------------------- Start
                  products = Products.query.filter(
                        Products.workshop_id == workshop_id,
                        Products.stock <= minimum_stock,
                        Products.is_delete == 0
                  ).order_by(
                        Products.stock.asc(),
                        Products.product_name.asc()
                  ).limit(limit).all()
                  # Get Data ---------------------------------------- Finish

                  # Initialize Data ---------------------------------------- Start
                  data = []

                  for product in products:
                        data.append({
                              "id": product.id,
                              "product_name": product.product_name,
                              "stock": product.stock,
                              "purchase": product.purchase_price,
                              "price": product.selling_price
                        })
                  # Initialize Data ---------------------------------------- Finish

                  # Return Response ---------------------------------------- Start
                  return success_data(data=data, status_code=200)
                  # Return Response ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # LOW STOCK ============================================================ End
      
      # RECENT TRANSACTIONS ============================================================ Begin
      def recent_transactions(user_role, workshop_id, user_id, limit=5):
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

                  # Get Data ---------------------------------------- Start
                  payments = Payments.query.filter(
                        Payments.workshop_id == workshop_id,
                        Payments.cashier_id == user_id,
                        Payments.is_delete == 0
                  ).order_by(
                        Payments.payment_date.desc()
                  ).limit(limit).all()
                  # Get Data ---------------------------------------- Finish

                  # Initialize Data ---------------------------------------- Start
                  data = []

                  for payment in payments:

                        payment_date = format_date(payment.payment_date)
                        created_at = format_date(payment.created_at)

                        data.append({
                              "id": payment.id,
                              "invoice": payment.invoice,
                              "customer_name": (
                                    payment.customers.customer_name
                                    if payment.customers else "Pelanggan Umum"
                              ),
                              "cashier": (
                                    payment.cashier.username
                                    if payment.cashier else "-"
                              ),
                              "total": payment.total,
                              "payment_date": payment_date,
                              "created_at": created_at
                        })
                  # Initialize Data ---------------------------------------- Finish

                  # Return Response ---------------------------------------- Start
                  return success_data(data=data, status_code=200)
                  # Return Response ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # RECENT TRANSACTIONS ============================================================ End

      # DEPOSIT SUMMARY ============================================================ Begin
      def deposit_summary(user_role, workshop_id, user_id):
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

                  # Today Timestamp ---------------------------------------- Start
                  today = datetime.now().date()

                  start_date = int(datetime.combine(
                        today,
                        datetime.min.time()
                  ).timestamp())

                  end_date = int(datetime.combine(
                        today,
                        datetime.max.time()
                  ).timestamp())
                  # Today Timestamp ---------------------------------------- Finish
            
                  # Get Deposit ---------------------------------------- Start
                  deposit = CashDeposits.query.filter(
                        CashDeposits.workshop_id == workshop_id,
                        CashDeposits.user_id == user_id,
                        CashDeposits.deposit_date >= start_date,
                        CashDeposits.deposit_date <= end_date,
                        CashDeposits.is_deleted == 0
                  ).order_by(
                        CashDeposits.deposit_date.desc()
                  ).first()
                  # Get Deposit ---------------------------------------- Finish
                  
                  # Initialize Data ---------------------------------------- Start
                  if deposit:

                        if deposit.status == 0:
                              status = "Menunggu"

                        elif deposit.status == 1:
                              status = "Disetujui"

                        elif deposit.status == 2:
                              status = "Ditolak"

                        else:
                              status = "-"

                        data = {
                              "total_sales": deposit.total_sales,
                              "total_deposit": deposit.total_deposit,
                              "difference": deposit.difference,
                              "status": status,
                              "deposit_date": format_date(deposit.deposit_date)
                        }

                  else:
                        data = {
                              "total_sales": 0,
                              "total_deposit": 0,
                              "difference": 0,
                              "status": "Belum Setor",
                              "deposit_date": "-"
                        }
                  # Initialize Data ---------------------------------------- Finish

                  # Return Response ---------------------------------------- Start
                  return success_data(data=data, status_code=200)
                  # Return Response ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # DEPOSIT SUMMARY ============================================================ End
      
      # CASHIER PROFILE ============================================================ Begin
      def cashier_profile(user_role, user_id):
            try:
                  # Access Validation ---------------------------------------- Start
                  access = role_validator(user_role)

                  if not access:
                        return authorization_error()
                  # Access Validation ---------------------------------------- Finish

                  # Get Cashier ---------------------------------------- Start
                  cashier = Users.query.filter_by(
                        id=user_id,
                        is_delete=0
                  ).first()

                  if not cashier:
                        return not_found(
                              "Cashier could not be found."
                        )
                  # Get Cashier ---------------------------------------- Finish

                  # Initialize Data ---------------------------------------- Start
                  data = {
                        "id": cashier.id,
                        "username": cashier.username,
                        "email": cashier.email,
                        "role": cashier.role,
                        "created_at": format_date(cashier.created_at)
                  }
                  # Initialize Data ---------------------------------------- Finish

                  # Return Response ---------------------------------------- Start
                  return success_data(data=data, status_code=200)
                  # Return Response ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # CASHIER PROFILE ============================================================ End
      
# DASHBOARD MODEL CLASS ============================================================ End