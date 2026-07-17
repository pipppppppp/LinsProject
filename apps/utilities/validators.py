from datetime import datetime, timedelta

import json

from apps.database.db_categories import Categories
from apps.database.db_users import Users
from apps.database.db_workshops import Workshops
from apps.database.db_customers import Customers
from apps.database.db_vehicles import Vehicles
from apps.utilities.utilities import *


##########################################################################################################
# VALIDATION

# AUTH VALIDATION ============================================================ Begin
def signup_validator(username, email, password, repassword, workshop_name, workshop_address, workshop_phone):
    checker_result = []

    # Check Null Value ---------------------------------------- Start
    if username == "":
        checker_result.append(f"Nama tidak boleh kosong")
    if email == "":
        checker_result.append(f"Email tidak boleh kosong")
    if password == "":
        checker_result.append(f"Password tidak boleh kosong")
    if repassword == "":
        checker_result.append(f"Password tidak boleh kosong")
    if workshop_name == "":
          checker_result.append("Nama bengkel tidak boleh kosong")
    if workshop_address == "":
        checker_result.append("Alamat bengkel tidak boleh kosong")
    if workshop_phone == "":
        checker_result.append("Nomor HP bengkel tidak boleh kosong")
    # Check Null Value ---------------------------------------- Finish

    # Sanitize String Content ---------------------------------------- Start
    sanitizeName, charName = sanitize_all_char(username)
    if sanitizeName:
        checker_result.append(f"Nama tidak boleh mengandung karakter {charName}")
    sanitizeEmail, charEmail = sanitize_email_char(email)
    if sanitizeEmail:
        checker_result.append(f"Email tidak boleh mengandung karakter {charEmail}")
    sanitizePass, charPass = sanitize_passwd_char(password)
    if sanitizePass:
        checker_result.append(f"Password tidak boleh mengandung karakter {charPass}")
    sanitizeRepass, charRepass = sanitize_passwd_char(repassword)
    if sanitizeRepass:
        checker_result.append(f"Password tidak boleh mengandung karakter {charRepass}")
    sanitizeWorkshop, charWorkshop = sanitize_all_char(workshop_name)
    if sanitizeWorkshop:
        checker_result.append(f"Nama bengkel tidak boleh mengandung karakter {charWorkshop}")
    if phone_checker(workshop_phone):
        checker_result.append("Nomor HP tidak valid.")
    # Sanitize String Content ---------------------------------------- Finish


    if password != repassword:
        checker_result.append(f"Password tidak sama.")
    

    if email_checker(email):
        checker_result.append(f"Email tidak valid.")
    passwordCheck, message = password_checker(password)
    if passwordCheck:
        checker_result.append(message)


    datas = Users.query.filter_by(email=email, is_delete=0).first()
    if datas:
        checker_result.append(f"Email sudah terdaftar sebagai owner.")

    return checker_result 

def role_validator(role):
    access = False

    if int(role) <= 1:
        access = True

    return access

def signin_validator(usermail, password):
    checker_result = []

    # Check Null Value ---------------------------------------- Start
    if usermail == "":
        checker_result.append("Username atau email tidak boleh kosong.")
    if password == "":
        checker_result.append("Password tidak boleh kosong.")
    # Check Null Value ---------------------------------------- Finish

    # Sanitize String Content ---------------------------------------- Start
    sanitMail, charMail = sanitize_email_char(usermail)
    if sanitMail:
        checker_result.append(f"Email tidak boleh mengandung karakter {charMail}.")
    sanitPass, charPass = sanitize_passwd_char(password)
    if sanitPass:
        checker_result.append(f"Password tidak boleh mengandung karakter {charPass}.")
    # Sanitize String Content ---------------------------------------- Finish
    
    # Check Data in Database ---------------------------------------- Finish
    # Get data
    result_data = Users.query.filter_by(email=usermail, is_delete=0).first()
    if not result_data:
        result_data = Users.query.filter_by(username=usermail, is_delete=0).first()
    
    # Check data ready or not
    stts = 200
    if not result_data:
        stts = 404
        checker_result.append("Username/Email tidak terdaftar.")
    # Check Data in Database ---------------------------------------- Finish

    # Password Validation ---------------------------------------- Start
    # Check password
    if result_data:
        # Check activated
        if result_data.is_active == 0:
            stts = 400
            checker_result.append("Akun Anda belum diverifikasi Administrator.")
            return checker_result, result_data, stts
        
        # Cek password
        password_match = password_compare(result_data.password, password)
        if not password_match:
            stts = 400
            checker_result.append("Password salah.")
    # Password Validation ---------------------------------------- Finish

    # Get photo profile
    
    return checker_result, result_data, stts

