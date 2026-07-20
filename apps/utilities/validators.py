from datetime import datetime, timedelta

import json

from apps.database.db_categories import Categories
from apps.database.db_users import Users
from apps.database.db_workshops import Workshops
from apps.database.db_customers import Customers
from apps.database.db_vehicles import Vehicles
from apps.database.db_products import Products
from apps.utilities.utilities import *


##########################################################################################################
# VALIDATION

# AUTH VALIDATION ============================================================ Begin
def signup_validator(owner_name, username, email, password, repassword, workshop_name, workshop_address, workshop_phone):
    checker_result = []

    # Check Null Value ---------------------------------------- Start
    if owner_name == "":
        checker_result.append(f"Nama tidak boleh kosong")
    if username == "":
        checker_result.append(f"Username tidak boleh kosong")
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
    sanitizeName, charName = sanitize_all_char(owner_name)
    if sanitizeName:
        checker_result.append(f"Nama tidak boleh mengandung karakter {charName}")
    sanitizeName, charName = sanitize_all_char(username)
    if sanitizeName:
        checker_result.append(f"Username tidak boleh mengandung karakter {charName}")
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
    
# ADMINISTRATOR VALIDATION ============================================================ Begin
def administrator_validator(role):
    access = False

    if int(role) == 0:
        access = True

    return access
# ADMINISTRATOR VALIDATION ============================================================ End

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
            stts = 403
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
def customer_validator(
    customer_name,
    customer_address,
    customer_phone,
    workshop_id,
    customer_id=None
):
    check_result = []

    # Check Null Value ---------------------------------------- Start
    if customer_name == "":
        check_result.append("Nama pelanggan tidak boleh kosong.")

    if customer_address == "":
        check_result.append("Alamat pelanggan tidak boleh kosong.")

    if customer_phone == "":
        check_result.append("No telepon tidak boleh kosong.")
    # Check Null Value ---------------------------------------- Finish

    # Sanitize String Content ---------------------------------------- Start
    sanitize_name, char_name = sanitize_all_char(customer_name)
    if sanitize_name:
        check_result.append(
            f"Nama pelanggan tidak boleh mengandung karakter {char_name}"
        )

    sanitize_phone, char_phone = sanitize_phone_char(customer_phone)
    if sanitize_phone:
        check_result.append(
            f"No telepon tidak boleh mengandung karakter {char_phone}"
        )
    # Sanitize String Content ---------------------------------------- Finish

    # Check Field Content ---------------------------------------- Start
    if string_checker(customer_name):
        check_result.append("Nama pelanggan tidak valid.")

    if phone_checker(customer_phone):
        check_result.append("No telepon tidak valid.")
    # Check Field Content ---------------------------------------- Finish

    # Check Duplicate Customer ---------------------------------------- Start
    query = Customers.query.filter(
        Customers.workshop_id == workshop_id,
        Customers.customer_name == customer_name.strip(),
        Customers.is_delete == 0
    )

    if customer_id is not None:
        query = query.filter(
            Customers.id != customer_id
        )

    result = query.first()

    if result:
        check_result.append("Nama pelanggan sudah terdaftar.")
    # Check Duplicate Customer ---------------------------------------- Finish

    return check_result
# CUSTOMER VALIDATION ============================================================ End

