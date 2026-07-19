from datetime import datetime
import time

from apps import db
from apps.database.db_products import Products
from apps.database.db_categories import Categories
from apps.database.db_workshops import Workshops
from apps.utilities.responseHelpers import *
from apps.utilities.utilities import split_date_time
from apps.utilities.validators import role_validator, product_validator

# PRODUCT MODEL CLASS ============================================================ Begin
class ProductModels():

    # CREATE PRODUCT ============================================================ Begin
    def create_product(user_role, workshop_id, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)
            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Check Request Body ---------------------------------------- Start
            if datas is None:
                return invalid_params()

            required_data = [
                "category_id",
                "product_name",
                "stock",
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
            product_name = datas["product_name"].strip()
            stock = datas["stock"]
            purchase_price = datas["purchase"]
            selling_price = datas["price"]
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checker_result = product_validator(
                category_id,
                product_name,
                stock,
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
            timestamp = int(time.time() * 1000)

            data = Products(
                workshop_id=workshop.id,
                category_id=category_id,
                product_name=product_name,
                stock=stock,
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
            return success(status_code=200)

        except Exception as e:
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
                created_at = split_date_time(
                    datetime.fromtimestamp(product.created_at / 1000)
                )

                updated_at = split_date_time(
                    datetime.fromtimestamp(product.updated_at / 1000)
                )

                deleted_at = None

                if product.deleted_at:
                    deleted_at = split_date_time(
                        datetime.fromtimestamp(product.deleted_at / 1000)
                    )

                data.append({
                    "id": product.id,
                    "category_id": product.category_id,
                    "category": product.categories.category,
                    "product_name": product.product_name,
                    "stock": product.stock,
                    "purchase_price": product.purchase_price,
                    "selling_price": product.selling_price,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "deleted_at": deleted_at
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
            # Access Validation ---------------------------------------- Finish

            # Check Request Body ---------------------------------------- Start
            if datas is None:
                return invalid_params()

            required_data = [
                "category_id",
                "product_name",
                "stock",
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
            product_name = datas["product_name"].strip()
            stock = datas["stock"]
            purchase_price = datas["purchase"]
            selling_price = datas["price"]
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checker_result = []

            checker_result = product_validator(
                category_id,
                product_name,
                stock,
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
            product.product_name = product_name
            product.stock = stock
            product.purchase_price = purchase_price
            product.selling_price = selling_price
            product.updated_at = int(time.time() * 1000)

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
            product.is_delete = 1
            product.deleted_at = int(time.time() * 1000)
            product.updated_at = int(time.time() * 1000)

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