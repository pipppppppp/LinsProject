from datetime import datetime
from sqlalchemy import func
from ... import db
from ...database.db_workshops import Workshops
from ...database.db_customers import Customers
from ...database.db_cash_deposits import CashDeposits
from ...database.db_payment import Payments
from ...utilities.validators import role_validator, cash_deposit_validator

from apps.utilities.responseHelpers import *
from apps.utilities.utilities import current_timestamp
from apps.utilities.formatter import format_date
# CASH DEPOSIT MODEL CLASS ============================================================ Begin
class CashDepositModels():
    # CREATE CASH DEPOSIT ============================================================ Begin
    def create_cash_deposit(user_role, workshop_id,user_id, datas):
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
                "total_deposit",
                "notes"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )
            # Check Request Body ---------------------------------------- Finish
            
           # Initialize Data Input ---------------------------------------- Start
            total_deposit = int(datas["total_deposit"])
            notes = datas["notes"].strip()
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checker_result = cash_deposit_validator(total_deposit)

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

            # Get Total Sales ---------------------------------------- Start
            today = datetime.now().date()

            start_timestamp = int(
                datetime.combine(today, datetime.min.time()).timestamp()
            )

            end_timestamp = int(
                datetime.combine(today, datetime.max.time()).timestamp()
            )
            total_sales = db.session.query(
                  db.func.coalesce(func.sum(Payments.total),0)
            ).filter(
                  Payments.workshop_id == workshop_id,
                  Payments.cashier_id == user_id,
                  Payments.payment_date >= start_timestamp,
                  Payments.payment_date <= end_timestamp,
                  Payments.is_delete == 0
            ).scalar()
            timestamp = current_timestamp()
            # Get Total Sales ---------------------------------------- Finish

            # Calculate Difference ---------------------------------------- Start
            difference = total_sales - total_deposit
            # Calculate Difference ---------------------------------------- Finish

            # Insert Data ---------------------------------------- Start
            data = CashDeposits(
                workshop_id=workshop_id,
                user_id=user_id,
                deposit_date=timestamp,
                total_sales=total_sales,
                total_deposit=total_deposit,
                difference=difference,
                notes=notes,
                status=0,
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

            # Return Response ======================================== 
            # return success(statusCode=201)
            return success(
                status_code=201
            )
        
        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # CREATE CASH DEPOSIT ============================================================ End

    # READ CASH DEPOSIT ============================================================ Begin
    def read_cash_deposit(user_role, workshop_id, user_id):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)
            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish
            today = datetime.now().date()

            start_date = int(datetime.combine(today, datetime.min.time()).timestamp())
            end_date = int(datetime.combine(today, datetime.max.time()).timestamp())
            today_sales = db.session.query(
                func.coalesce(func.sum(Payments.total), 0)
            ).filter(
                Payments.workshop_id == workshop_id,
                Payments.cashier_id == user_id,
                Payments.payment_date >= start_date,
                Payments.payment_date <= end_date,
                Payments.is_delete == 0
            ).scalar()
            # Get Data ---------------------------------------- Start
            if user_role == "cashier":
                  cash_deposits = CashDeposits.query.filter_by(
                        workshop_id=workshop_id,
                        user_id=user_id,
                        is_deleted=0
                  ).all()
            else:
                  cash_deposits = CashDeposits.query.filter_by(
                        workshop_id=workshop_id,
                        is_deleted=0
                  ).all()
            # Get Data ---------------------------------------- Finish
            
            # Initialize Data ---------------------------------------- Start
            data = []

            for cash_deposit in cash_deposits:

                deposit_date = format_date(cash_deposit.deposit_date)
                created_at = format_date(cash_deposit.created_at)
                updated_at = format_date(cash_deposit.updated_at)
                deleted_at = None

                if cash_deposit.deleted_at:
                    deleted_at = format_date(cash_deposit.deleted_at)

                data.append({
                        "id": cash_deposit.id,
                        "user_id": cash_deposit.user_id,
                        "deposit_date": deposit_date,
                        "total_sales": cash_deposit.total_sales,
                        "total_deposit": cash_deposit.total_deposit,
                        "difference": cash_deposit.difference,
                        "notes": cash_deposit.notes,
                        "status": cash_deposit.status,
                        "verified_by": cash_deposit.verified_by,
                        "verified_at": format_date(cash_deposit.verified_at) if cash_deposit.verified_at else None,
                        "created_at": created_at,
                        "updated_at": updated_at,
                        "deleted_at": deleted_at
                  })
            # Initialize Data ---------------------------------------- Finish
            # Response Data ---------------------------------------- Start
            return success_data(
                data={
                    "history": data,
                    "today_sales": today_sales
                },
                status_code=200
            )
        
        except Exception as e:
            return bad_request(str(e))
    # READ CASH DEPOSIT ============================================================ End

    # DELETE CASH DEPOSIT ============================================================ Begin
    def delete_cash_deposit(user_role, workshop_id, id):
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

            # Check Cash Deposit ---------------------------------------- Start
            data = CashDeposits.query.filter_by(
                id=id,
                workshop_id=workshop_id,
                is_deleted=0
            ).first()

            if not data:
                return not_found(
                    "Cash deposit could not be found."
                )
            # Check Cash Deposit ---------------------------------------- Finish
            # Delete Data ---------------------------------------- Start
            timestamp = current_timestamp()

            data.is_deleted = 1
            data.deleted_at = timestamp
            data.updated_at = timestamp

            try:
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Delete Data ---------------------------------------- Finish

            # Return Response ========================================
            return success(
                status_code=200
            )

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # DELETE CASH DEPOSIT ============================================================ End
# CASH DEPOSIT MODEL CLASS ============================================================ End