# VEHICLE VALIDATION ============================================================ Begin
def vehicle_validator(
    customer_id,
    plate_number,
    vehicle_brand,
    vehicle_type,
    vehicle_year,
    vehicle_color,
    workshop_id,
    vehicle_id=None
):
    check_result = []

    # Check Null Value ---------------------------------------- Start
    if customer_id == "":
        check_result.append("Pelanggan tidak boleh kosong.")

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
        check_result.append(
            f"Plat nomor tidak boleh mengandung karakter {char_plate}"
        )

    sanitize_brand, char_brand = sanitize_all_char(vehicle_brand)
    if sanitize_brand:
        check_result.append(
            f"Merek kendaraan tidak boleh mengandung karakter {char_brand}"
        )

    # sanitize_type, char_type = sanitize_all_char(vehicle_type)
    # if sanitize_type:
    #     check_result.append(
    #         f"Tipe kendaraan tidak boleh mengandung karakter {char_type}"
    #     )

    sanitize_color, char_color = sanitize_all_char(vehicle_color)
    if sanitize_color:
        check_result.append(
            f"Warna kendaraan tidak boleh mengandung karakter {char_color}"
        )
    # Sanitize String Content ---------------------------------------- Finish

    # Check Field Content ---------------------------------------- Start
    if not str(customer_id).isdigit():
        check_result.append("Pelanggan tidak valid.")

    if plate_checker(plate_number):
        check_result.append("Plat nomor tidak valid.")

    if string_checker(vehicle_brand):
        check_result.append("Merek kendaraan tidak valid.")

    # if string_checker(vehicle_type):
    #     check_result.append("Tipe kendaraan tidak valid.")

    if string_checker(vehicle_color):
        check_result.append("Warna kendaraan tidak valid.")

    if not str(vehicle_year).isdigit():
        check_result.append("Tahun kendaraan harus berupa angka.")
    else:
        year = int(vehicle_year)

        if year < 1980 or year > datetime.now().year:
            check_result.append("Tahun kendaraan tidak valid.")
    # Check Field Content ---------------------------------------- Finish

    # Check Duplicate Vehicle ---------------------------------------- Start
    query = Vehicles.query.filter(
        Vehicles.workshop_id == workshop_id,
        Vehicles.plate_number == plate_number.strip().upper(),
        Vehicles.is_delete == 0
    )

    if vehicle_id is not None:
        query = query.filter(
            Vehicles.id != vehicle_id
        )

    result = query.first()

    if result:
        check_result.append("Plat nomor sudah terdaftar.")
    # Check Duplicate Vehicle ---------------------------------------- Finish

    return check_result
# VEHICLE VALIDATION ============================================================ End
# PRODUCT VALIDATION ============================================================ Begin
def product_validator(
    category_id,
    product_name,
    stock,
    purchase_price,
    selling_price,
    workshop_id,
    product_id=None
):
    check_result = []

    # Check Null Value ---------------------------------------- Start
    if category_id == "":
        check_result.append("Kategori tidak boleh kosong.")

    if product_name == "":
        check_result.append("Nama produk tidak boleh kosong.")

    if stock == "":
        check_result.append("Stok tidak boleh kosong.")

    if purchase_price == "":
        check_result.append("Harga beli tidak boleh kosong.")

    if selling_price == "":
        check_result.append("Harga jual tidak boleh kosong.")
    # Check Null Value ---------------------------------------- Finish

    # Sanitize String Content ---------------------------------------- Start
    sanitize_product, char_product = sanitize_title_char(product_name)
    if sanitize_product:
        check_result.append(
            f"Nama produk tidak boleh mengandung karakter {char_product}"
        )
    # Sanitize String Content ---------------------------------------- Finish

    # Check Field Content ---------------------------------------- Start
    if not str(category_id).isdigit():
        check_result.append("Kategori tidak valid.")

    if not str(stock).isdigit():
        check_result.append("Stok harus berupa angka.")

    if not str(purchase_price).isdigit():
        check_result.append("Harga beli harus berupa angka.")

    if not str(selling_price).isdigit():
        check_result.append("Harga jual harus berupa angka.")

    if str(stock).isdigit():
        if int(stock) < 0:
            check_result.append("Stok tidak boleh kurang dari 0.")

    if str(purchase_price).isdigit():
        if int(purchase_price) < 0:
            check_result.append("Harga beli tidak boleh kurang dari 0.")

    if str(selling_price).isdigit():
        if int(selling_price) < 0:
            check_result.append("Harga jual tidak boleh kurang dari 0.")

    if (
        str(purchase_price).isdigit() and
        str(selling_price).isdigit()
    ):
        if int(selling_price) < int(purchase_price):
            check_result.append(
                "Harga jual tidak boleh lebih kecil dari harga beli."
            )
    # Check Field Content ---------------------------------------- Finish

    # Check Category ---------------------------------------- Start
    if str(category_id).isdigit():
        result = Categories.query.filter_by(
            id=category_id,
            workshop_id=workshop_id,
            is_delete=0
        ).first()

        if not result:
            check_result.append("Kategori tidak ditemukan.")
    # Check Category ---------------------------------------- Finish

    # Check Duplicate Product ---------------------------------------- Start
    query = Products.query.filter(
        Products.workshop_id == workshop_id,
        Products.product_name == product_name.strip(),
        Products.is_delete == 0
    )

    if product_id is not None:
        query = query.filter(
            Products.id != product_id
        )

    result = query.first()

    if result:
        check_result.append("Nama produk sudah terdaftar.")
    # Check Duplicate Product ---------------------------------------- Finish
    return check_result
# PRODUCT VALIDATION ============================================================ End