from flask_jwt_extended import get_jwt
from flask import render_template
from apps import db

from apps.database.db_customers import Customers
from apps.database.db_vehicles import Vehicles
from apps.database.db_products import Products
from apps.database.db_services import Services
from apps.database.db_payment import Payments
from apps.database.db_sale_details import SaleDetails
from apps.database.db_sale_service_details import SaleServiceDetails

from apps.utilities.responseHelpers import *
from apps.utilities.validators import sale_validator
from apps.utilities.formatter import format_datetime

import time
from datetime import datetime


# CASHIER MODEL CLASS ============================================================ Begin
class CashierModels():

    # GET CUSTOMERS ============================================================ Begin
    def get_customers(workshop_id):
        try:

            customers = Customers.query.filter_by(
                workshop_id=workshop_id,
                is_delete=0
            ).order_by(
                Customers.customer_name.asc()
            ).all()

            data = []

            for customer in customers:

                data.append({
                    "id": customer.id,
                    "customer_name": customer.customer_name,
                    "customer_phone": customer.customer_phone
                })

            return success_data(data=data,status_code=200)

        except Exception as e:
            return bad_request(str(e))
    # GET CUSTOMERS ============================================================ End



    # CUSTOMER VEHICLES ============================================================ Begin
    def customer_vehicles(customer_id, workshop_id):
        try:

            vehicles = Vehicles.query.filter_by(
                customer_id=customer_id,
                workshop_id=workshop_id,
                is_delete=0
            ).order_by(
                Vehicles.plate_number.asc()
            ).all()

            data = []

            for vehicle in vehicles:

                data.append({
                    "id": vehicle.id,
                    "plate_number": vehicle.plate_number,
                    "vehicle_name": f"{vehicle.vehicle_brand} {vehicle.vehicle_type}",
                    "vehicle_brand": vehicle.vehicle_brand,
                    "vehicle_type": vehicle.vehicle_type,
                    "vehicle_year": vehicle.vehicle_year,
                    "vehicle_color": vehicle.vehicle_color
                })

            return success(data)

        except Exception as e:
            return bad_request(str(e))
    # CUSTOMER VEHICLES ============================================================ End

    # SEARCH ITEM ============================================================ Begin
    def search_items(keyword, workshop_id):
        try:

            keyword = keyword.strip()

            data = []

            # ==================================================
            # SEARCH PRODUCT BY BARCODE
            # ==================================================

            product = Products.query.filter_by(
                barcode=keyword,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if product:

                data.append({
                    "id": product.id,
                    "type": "product",
                    "barcode": product.barcode,
                    "name": product.product_name,
                    "price": product.selling_price,
                    "stock": product.stock
                })

                return success_data(data=data,status_code=200)

            # ==================================================
            # SEARCH PRODUCT NAME
            # ==================================================

            products = Products.query.filter(
                Products.workshop_id == workshop_id,
                Products.is_delete == 0,
                Products.product_name.ilike(f"%{keyword}%")
            ).all()

            for product in products:

                data.append({
                    "id": product.id,
                    "type": "product",
                    "name": product.product_name,
                    "price": product.selling_price,
                    "stock": product.stock
                })

            # ==================================================
            # SEARCH SERVICE NAME
            # ==================================================

            services = Services.query.filter(
                Services.workshop_id == workshop_id,
                Services.is_delete == 0,
                Services.name.ilike(f"%{keyword}%")
            ).all()

            for service in services:

                data.append({
                    "id": service.id,
                    "type": "service",
                    "name": service.name,
                    "price": service.service_fee,
                    "stock": "-"
                })

            return success_data(data=data,status_code=200)

        except Exception as e:
            return bad_request(str(e))
    # SEARCH ITEM ============================================================ End

    # CHECKOUT ============================================================ Begin
    def checkout(datas):
        try:

            claims = get_jwt()

            workshop_id = claims["ws_id"]
            role = claims["role"]

            OWNER = "1"
            CASHIER = "2"

            if role not in [OWNER, CASHIER]:
                return bad_request("Anda tidak memiliki akses.")
            customer_id = datas.get("customer_id")
            vehicle_id = datas.get("vehicle_id")
            payment = datas.get("payment")
            product_details = datas.get("product_details", [])
            service_details = datas.get("service_details", [])

            validation = sale_validator(
                customer_id,
                vehicle_id,
                payment,
                product_details,
                service_details,
                workshop_id
            )

            if validation:
                return bad_request(validation)

            # ==================================================
            # HITUNG TOTAL BARANG
            # ==================================================

            total = 0

            for item in product_details:

                product = Products.query.filter_by(
                    id=item["product_id"],
                    workshop_id=workshop_id,
                    is_delete=0
                ).first()

                if not product:
                    return bad_request("Produk tidak ditemukan.")

                qty = int(item["quantity"])

                if qty > product.stock:
                    return bad_request(
                        f"Stok {product.product_name} tidak mencukupi."
                    )

                total += product.selling_price * qty

            # ==================================================
            # HITUNG TOTAL JASA
            # ==================================================

            for item in service_details:

                service = Services.query.filter_by(
                    id=item["service_id"],
                    workshop_id=workshop_id,
                    is_delete=0
                ).first()

                if not service:
                    return bad_request("Jasa tidak ditemukan.")

                qty = int(item["quantity"])

                total += service.service_fee * qty

            payment = int(payment)

            if payment < total:
                return bad_request(
                    "Nominal pembayaran kurang."
                )

            change = payment - total

            now = int(time.time())

            # ==================================================
            # HEADER TRANSAKSI
            # ==================================================

            trx = Payments(
                cashier_id=claims["id"],

                workshop_id=workshop_id,

                customer_id=customer_id or None,

                vehicle_id=vehicle_id or None,

                payment_date=now,

                total=total,

                paid=payment,

                change=change,

                created_at=now,

                updated_at=now

            )

            db.session.add(trx)
            # simpan dulu untuk mendapatkan id
            db.session.flush()

            # Generate nomor invoice
            trx.invoice = (
                f"INV-{datetime.now().strftime('%Y%m%d')}-{trx.id:06d}"
            )
            # ==================================================
            # DETAIL BARANG
            # ==================================================

            for item in product_details:

                product = Products.query.get(item["product_id"])

                qty = int(item["quantity"])

                subtotal = qty * product.selling_price

                detail = SaleDetails(

                    payment_id=trx.id,

                    product_id=product.id,

                    quantity=qty,

                    unit_price=product.selling_price,

                    subtotal=subtotal

                )

                db.session.add(detail)

                product.stock -= qty

            # ==================================================
            # DETAIL JASA
            # ==================================================

            for item in service_details:

                service = Services.query.get(item["service_id"])

                qty = int(item["quantity"])

                subtotal = qty * service.service_fee

                detail = SaleServiceDetails(

                    payment_id=trx.id,

                    service_id=service.id,

                    quantity=qty,

                    service_price=service.service_fee,

                    subtotal=subtotal

                )

                db.session.add(detail)

            db.session.commit()

            return success({

                "payment_id": trx.id,

                "total": total,

                "paid": payment,

                "change": change

            })

        except Exception as e:

            db.session.rollback()

            return bad_request(str(e))
    # CHECKOUT ============================================================ End

    # HISTORY ============================================================ Begin
    def history(workshop_id):
        try:

            payments = Payments.query.filter_by(
                workshop_id=workshop_id,
                is_delete=0
            ).order_by(
                Payments.payment_date.desc()
            ).all()

            data = []

            for payment in payments:

                data.append({

                    "id": payment.id,

                    "customer":
                        payment.customers.customer_name
                        if payment.customers
                        else "Pelanggan Umum",

                    "vehicle":
                        payment.vehicles.plate_number
                        if payment.vehicles
                        else "-",

                    "payment_date": payment.payment_date,

                    "total": payment.total,

                    "paid": payment.paid,

                    "change": payment.change

                })

            return success_data(data=data,status_code=200)

        except Exception as e:
            return bad_request(str(e))
    # HISTORY ============================================================ End



    # DETAIL ============================================================ Begin
    def detail(payment_id, workshop_id):
        try:

            payment = Payments.query.filter_by(
                id=payment_id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not payment:
                return bad_request(
                    "Data transaksi tidak ditemukan."
                )

            products = []

            for item in payment.sale_details:

                products.append({

                    "product_name":
                        item.products.product_name,

                    "quantity":
                        item.quantity,

                    "price":
                        item.unit_price,

                    "subtotal":
                        item.subtotal

                })

            services = []

            for item in payment.sale_service_details:

                services.append({

                    "service_name":
                        item.services.name,

                    "quantity":
                        item.quantity,

                    "price":
                        item.service_price,

                    "subtotal":
                        item.subtotal

                })

            return success({

                "payment": {

                    "id": payment.id,

                    "customer":
                        payment.customers.customer_name
                        if payment.customers
                        else "Pelanggan Umum",

                    "vehicle":
                        payment.vehicles.plate_number
                        if payment.vehicles
                        else "-",

                    "payment_date":
                        payment.payment_date,

                    "total":
                        payment.total,

                    "paid":
                        payment.paid,

                    "change":
                        payment.change

                },

                "products": products,

                "services": services

            })

        except Exception as e:
            return bad_request(str(e))
    # DETAIL ============================================================ End


    # PRINT RECEIPT ============================================================ Begin
    def print_receipt(payment_id, workshop_id):
        try:

            payment = Payments.query.filter_by(
                id=payment_id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not payment:

                return bad_request(
                    "Data transaksi tidak ditemukan."
                )

            return render_template(
                "pages/appPages/receipt.html",
                payment=payment,
                payment_date=format_datetime(payment.payment_date)
            )

        except Exception as e:
            return bad_request(str(e))
    # PRINT RECEIPT ============================================================ End

# CASHIER MODEL CLASS ============================================================ End