# def vld_auth(email):
    checkResult = []
    
    if email_checker(email):
        checkResult.append(f"Email tidak valid.")

    token = auth_token()

    return checkResult, token
# AUTH VALIDATION ============================================================ End

# WORKSHOP VALIDATION ============================================================ Begin
def workshop_validator(user_id, name, address, phone, is_create=True):
    checker_result = []

    # Check Null Value ---------------------------------------- Start
    if name == "":
        checker_result.append("Nama bengkel tidak boleh kosong.")
    if address == "":
        checker_result.append("Alamat bengkel tidak boleh kosong.")
    if phone == "":
        checker_result.append("No telepon bengkel tidak boleh kosong.")
    # Check Null Value ---------------------------------------- Finish

    # Sanitize String Content ---------------------------------------- Start
    sanitize_wsname, char_wsname = sanitize_all_char(name)
    if sanitize_wsname:
        checker_result.append(f"Nama bengkel tidak boleh mengandung karakter {char_wsname}")
    sanitize_wsphone, char_wsphone = sanitize_phone_char(phone)
    if sanitize_wsphone:
        checker_result.append(f"No telepon tidak boleh mengandung karakter {char_wsphone}")
    # Sanitize String Content ---------------------------------------- Finish

    # Check Field Content ---------------------------------------- Start
    if phone_checker(phone):
        checker_result.append(f"No telepon tidak valid.")
    # Check Field Content ---------------------------------------- Finish

    # Check Duplicated Data ---------------------------------------- Start
    if is_create:
        result = Workshops.query.filter_by(workshop_name=name, owner_id=user_id, is_delete=0).first()
        if result:
            checker_result.append("Bengkel sudah terdaftar")
    # Check Duplicated Data ---------------------------------------- Finish

    return checker_result
# WORKSHOP VALIDATION ============================================================ End

# CATEGORY VALIDATION ============================================================ Begin
def category_validator(category, workshop_id):
    check_result = []

    # Check Null Value ---------------------------------------- Start
    if category == "":
        check_result.append("Kategori tidak boleh kosong.")
    # Check Null Value ---------------------------------------- Finish

    # Sanitize Category ---------------------------------------- Start
    sanitize_category, char_category = sanitize_all_char(category)
    if sanitize_category:
        check_result.append(f"Kategori tidak boleh mengandung karakter {char_category}")
    # Sanitize Category ---------------------------------------- Finish
    
    # Check String Value ---------------------------------------- Start
    if string_checker(category):
        check_result.append("Kategori tidak valid")
    # Check String Value ---------------------------------------- Finish

    # Check Duplicate Category ---------------------------------------- Start
    result = Categories.query.filter_by(category=category, workshop_id=workshop_id, is_delete=0).first()
    if result:
        check_result.append("Kategori sudah terdaftar")
    # Check Duplicate Category ---------------------------------------- Finish

    return check_result
# CATEGORY VALIDATION ============================================================ End

