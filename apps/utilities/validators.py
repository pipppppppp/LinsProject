from datetime import datetime, timedelta

import json

from apps import db
from apps.database.db_categories import Categories
from apps.database.db_users import Users
from apps.database.db_workshops import Workshops
from apps.database.db_customers import Customers
from apps.database.db_vehicles import Vehicles
from apps.database.db_products import Products
from apps.database.db_suppliers import Suppliers
from apps.database.db_services import Services
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

    if int(role) in [0, 1, 2]:
        access = True

    return access
    
# ADMINISTRATOR VALIDATION ============================================================ Begin
def administrator_validator(role):
    access = False

    if int(role) == 0:
        access = True

    return access
# ADMINISTRATOR VALIDATION ============================================================ End

# OWNER VALIDATION ============================================================ Begin
def owner_validator(role):
    access = False

    if int(role) == 1:
        access = True

    return access
# OWNER VALIDATION ============================================================ End

# CASHIER VALIDATION ============================================================ Begin
def cashier_validator(role):
    access = False

    if int(role) == 2:
        access = True

    return access
# CASHIER VALIDATION ============================================================ End

# SUBSCRIPTION VALIDATION ============================================================ Begin
def subscription_validator(role, workshop_id):
    try:
        # Administrator tidak membutuhkan subscription
        if int(role) == 0:
            return True

        # Workshop ID Validation ---------------------------------------- Start
        if (
            workshop_id is None or
            str(workshop_id).strip() == "" or
            not str(workshop_id).isdigit()
        ):
            return False
        # Workshop ID Validation ---------------------------------------- Finish

        # Check Workshop ---------------------------------------- Start
        workshop = Workshops.query.filter_by(
            id=workshop_id,
            is_delete=0
        ).first()

        if not workshop:
            return False
        # Check Workshop ---------------------------------------- Finish
        
        # Workshop Active Validation ---------------------------------------- Start
        if int(workshop.is_active or 0) != 1:
            return False
        # Workshop Active Validation ---------------------------------------- Finish
        
        # Initialize Subscription ---------------------------------------- Start
        timestamp = current_timestamp()

        subscription_status = int(
            workshop.subscription_status or 0
        )

        subscription_end = int(
            workshop.subscription_end or 0
        )
        # Initialize Subscription ---------------------------------------- Finish

        # Active Subscription ---------------------------------------- Start
        if (
            subscription_status == 1 and
            subscription_end > timestamp
        ):
            return True
        # Active Subscription ---------------------------------------- Finish

        # Expired Subscription ---------------------------------------- Start
        if (
            subscription_status == 1 and
            subscription_end > 0 and
            subscription_end <= timestamp
        ):
            workshop.subscription_status = 2
            workshop.updated_at = timestamp

            try:
                db.session.commit()

            except Exception:
                db.session.rollback()

            return False
        # Expired Subscription ---------------------------------------- Finish

        return False

    except Exception:
        db.session.rollback()
        return False
# SUBSCRIPTION VALIDATION ============================================================ End

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

# EXCEL FILE VALIDATION ============================================================ Begin
def excel_file_validator(file):
    check_result = []

    # Check Null Value ---------------------------------------- Start
    if file is None:
        check_result.append("File is required.")
        return check_result
    # Check Null Value ---------------------------------------- Finish

    # Check File Name ---------------------------------------- Start
    if file.filename == "":
        check_result.append("File name cannot be empty.")
        return check_result
    # Check File Name ---------------------------------------- Finish

    # Check File Extension ---------------------------------------- Start
    extension = file.filename.rsplit(".", 1)[-1].lower()

    if extension != "xlsx":
        check_result.append(
            "Only .xlsx files are allowed."
        )
    # Check File Extension ---------------------------------------- Finish

    return check_result
# EXCEL FILE VALIDATION ============================================================ End

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

