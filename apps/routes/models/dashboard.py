from sqlalchemy import func
from datetime import datetime

from ... import db

from ...database.db_payment import Payments
from ...database.db_purchases import Purchases
from ...database.db_products import Products
from ...database.db_services import Services
from ...database.db_customers import Customers
from ...database.db_sale_details import SaleDetails
from ...database.db_sale_service_details import SaleServiceDetails
from ...database.db_workshops import Workshops
from ...utilities.validators import role_validator
from ...utilities.formatter import format_date

from apps.utilities.responseHelpers import *


# DASHBOARD MODEL CLASS ============================================================ Begin
class DashboardModels():

      # DASHBOARD SUMMARY ============================================================ Begin
      def dashboard_summary(user_role, workshop_id):
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

                  # Total Payment/penjualan ---------------------------------------- Start
                  total_payments = db.session.query(
                        func.coalesce(func.sum(Payments.total), 0)
                  ).filter(
                        Payments.workshop_id == workshop_id,
                        Payments.is_delete == 0
                  ).scalar()
                  # Total Payment/penjualan ---------------------------------------- Finish
                  
                  # Total Purchase ---------------------------------------- Start
                  total_purchase = db.session.query(
                        func.coalesce(func.sum(Purchases.total), 0)
                  ).filter(
                        Purchases.workshop_id == workshop_id,
                        Purchases.is_delete == 0
                  ).scalar()
                  # Total Purchase ---------------------------------------- Finish

                  # Total Transaction ---------------------------------------- Start
                  total_transaction = Payments.query.filter_by(
                        workshop_id=workshop_id,
                        is_delete=0
                  ).count()
                  # Total Transaction ---------------------------------------- Finish

                  # Total Customer ---------------------------------------- Start
                  total_customer = Customers.query.filter_by(
                        workshop_id=workshop_id,
                        is_delete=0
                  ).count()
                  # Total Customer ---------------------------------------- Finish

                  # Total Product ---------------------------------------- Start
                  total_product = Products.query.filter_by(
                        workshop_id=workshop_id,
                        is_delete=0
                  ).count()
                  # Total Product ---------------------------------------- Finish

                  # Total Services ---------------------------------------- Start
                  total_service = Services.query.filter(
                        Services.workshop_id == workshop_id,
                        Services.is_delete == 0
                  ).count()
                  # Total Services ---------------------------------------- Finish

                  # Initialize Data ---------------------------------------- Start
                  data = {
                        "total_payments": total_payments,
                        "total_purchase": total_purchase,
                        "total_transaction": total_transaction,
                        "total_customer": total_customer,
                        "total_product": total_product,
                        "total_service": total_service
                  }
                  # Initialize Data ---------------------------------------- Finish

                  # Return Response ---------------------------------------- Start
                  return success_data(data=data, status_code=200)
                  # Return Response ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # DASHBOARD SUMMARY ============================================================ End

      # SALES CHART ============================================================ Begin
      def payments_chart(user_role, workshop_id, start_date, end_date):
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
                  return success_data(
                        data=data,
                        status_code=200
                  )
                  # Return Response ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # SALES CHART ============================================================ End

      # PURCHASE CHART ============================================================ Begin
      def purchase_chart(user_role, workshop_id, start_date, end_date):
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
                        Purchases.purchase_date,
                        func.sum(Purchases.total).label("total")
                  ).filter(
                        Purchases.workshop_id == workshop_id,
                        Purchases.is_delete == 0
                  )

                  if start_date is not None:
                        query = query.filter(
                              Purchases.purchase_date >= start_date
                  )

                  if end_date is not None:
                        query = query.filter(
                              Purchases.purchase_date <= end_date
                  )

                  purchases = query.group_by(
                        Purchases.purchase_date
                  ).order_by(
                        Purchases.purchase_date
                  ).all()
                  # Get Data ---------------------------------------- Finish

                  # Initialize Data ---------------------------------------- Start
                  data = []

                  for purchase in purchases:
                        data.append({
                              "date": format_date(purchase.purchase_date),
                              "total": int(purchase.total)
                        })
                  # Initialize Data ---------------------------------------- Finish

                  # Return Response ---------------------------------------- Start
                  return success_data(
                        data=data,
                        status_code=200
                  )
                  # Return Response ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # PURCHASE CHART ============================================================ End

      # TOP PRODUCTS ============================================================ Begin
      def top_products(user_role, workshop_id, start_date, end_date, limit=5):
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
                        Payments.is_delete == 0,
                        Products.is_delete == 0
                  ).group_by(
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
                  return success_data(
                        data=data,
                        status_code=200
                  )
                  # Return Response ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # TOP PRODUCTS ============================================================ End

      # TOP SERVICES ============================================================ Begin
      def top_services(user_role, workshop_id, start_date, end_date, limit=5):
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
                  return success_data(
                        data=data,
                        status_code=200
                  )
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
                  return success_data(
                        data=data,
                        status_code=200
                  )
                  # Return Response ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # LOW STOCK ============================================================ End
      
      # RECENT TRANSACTIONS ============================================================ Begin
      def recent_transactions(user_role, workshop_id, limit=5):
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
                  payments = Payments.query.filter_by(
                        workshop_id=workshop_id,
                        is_delete=0
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
                  return success_data(
                        data=data,
                        status_code=200
                  )
                  # Return Response ---------------------------------------- Finish

            except Exception as e:
                  return bad_request(str(e))
      # RECENT TRANSACTIONS ============================================================ End

# DASHBOARD MODEL CLASS ============================================================ End