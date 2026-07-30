from datetime import datetime
import time

from apps import db
from apps.database.db_products import Products
from apps.database.db_categories import Categories
from apps.database.db_workshops import Workshops
from apps.utilities.responseHelpers import *
from apps.utilities.utilities import current_timestamp
from apps.utilities.formatter import format_date
from apps.utilities.validators import role_validator, product_validator, subscription_validator

# PRODUCT MODEL CLASS ============================================================ Begin
class ProductModels():

    # CREATE PRODUCT ============================================================ Begin
    def create_product(user_role, workshop_id, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)
            if not access:
                return authorization_error()
            
            subscription_access = subscription_validator(user_role, workshop_id)

            if not subscription_access:
                return subscription_required()
            # Access Validation ---------------------------------------- Finish

            # Check Request Body ---------------------------------------- Start
            if datas is None:
                return invalid_params()

            required_data = [
                "category_id",
                "product_name",
                "stock",
                "minimum_stock",
                "purchase",
                "price"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )
            # Check Request Body ---------------------------------------- Finish

            # Initialize Data Input ---------------------------------------- Start
            category_id = datas["category_id"]
            barcode = str(datas.get("barcode", "")).strip()
            product_name = datas["product_name"].strip()
            stock = datas["stock"]
            minimum_stock = datas["minimum_stock"]
            purchase_price = datas["purchase"]
            selling_price = datas["price"]
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checker_result = product_validator(
                category_id,
                barcode,
                product_name,
                stock,
                minimum_stock,
                purchase_price,
                selling_price,
                workshop_id
            )

            if len(checker_result) != 0:
                return defined_error(
                    checker_result,
                    "Defined Error",
                    499
                )
            # Data Validation ---------------------------------------- Finish

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

            # Insert Data ---------------------------------------- Start
            timestamp = current_timestamp()


            data = Products(
                workshop_id=workshop.id,
                category_id=category_id,
                barcode=barcode if barcode != "" else None,
                product_name=product_name,
                stock=stock,
                minimum_stock=minimum_stock,
                purchase_price=purchase_price,
                selling_price=selling_price,
                created_at=timestamp,
                updated_at=timestamp
            )

            try:
                db.session.add(data)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ========================================
            return success(status_code=201)

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # CREATE PRODUCT ============================================================ End

    # READ PRODUCT ============================================================ Begin
    def read_product(user_role, workshop_id):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)
            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Get Product Data ---------------------------------------- Start
            products = (
                Products.query
                .join(
                    Categories,
                    Products.category_id == Categories.id
                )
                .filter(
                    Products.workshop_id == workshop_id,
                    Products.is_delete == 0,
                    Categories.is_delete == 0
                )
                .order_by(Products.id.desc())
                .all()
            )
            # Get Product Data ---------------------------------------- Finish

            # Initialize Data ---------------------------------------- Start
            data = []

            for product in products:
                created_date = format_date(product.created_at)
                updated_date = format_date(product.updated_at)

                deleted_date = None

                if product.deleted_at:
                    deleted_date = format_date(product.deleted_at)

                data.append({
                    "id": product.id,
                    "category_id": product.category_id,
                    "category": product.categories.category,
                    "barcode": product.barcode,
                    "product_name": product.product_name,
                    "stock": product.stock,
                    "minimum_stock": product.minimum_stock,
                    "purchase_price": product.purchase_price,
                    "selling_price": product.selling_price,
                    "created_at": product.created_at,
                    "created_date": created_date,
                    "updated_at": product.updated_at,
                    "updated_date": updated_date,
                    "deleted_at": product.deleted_at,
                    "deleted_date": deleted_date
                })
            # Initialize Data ---------------------------------------- Finish

            # Return Response ========================================
            return success_data(
                data=data,
                status_code=200
            )

        except Exception as e:
            return bad_request(str(e))
    # READ PRODUCT ============================================================ End
    
    # UPDATE PRODUCT ============================================================ Begin
    def update_product(user_role, workshop_id, product_id, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)
            if not access:
                return authorization_error()
            
            subscription_access = subscription_validator(user_role, workshop_id)

            if not subscription_access:
                return subscription_required()
            # Access Validation ---------------------------------------- Finish

            # Check Request Body ---------------------------------------- Start
            if datas is None:
                return invalid_params()

            required_data = [
                "category_id",
                "product_name",
                "stock",
                "minimum_stock",
                "purchase",
                "price"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )
            # Check Request Body ---------------------------------------- Finish

            # Check Product ---------------------------------------- Start
            product = Products.query.filter_by(
                id=product_id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not product:
                return not_found(
                    "Product could not be found."
                )
            # Check Product ---------------------------------------- Finish

            # Initialize Data Input ---------------------------------------- Start
            category_id = datas["category_id"]
            barcode = str(datas.get("barcode", "")).strip()
            product_name = datas["product_name"].strip()
            stock = datas["stock"]
            minimum_stock = datas["minimum_stock"]
            purchase_price = datas["purchase"]
            selling_price = datas["price"]
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checker_result = []

            checker_result = product_validator(
                category_id,
                barcode,
                product_name,
                stock,
                minimum_stock,
                purchase_price,
                selling_price,
                workshop_id,
                product_id
            )

            if len(checker_result) != 0:
                return defined_error(
                    checker_result,
                    "Defined Error",
                    499
                )
            # Data Validation ---------------------------------------- Finish

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

            # Update Data ---------------------------------------- Start
            product.category_id = category_id
            product.barcode = barcode if barcode != "" else None
            product.product_name = product_name
            product.stock = stock
            product.minimum_stock = minimum_stock
            product.purchase_price = purchase_price
            product.selling_price = selling_price
            product.updated_at = current_timestamp()


            try:
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Update Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ========================================
            return success(status_code=200)

        except Exception as e:
            return bad_request(str(e))
    # UPDATE PRODUCT ============================================================ End

        # DELETE PRODUCT ============================================================ Begin
    def delete_product(user_role, workshop_id, product_id):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)
            if not access:
                return authorization_error()
            
            subscription_access = subscription_validator(user_role, workshop_id)

            if not subscription_access:
                return subscription_required()
            # Access Validation ---------------------------------------- Finish

            # Check Product ---------------------------------------- Start
            product = Products.query.filter_by(
                id=product_id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not product:
                return not_found(
                    "Product could not be found."
                )
            # Check Product ---------------------------------------- Finish

            # Delete Product ---------------------------------------- Start
            timestamp = current_timestamp()
            product.is_delete = 1
            product.deleted_at = timestamp
            product.updated_at = timestamp

            try:
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Delete Product ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ========================================
            return success(status_code=200)

        except Exception as e:
            return bad_request(str(e))
    # DELETE PRODUCT ============================================================ End

# PRODUCT MODEL CLASS ============================================================ End