# CUSTOMER VALIDATION ============================================================ Begin
class CustomerValidator:
          
    def validate(self, datas, workshop_id, is_create=True):
      
        customer_name = datas["customer_name"]
        customer_address = datas["customer_address"]
        customer_phone = datas["customer_phone"]

        check_result = []

        # Check Null Value ---------------------------------------- Start
        if customer_name == "":
                check_result.append("Nama tidak boleh kosong.")
        if customer_address == "":
                check_result.append("Alamat tidak boleh kosong.")
        if customer_phone == "":
                check_result.append("No telepon tidak boleh kosong.")
        # Check Null Value ---------------------------------------- Finish

        # Sanitize String Content ---------------------------------------- Start
        sanitize_wsname, char_wsname = sanitize_all_char(customer_name)
        if sanitize_wsname:
                check_result.append(f"Nama tidak boleh mengandung karakter {char_wsname}")
        sanitize_wsphone, char_wsphone = sanitize_phone_char(customer_phone)
        if sanitize_wsphone:
                check_result.append(f"No telepon tidak boleh mengandung karakter {char_wsphone}")
        # Sanitize String Content ---------------------------------------- Finish

        # Check Field Content ---------------------------------------- Start
        if string_checker(customer_name):
                check_result.append("Nama pelanggan tidak valid.")
        if phone_checker(customer_phone):
                check_result.append(f"No telepon tidak valid.")
        # Check Field Content ---------------------------------------- Finish

        # Check Duplicate Customer ---------------------------------------- Start
        if is_create:
                result = Customers.query.filter_by(
                    workshop_id=workshop_id,
                    customer_name=customer_name,
                    is_delete=0
                    ).first()
                if result:
                    check_result.append("Nama sudah terdaftar")
        # Check Duplicate Customer ---------------------------------------- Finish
        return check_result
# CUSTOMER VALIDATION ============================================================ End

# VEHICLE VALIDATION ============================================================ Begin
class VehicleValidator:
          
    def validate(self, datas, workshop_id, is_create=True):
      
        plate_number = datas["plate_number"]
        vehicle_brand = datas["vehicle_brand"]
        vehicle_type = datas["vehicle_type"]
        vehicle_year = datas["vehicle_year"]
        vehicle_color = datas["vehicle_color"]
        customer_id = datas["customer_id"]

        check_result = []

        # Check Null Value ---------------------------------------- Start
        if plate_number == "":
                check_result.append("Plat nomor kendaraan tidak boleh kosong.")
        if vehicle_brand == "":
                check_result.append("Merek kendaraan tidak boleh kosong.")
        if vehicle_type == "":
                check_result.append("Tipe kendaraan tidak boleh kosong.")
        if vehicle_year == "":
                check_result.append("Tahun kendaraan tidak boleh kosong.")
        if vehicle_color == "":
                check_result.append("Warna kendaraan tidak boleh kosong.")
        # Check Null Value ---------------------------------------- Finish

        # Sanitize String Content ---------------------------------------- Start
        sanitize_plate, char_plate = sanitize_plate_char(plate_number)
        if sanitize_plate:
                check_result.append(f"Plat nomor tidak boleh mengandung karakter {char_plate}")
        sanitize_brand, char_brand = sanitize_all_char(vehicle_brand)
        if sanitize_brand:
                check_result.append(f"Merk kendaraan tidak boleh mengandung karakter {char_brand}")
        sanitize_type, char_type = sanitize_all_char(vehicle_type)
        if sanitize_type:
                check_result.append(f"Tipe kendaraan tidak boleh mengandung karakter {char_type}")
        sanitize_color, char_color = sanitize_all_char(vehicle_color)
        if sanitize_color:
                check_result.append(f"Warna kendaraan tidak boleh mengandung karakter {char_color}")
        # Sanitize String Content ---------------------------------------- Finish

        # Check Field Content ---------------------------------------- Start
        if plate_checker(plate_number):
                check_result.append("Plat nomor tidak valid.")

        if string_checker(vehicle_brand):
                check_result.append("Merk kendaraan tidak valid.")

        if string_checker(vehicle_type):
                check_result.append("Tipe kendaraan tidak valid.")

        if vehicle_color != "" and string_checker(vehicle_color):
                check_result.append("Warna kendaraan tidak valid.")

        if vehicle_year != "":
                if not str(vehicle_year).isdigit():
                    check_result.append("Tahun kendaraan harus berupa angka.")
                else:
                    year = int(vehicle_year)

                    if year < 1980 or year > datetime.now().year:
                            check_result.append("Tahun kendaraan tidak valid.")

        # Check Field Content ---------------------------------------- Finish

        # Check Duplicate Vehicle ---------------------------------------- Start
        if is_create:
                result = Vehicles.query.filter_by(
                    workshop_id=workshop_id,
                    plate_number=plate_number.strip().upper(),
                    is_delete=0
                ).first()

                if result:
                    check_result.append("Plat nomor sudah terdaftar.")
        # Check Duplicate Customer ---------------------------------------- Finish
        return check_result
# VEHICLE VALIDATION ============================================================ End