# SUPPLIER VALIDATION ============================================================ Begin
def supplier_validator(
    name,
    phone,
    address,
    workshop_id,
    supplier_id=None
):
    check_result = []

    # Check Null Value ---------------------------------------- Start
    if name == "":
        check_result.append("Nama supplier tidak boleh kosong.")

    if phone == "":
        check_result.append("No telepon tidak boleh kosong.")

    if address == "":
        check_result.append("Alamat supplier tidak boleh kosong.")
    # Check Null Value ---------------------------------------- Finish

    # Sanitize String Content ---------------------------------------- Start
    sanitize_name, char_name = sanitize_all_char(name)
    if sanitize_name:
        check_result.append(
            f"Nama supplier tidak boleh mengandung karakter {char_name}"
        )

    sanitize_phone, char_phone = sanitize_phone_char(phone)
    if sanitize_phone:
        check_result.append(
            f"No telepon tidak boleh mengandung karakter {char_phone}"
        )
    # Sanitize String Content ---------------------------------------- Finish

    # Check Field Content ---------------------------------------- Start
    if string_checker(name):
        check_result.append("Nama supplier tidak valid.")

    if phone_checker(phone):
        check_result.append("No telepon tidak valid.")
    # Check Field Content ---------------------------------------- Finish

    # Check Duplicate Supplier ---------------------------------------- Start
    query = Suppliers.query.filter(
        Suppliers.workshop_id == workshop_id,
        Suppliers.name == name.strip(),
        Suppliers.is_delete == 0
    )

    if supplier_id is not None:
        query = query.filter(
            Suppliers.id != supplier_id
        )

    result = query.first()

    if result:
        check_result.append("Nama supplier sudah terdaftar.")
    # Check Duplicate Supplier ---------------------------------------- Finish

    return check_result
# SUPPLIER VALIDATION ============================================================ End

# SERVICE VALIDATION ============================================================ Begin
def service_validator(
    name,
    service_fee,
    description,
    workshop_id,
    service_id=None
):
    check_result = []

    # Check Null Value ---------------------------------------- Start
    if name == "":
        check_result.append("Nama jasa tidak boleh kosong.")

    if service_fee == "":
        check_result.append("Biaya jasa tidak boleh kosong.")
    # Check Null Value ---------------------------------------- Finish

    # Sanitize String Content ---------------------------------------- Start
    sanitize_name, char_name = sanitize_title_char(name)
    if sanitize_name:
        check_result.append(
            f"Nama jasa tidak boleh mengandung karakter {char_name}"
        )
    # Sanitize String Content ---------------------------------------- Finish

    # Check Field Content ---------------------------------------- Start
    if string_checker(name):
        check_result.append("Nama jasa tidak valid.")

    if not str(service_fee).isdigit():
        check_result.append("Biaya jasa harus berupa angka.")

    if str(service_fee).isdigit():
        if int(service_fee) < 0:
            check_result.append("Biaya jasa tidak boleh kurang dari 0.")
    # Check Field Content ---------------------------------------- Finish

    # Check Duplicate Service ---------------------------------------- Start
    query = Services.query.filter(
        Services.workshop_id == workshop_id,
        Services.name == name.strip(),
        Services.is_delete == 0
    )

    if service_id is not None:
        query = query.filter(
            Services.id != service_id
        )

    result = query.first()

    if result:
        check_result.append("Nama jasa sudah terdaftar.")
    # Check Duplicate Service ---------------------------------------- Finish

    return check_result
# SERVICE VALIDATION ============================================================ End

# USER VALIDATION ============================================================ Begin
def user_validator(
    owner_name,
    username,
    email,
    password,
    role,
    workshop_id,
    user_id=None,
    is_update=False
):
    check_result = []

    # Check Null Value ---------------------------------------- Start
    if owner_name == "":
        check_result.append("Nama tidak boleh kosong.")

    if username == "":
        check_result.append("Username tidak boleh kosong.")

    if email == "":
        check_result.append("Email tidak boleh kosong.")

    if not is_update and password == "":
        check_result.append("Password tidak boleh kosong.")

    if role == "":
        check_result.append("Role tidak boleh kosong.")
    # Check Null Value ---------------------------------------- Finish

    # Sanitize String Content ---------------------------------------- Start
    sanitize_name, char_name = sanitize_all_char(owner_name)
    if sanitize_name:
        check_result.append(
            f"Nama tidak boleh mengandung karakter {char_name}"
        )

    sanitize_username, char_username = sanitize_all_char(username)
    if sanitize_username:
        check_result.append(
            f"Username tidak boleh mengandung karakter {char_username}"
        )

    sanitize_email, char_email = sanitize_email_char(email)
    if sanitize_email:
        check_result.append(
            f"Email tidak boleh mengandung karakter {char_email}"
        )

    if password != "":
        sanitize_password, char_password = sanitize_passwd_char(password)
        if sanitize_password:
            check_result.append(
                f"Password tidak boleh mengandung karakter {char_password}"
            )
    # Sanitize String Content ---------------------------------------- Finish

    # Check Field Content ---------------------------------------- Start
    if string_checker(owner_name):
        check_result.append("Nama tidak valid.")

    if string_checker(username):
        check_result.append("Username tidak valid.")

    if email_checker(email):
        check_result.append("Email tidak valid.")

    if password != "":
        password_check, message = password_checker(password)

        if password_check:
            check_result.append(message)

    if str(role) not in ["0", "1", "2"]:
        check_result.append("Role tidak valid.")
    # Check Field Content ---------------------------------------- Finish

    # Check Duplicate Username ---------------------------------------- Start
    username_query = Users.query.filter(
        Users.username == username.strip(),
        Users.is_delete == 0
    )

    if user_id is not None:
        username_query = username_query.filter(
            Users.id != user_id
        )

    username_result = username_query.first()

    if username_result:
        check_result.append("Username sudah digunakan.")
    # Check Duplicate Username ---------------------------------------- Finish

    # Check Duplicate Email ---------------------------------------- Start
    email_query = Users.query.filter(
        Users.email == email.strip(),
        Users.is_delete == 0
    )

    if user_id is not None:
        email_query = email_query.filter(
            Users.id != user_id
        )

    email_result = email_query.first()

    if email_result:
        check_result.append("Email sudah digunakan.")
    # Check Duplicate Email ---------------------------------------- Finish

    return check_result
