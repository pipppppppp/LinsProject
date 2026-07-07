from flask import session

from ... import db
from ...database.db_vehicles import Vehicles
from ...utilities.validators import VehicleValidator
from ...utilities.responseHelper import bad_request

import time


# VEHICLE MODEL CLASS ============================================================ Begin
class VehicleModels():

    # CREATE VEHICLE ============================================================ Begin
    def add_vehicle(datas):
        try:
            # Validation Data ---------------------------------------- Start
            validator = VehicleValidator().validate(datas, session["workshop_id"])
            if validator:
                return {
                    "status": False,
                    "message": validator
                }
            # Validation Data ---------------------------------------- Finish

            # Insert Data ---------------------------------------- Start
            data = Vehicles(
                workshop_id=session["workshop_id"],
                customer_id=datas["customer_id"],
                plate_number=datas["plate_number"],
                vehicle_brand=datas["vehicle_brand"],
                vehicle_type=datas["vehicle_type"],
                vehicle_year=datas["vehicle_year"],
                vehicle_color=datas["vehicle_color"],
                created_at=int(time.time()),
                updated_at=int(time.time())
            )

            db.session.add(data)
            db.session.commit()
            # Insert Data ---------------------------------------- Finish

            return {
                "status": True,
                "message": "Data kendaraan berhasil ditambahkan"
            }

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # CREATE VEHICLE ============================================================ End


    # GET ALL VEHICLE ============================================================ Begin
    def view_vehicle(customer_id):
        try:
            # Get Data ---------------------------------------- Start
            vehicles = Vehicles.query.filter_by(
                workshop_id=session["workshop_id"],
                customer_id=customer_id,
                is_delete=0
            ).all()
            # Get Data ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            response = []

            for rsl in vehicles:
                data = {
                    "vehicle_id": rsl.id,
                    "customer_id": rsl.customer_id,
                    "plate_number": rsl.plate_number,
                    "vehicle_brand": rsl.vehicle_brand,
                    "vehicle_type": rsl.vehicle_type,
                    "vehicle_year": rsl.vehicle_year,
                    "vehicle_color": rsl.vehicle_color,
                }

                response.append(data)

            # Response Data ---------------------------------------- Finish

            return response

        except Exception as e:
            return bad_request(str(e))
    # GET ALL VEHICLE ============================================================ End


    # GET DETAIL VEHICLE ============================================================ Begin
    def detail_vehicle(id):
        try:

            vehicle = Vehicles.query.filter_by(
                id=id,
                workshop_id=session["workshop_id"],
                is_delete=0
            ).first()

            if vehicle is None:
                return {
                    "status": False,
                    "message": "Data kendaraan tidak ditemukan"
                }

            return {
                "vehicle_id": vehicle.id,
                "customer_id": vehicle.customer_id,
                "plate_number": vehicle.plate_number,
                "vehicle_brand": vehicle.vehicle_brand,
                "vehicle_type": vehicle.vehicle_type,
                "vehicle_year": vehicle.vehicle_year,
                "vehicle_color": vehicle.vehicle_color,
            }

        except Exception as e:
            return bad_request(str(e))
    # GET DETAIL VEHICLE ============================================================ End


    # UPDATE VEHICLE ============================================================ Begin
    def edit_vehicle(datas, id):
        try:
            # Validation Data ---------------------------------------- Start
            validator = VehicleValidator().validate(datas, session["workshop_id"], is_create=False)
            if validator:
                return {
                    "status": False,
                    "message": validator
                }
            # Validation Data ---------------------------------------- Finish
            data = Vehicles.query.filter_by(
                id=id,
                workshop_id=session["workshop_id"],
                is_delete=0
            ).first()

            if data is None:
                return {
                    "status": False,
                    "message": "Data kendaraan tidak ditemukan"
                }

            data.customer_id = datas["customer_id"]
            data.plate_number = datas["plate_number"]
            data.vehicle_brand = datas["vehicle_brand"]
            data.vehicle_type = datas["vehicle_type"]
            data.vehicle_year = datas["vehicle_year"]
            data.vehicle_color = datas["vehicle_color"]
            data.updated_at = int(time.time())

            db.session.commit()

            return {
                "status": True,
                "message": "Data kendaraan berhasil diupdate"
            }

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # UPDATE VEHICLE ============================================================ End


    # DELETE VEHICLE ============================================================ Begin
    def delete_vehicle(id):
        try:

            data = Vehicles.query.filter_by(
                id=id,
                workshop_id=session["workshop_id"],
                is_delete=0
            ).first()

            if data is None:
                return {
                    "status": False,
                    "message": "Data kendaraan tidak ditemukan"
                }

            data.is_delete = 1
            data.deleted_at = int(time.time())

            db.session.commit()

            return {
                "status": True,
                "message": "Data kendaraan berhasil dihapus"
            }

        except Exception as e:
            db.session.rollback()
            return bad_request(str(e))
    # DELETE VEHICLE ============================================================ End

# VEHICLE MODEL CLASS ============================================================ End