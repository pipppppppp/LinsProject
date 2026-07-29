from datetime import datetime
from sqlalchemy import func
from ... import db

from ...database.db_users import Users
from ...database.db_workshops import Workshops
from ...database.db_customers import Customers
from ...database.db_cash_deposits import CashDeposits
from ...database.db_payment import Payments
from ...utilities.validators import role_validator, cash_deposit_validator, subscription_validator

from apps.utilities.responseHelpers import *
from apps.utilities.utilities import current_timestamp
from apps.utilities.formatter import format_date, format_date_timestamp
# CASH DEPOSIT MODEL CLASS ============================================================ Begin
class CashDepositModels():
    # CREATE CASH DEPOSIT ============================================================ Begin
    def create_cash_deposit(user_role, workshop_id, user_id, datas):
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

            # Timestamp For Deposit (Milliseconds) -------------------- Start
            start_deposit = start_timestamp * 1000
            end_deposit = end_timestamp * 1000
            # Timestamp For Deposit (Milliseconds) -------------------- Finish
           
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
            
            # Approved Deposit ---------------------------------------- Start
            approved_deposit = db.session.query(
                func.coalesce(func.sum(CashDeposits.total_deposit), 0)
            ).filter(
                CashDeposits.workshop_id == workshop_id,
                CashDeposits.user_id == user_id,
                CashDeposits.deposit_date >= start_deposit,
                CashDeposits.deposit_date <= end_deposit,
                CashDeposits.status == 1,
                CashDeposits.is_deleted == 0
            ).scalar()
            approved_data = CashDeposits.query.filter(
                CashDeposits.workshop_id == workshop_id,
                CashDeposits.user_id == user_id,
                CashDeposits.deposit_date >= start_deposit,
                CashDeposits.deposit_date <= end_deposit,
                CashDeposits.status == 1,
                CashDeposits.is_deleted == 0
            ).all()

            remaining = max(0, total_sales - approved_deposit)
            # Approved Deposit ---------------------------------------- Finish
            
            # Check Remaining Deposit ---------------------------------------- Start
            if remaining == 0:
                return defined_error(
                    "Seluruh hasil penjualan hari ini sudah disetor.",
                    "Defined Error",
                    499
                )
            # Check Remaining Deposit ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checker_result = cash_deposit_validator(total_deposit, remaining)

            if len(checker_result) != 0:
                return defined_error(
                    checker_result,
                    "Defined Error",
                    499
                )
            # Data Validation ---------------------------------------- Finish
            
            # Check Pending Deposit ---------------------------------------- Start
            pending_deposit = CashDeposits.query.filter_by(
                workshop_id=workshop_id,
                user_id=user_id,
                status=0,
                is_deleted=0
            ).first()

            if pending_deposit:
                return defined_error(
                    "Masih ada setor kas yang menunggu verifikasi.",
                    "Defined Error",
                    499
                )
            # Check Pending Deposit ---------------------------------------- Finish

            # Calculate Difference ---------------------------------------- Start
            difference = remaining - total_deposit
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
    def read_cash_deposit(user_role, workshop_id, user_id, date="", status=""):
        try:

            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)

            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Today Sales ---------------------------------------------- Start
            today = datetime.now().date()

            start_date = int(
                datetime.combine(
                    today,
                    datetime.min.time()
                ).timestamp()
            )

            end_date = int(
                datetime.combine(
                    today,
                    datetime.max.time()
                ).timestamp()
            )

            # Deposit Timestamp (Milliseconds) ------------------------- Start
            start_deposit = start_date * 1000
            end_deposit = end_date * 1000
            # Deposit Timestamp (Milliseconds) ------------------------- Finish

            # Summary ---------------------------------------------- Start
            if str(user_role) == "2":

                today_sales = db.session.query(
                    func.coalesce(func.sum(Payments.total), 0)
                ).filter(
                    Payments.workshop_id == workshop_id,
                    Payments.cashier_id == user_id,
                    Payments.payment_date >= start_date,
                    Payments.payment_date <= end_date,
                    Payments.is_delete == 0
                ).scalar()

                total_deposit = db.session.query(
                    func.coalesce(func.sum(CashDeposits.total_deposit), 0)
                ).filter(
                    CashDeposits.workshop_id == workshop_id,
                    CashDeposits.user_id == user_id,
                    CashDeposits.deposit_date >= start_deposit,
                    CashDeposits.deposit_date <= end_deposit,
                    CashDeposits.status == 1,
                    CashDeposits.is_deleted == 0
                ).scalar()

            else:

                today_sales = db.session.query(
                    func.coalesce(func.sum(Payments.total), 0)
                ).filter(
                    Payments.workshop_id == workshop_id,
                    Payments.payment_date >= start_date,
                    Payments.payment_date <= end_date,
                    Payments.is_delete == 0
                ).scalar()

                total_deposit = db.session.query(
                    func.coalesce(func.sum(CashDeposits.total_deposit), 0)
                ).filter(
                    CashDeposits.workshop_id == workshop_id,
                    CashDeposits.deposit_date >= start_deposit,
                    CashDeposits.deposit_date <= end_deposit,
                    CashDeposits.status == 1,
                    CashDeposits.is_deleted == 0
                ).scalar()

            remaining = max(0, today_sales - total_deposit)
            # Summary ---------------------------------------------- Finish
            
            # Get Query ----------------------------------------------- Start
            if str(user_role) == "2":

                query = db.session.query(
                    CashDeposits,
                    Users.username.label("cashier_name")
                ).join(
                    Users,
                    CashDeposits.user_id == Users.id
                ).filter(
                    CashDeposits.workshop_id == workshop_id,
                    CashDeposits.user_id == user_id,
                    CashDeposits.is_deleted == 0
                )

            else:

                query = db.session.query(
                    CashDeposits,
                    Users.username.label("cashier_name")
                ).join(
                    Users,
                    CashDeposits.user_id == Users.id
                ).filter(
                    CashDeposits.workshop_id == workshop_id,
                    CashDeposits.is_deleted == 0
                )
            # Get Query ----------------------------------------------- Finish

            # Filter Date --------------------------------------------- Start
            if date:
                    start = format_date_timestamp(date)
                    end = format_date_timestamp(date, True)

                    query = query.filter(
                        CashDeposits.deposit_date >= start,
                        CashDeposits.deposit_date <= end
                    )
            # Filter Date --------------------------------------------- Finish

            # Filter Status ------------------------------------------- Start
            if status != "":
                query = query.filter(
                    CashDeposits.status == int(status)
                )
            # Filter Status ------------------------------------------- Finish

            cash_deposits = query.order_by(
                CashDeposits.deposit_date.desc()
            ).all()

            # Initialize Data ----------------------------------------- Start
            data = []

            for cash_deposit, cashier_name in cash_deposits:
                # Deposit Status ---------------------------------------- Start
                status_name = {
                    0: "Menunggu",
                    1: "Disetujui",
                    2: "Ditolak"
                }.get(cash_deposit.status, "-")
                # Deposit Status ---------------------------------------- Finish
                
                deposit_date = format_date(cash_deposit.deposit_date)
                created_at = format_date(cash_deposit.created_at)
                updated_at = format_date(cash_deposit.updated_at)

                deleted_at = None

                if cash_deposit.deleted_at:
                    deleted_at = format_date(
                        cash_deposit.deleted_at
                    )
                
                data.append({
                    "id": cash_deposit.id,
                    "user_id": cash_deposit.user_id,
                    "cashier_name": cashier_name,
                    "deposit_date": deposit_date,
                    "total_sales": cash_deposit.total_sales,
                    "total_deposit": cash_deposit.total_deposit,
                    "difference": cash_deposit.difference,
                    "notes": cash_deposit.notes,
                    "status": cash_deposit.status,
                    "status_name":status_name,
                    "verified_by": (
                        cash_deposit.verifier.username
                        if cash_deposit.verifier
                        else "-"
                    ),
                    "verified_at": (
                        format_date(cash_deposit.verified_at)
                        if cash_deposit.verified_at
                        else None
                    ),
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "deleted_at": deleted_at
                })

            # Initialize Data ----------------------------------------- Finish

            return success_data(
                data={
                    "history": data,
                    "today_sales": today_sales,
                    "total_deposit": total_deposit,
                    "remaining": remaining
                },
                status_code=200
            )

        except Exception as e:
            return bad_request(str(e))
    # READ CASH DEPOSIT ============================================================ End
    
    # VERIFY CASH DEPOSIT ============================================================ Begin
    def verify_cash_deposit(user_role, workshop_id, user_id, datas):
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
                "deposit_id",
                "status"
            ]

            for req in required_data:
                if req not in datas:
                    return parameter_error(
                        f"Missing {req} in request body."
                    )
            # Check Request Body ---------------------------------------- Finish

            # Initialize Data ---------------------------------------- Start
            deposit_id = int(datas["deposit_id"])
            status = int(datas["status"])
            # Initialize Data ---------------------------------------- Finish

            # Validate Status ---------------------------------------- Start
            if status not in [1, 2]:
                return parameter_error(
                    "Invalid verification status."
                )
            # Validate Status ---------------------------------------- Finish

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
            cash_deposit = CashDeposits.query.filter_by(
                id=deposit_id,
                workshop_id=workshop_id,
                is_deleted=0
            ).first()

            if not cash_deposit:
                return not_found(
                    "Cash deposit could not be found."
                )

            if cash_deposit.status != 0:
                return defined_error(
                    "Cash deposit has already been verified.",
                    "Defined Error",
                    499
                )
            # Check Cash Deposit ---------------------------------------- Finish

            # Update Data ---------------------------------------- Start
            timestamp = current_timestamp()

            cash_deposit.status = status
            cash_deposit.verified_by = user_id
            cash_deposit.verified_at = timestamp
            cash_deposit.updated_at = timestamp

            try:
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                return parameter_error(str(e))
            # Update Data ---------------------------------------- Finish

            return success(
                status_code=200
            )

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # VERIFY CASH DEPOSIT ============================================================ End

    # DELETE CASH DEPOSIT ============================================================ Begin
    def delete_cash_deposit(user_role, workshop_id, id):
        try:
            # Access Validation ---------------------------------------- Start
            access = role_validator(user_role)

            if not access:
                return authorization_error()
            
            subscription_access = subscription_validator(user_role, workshop_id)

            if not subscription_access:
                return subscription_required()
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
           
            # Check Verification Status ---------------------------------------- Start
            if data.status != 0:
                return defined_error(
                    "Setor kas yang sudah diverifikasi tidak dapat dihapus.",
                    "Defined Error",
                    499
                )
            # Check Verification Status ---------------------------------------- Finish
            
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