# USER VALIDATION ============================================================ End

# PURCHASE VALIDATION ============================================================ Begin
def purchase_validator(
    supplier_id,
    purchase_date,
    purchase_details,
    workshop_id,
    purchase_id=None
):
    check_result = []

    # Check Null Value ---------------------------------------- Start
    if supplier_id == "":
        check_result.append("Supplier tidak boleh kosong.")

    if purchase_date == "":
        check_result.append("Tanggal pembelian tidak boleh kosong.")

    if (
        purchase_details is None or
        not isinstance(purchase_details, list) or
        len(purchase_details) == 0
    ):
        check_result.append("Detail pembelian tidak boleh kosong.")
    # Check Null Value ---------------------------------------- Finish

    # Check Field Content ---------------------------------------- Start
    if supplier_id != "" and not str(supplier_id).isdigit():
        check_result.append("Supplier tidak valid.")

    if purchase_date != "" and not str(purchase_date).isdigit():
        check_result.append("Tanggal pembelian tidak valid.")
    # Check Field Content ---------------------------------------- Finish

    # Check Supplier ---------------------------------------- Start
    if str(supplier_id).isdigit():
        supplier = Suppliers.query.filter_by(
            id=supplier_id,
            workshop_id=workshop_id,
            is_delete=0
        ).first()

        if not supplier:
            check_result.append("Supplier tidak ditemukan.")
    # Check Supplier ---------------------------------------- Finish

    # Check Purchase Detail ---------------------------------------- Start
    if isinstance(purchase_details, list):

        for index, item in enumerate(purchase_details):

            product_id = item.get("product_id", "")
            quantity = item.get("quantity", "")
            unit_cost = item.get("unit_cost", "")

            if product_id == "":
                check_result.append(
                    f"Produk pada item ke-{index + 1} tidak boleh kosong."
                )
                continue

            if not str(product_id).isdigit():
                check_result.append(
                    f"Produk pada item ke-{index + 1} tidak valid."
                )
                continue

            product = Products.query.filter_by(
                id=product_id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not product:
                check_result.append(
                    f"Produk pada item ke-{index + 1} tidak ditemukan."
                )
                continue

            if quantity == "":
                check_result.append(
                    f"Jumlah pada item ke-{index + 1} tidak boleh kosong."
                )

            elif not str(quantity).isdigit():
                check_result.append(
                    f"Jumlah pada item ke-{index + 1} harus berupa angka."
                )

            elif int(quantity) <= 0:
                check_result.append(
                    f"Jumlah pada item ke-{index + 1} harus lebih dari 0."
                )

            if unit_cost == "":
                check_result.append(
                    f"Harga beli pada item ke-{index + 1} tidak boleh kosong."
                )

            elif not str(unit_cost).isdigit():
                check_result.append(
                    f"Harga beli pada item ke-{index + 1} harus berupa angka."
                )

            elif int(unit_cost) < 0:
                check_result.append(
                    f"Harga beli pada item ke-{index + 1} tidak boleh kurang dari 0."
                )
    # Check Purchase Detail ---------------------------------------- Finish

    return check_result
# PURCHASE VALIDATION ============================================================ End

# PURCHASE EXCEL VALIDATION ============================================================ Begin
def purchase_excel_validator(worksheet):
    check_result = []

    # Check Empty File ---------------------------------------- Start
    if worksheet.max_row <= 1:
        check_result.append(
            "The uploaded Excel file is empty."
        )

        return check_result
    # Check Empty File ---------------------------------------- Finish

    # Check Header ---------------------------------------- Start
    english = ["Product", "Quantity", "Unit Cost"]
    indonesia = ["Nama Barang", "Jumlah", "Harga Beli"]

    headers = [
        str(worksheet.cell(row=1, column=index).value).strip()
        for index in range(1, 4)
    ]

    if headers != english and headers != indonesia:
        check_result.append("Invalid Excel template.")

        return check_result
    # Check Header ---------------------------------------- Finish

    # Check Rows ---------------------------------------- Start
    for row in range(2, worksheet.max_row + 1):

        product = worksheet.cell(row=row, column=1).value
        quantity = worksheet.cell(row=row, column=2).value
        unit_cost = worksheet.cell(row=row, column=3).value

        if not product:
            check_result.append(
                f"Row {row}: Product is required."
            )

        if quantity in [None, ""]:
            check_result.append(
                f"Row {row}: Quantity is required."
            )

        elif not isinstance(quantity, (int, float)):
            check_result.append(
                f"Row {row}: Quantity must be numeric."
            )

        elif quantity <= 0:
            check_result.append(
                f"Row {row}: Quantity must be greater than 0."
            )

        if unit_cost in [None, ""]:
            check_result.append(
                f"Row {row}: Unit cost is required."
            )

        elif not isinstance(unit_cost, (int, float)):
            check_result.append(
                f"Row {row}: Unit cost must be numeric."
            )

        elif unit_cost < 0:
            check_result.append(
                f"Row {row}: Unit cost cannot be less than 0."
            )
    # Check Rows ---------------------------------------- Finish

    return check_result
# PURCHASE EXCEL VALIDATION ============================================================ End

# REPORT VALIDATION ============================================================ Begin
def history_validator(
    start_date,
    end_date,
    workshop_id,
    cashier_id=None,
    customer_id=None,
    supplier_id=""
):
    check_result = []

    # Check Null Value ---------------------------------------- Start
    if start_date == "":
        check_result.append("Tanggal awal tidak boleh kosong.")

    if end_date == "":
        check_result.append("Tanggal akhir tidak boleh kosong.")
    # Check Null Value ---------------------------------------- Finish

    # Check Field Content ---------------------------------------- Start
    if start_date != "" and not str(start_date).isdigit():
        check_result.append("Tanggal awal tidak valid.")

    if end_date != "" and not str(end_date).isdigit():
        check_result.append("Tanggal akhir tidak valid.")

    if (
        str(start_date).isdigit() and
        str(end_date).isdigit()
    ):
        if int(start_date) > int(end_date):
            check_result.append(
                "Tanggal awal tidak boleh melebihi tanggal akhir."
            )

    if (
        cashier_id is not None and
        cashier_id != ""
    ):
        if not str(cashier_id).isdigit():
            check_result.append("Kasir tidak valid.")

    if (
        customer_id is not None and
        customer_id != ""
    ):
        if not str(customer_id).isdigit():
            check_result.append("Pelanggan tidak valid.")
    # Check Field Content ---------------------------------------- Finish

    # Check Cashier ---------------------------------------- Start
    if (
        cashier_id is not None and
        cashier_id != "" and
        str(cashier_id).isdigit()
    ):
        cashier = Users.query.filter_by(
            id=cashier_id,
            workshop_id=workshop_id,
            role=2,
            is_delete=0
        ).first()

        if not cashier:
            check_result.append("Kasir tidak ditemukan.")
    # Check Cashier ---------------------------------------- Finish

    # Check Customer ---------------------------------------- Start
    if (
        customer_id is not None and
        customer_id != "" and
        str(customer_id).isdigit()
    ):
        customer = Customers.query.filter_by(
            id=customer_id,
            workshop_id=workshop_id,
            is_delete=0
        ).first()

        if not customer:
            check_result.append("Pelanggan tidak ditemukan.")
    # Check Customer ---------------------------------------- Finish

    return check_result
# REPORT VALIDATION ============================================================ End

# SALE VALIDATION ============================================================ Begin
def sale_validator(customer_id,vehicle_id,payment,product_details,service_details,workshop_id):
    check_result = []

    # Check Null Value ---------------------------------------- Start
    if payment == "":
        check_result.append("Nominal pembayaran tidak boleh kosong.")

    if (
        (product_details is None or len(product_details) == 0) and
        (service_details is None or len(service_details) == 0)
    ):
        check_result.append(
            "Minimal harus ada barang atau jasa."
        )
    # Check Null Value ---------------------------------------- Finish

    # Check Field Content ---------------------------------------- Start
    if payment != "" and not str(payment).isdigit():
        check_result.append("Nominal pembayaran harus berupa angka.")
    # Check Field Content ---------------------------------------- Finish

    # Check Customer ---------------------------------------- Start
    if customer_id not in ["", None]:

        if not str(customer_id).isdigit():
            check_result.append("Pelanggan tidak valid.")

        else:
            customer = Customers.query.filter_by(
                id=customer_id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not customer:
                check_result.append("Pelanggan tidak ditemukan.")
    # Check Customer ---------------------------------------- Finish

    # Check Vehicle ---------------------------------------- Start
    if vehicle_id not in ["", None]:

        if not str(vehicle_id).isdigit():
            check_result.append("Kendaraan tidak valid.")

        else:
            query = Vehicles.query.filter_by(
                id=vehicle_id,
                workshop_id=workshop_id,
                is_delete=0
            )

            if customer_id not in ["", None]:
                query = query.filter_by(
                    customer_id=customer_id
                )

            vehicle = query.first()

            if not vehicle:
                check_result.append("Kendaraan tidak ditemukan.")
    # Check Vehicle ---------------------------------------- Finish

    # Check Product Detail ---------------------------------------- Start
    if isinstance(product_details, list):

        for index, item in enumerate(product_details):

            product_id = item.get("product_id", "")
            quantity = item.get("quantity", "")

            if product_id == "":
                check_result.append(
                    f"Produk pada item ke-{index+1} tidak boleh kosong."
                )
                continue

            if not str(product_id).isdigit():
                check_result.append(
                    f"Produk pada item ke-{index+1} tidak valid."
                )
                continue

            product = Products.query.filter_by(
                id=product_id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not product:
                check_result.append(
                    f"Produk pada item ke-{index+1} tidak ditemukan."
                )
                continue

            if quantity == "":
                check_result.append(
                    f"Jumlah produk pada item ke-{index+1} tidak boleh kosong."
                )

            elif not str(quantity).isdigit():
                check_result.append(
                    f"Jumlah produk pada item ke-{index+1} harus berupa angka."
                )

            elif int(quantity) <= 0:
                check_result.append(
                    f"Jumlah produk pada item ke-{index+1} harus lebih dari 0."
                )

            elif int(quantity) > product.stock:
                check_result.append(
                    f"Stok {product.product_name} tidak mencukupi."
                )
    # Check Product Detail ---------------------------------------- Finish


    # Check Service Detail ---------------------------------------- Start
    if isinstance(service_details, list):

        for index, item in enumerate(service_details):

            service_id = item.get("service_id", "")
            quantity = item.get("quantity", "")

            if service_id == "":
                check_result.append(
                    f"Jasa pada item ke-{index+1} tidak boleh kosong."
                )
                continue

            if not str(service_id).isdigit():
                check_result.append(
                    f"Jasa pada item ke-{index+1} tidak valid."
                )
                continue

            service = Services.query.filter_by(
                id=service_id,
                workshop_id=workshop_id,
                is_delete=0
            ).first()

            if not service:
                check_result.append(
                    f"Jasa pada item ke-{index+1} tidak ditemukan."
                )
                continue

            if quantity == "":
                check_result.append(
                    f"Jumlah jasa pada item ke-{index+1} tidak boleh kosong."
                )

            elif not str(quantity).isdigit():
                check_result.append(
                    f"Jumlah jasa pada item ke-{index+1} harus berupa angka."
                )

            elif int(quantity) <= 0:
                check_result.append(
                    f"Jumlah jasa pada item ke-{index+1} harus lebih dari 0."
                )
    # Check Service Detail ---------------------------------------- Finish
    return check_result
# SALE VALIDATION ============================================================ End

# CASH DEPOSIT VALIDATION ============================================================ Begin
def cash_deposit_validator(total_deposit, total_sales=None):
    check_result = []

    # Check Null Value
    if str(total_deposit).strip() == "":
        check_result.append("Nominal setor tidak boleh kosong.")

    # Check Number
    elif not str(total_deposit).isdigit():
        check_result.append("Nominal setor harus berupa angka.")

    elif int(total_deposit) <= 0:
        check_result.append("Nominal setor harus lebih dari 0.")

    # Check Maximum Deposit
    elif total_sales is not None and int(total_deposit) > int(total_sales):
        check_result.append(
            "Nominal setor tidak boleh melebihi total penjualan hari ini."
        )
    return check_result
# CASH DEPOSIT VALIDATION ============================================================ End

