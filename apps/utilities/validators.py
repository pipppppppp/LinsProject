from datetime import datetime, timedelta

import json

from apps.database.db_categories import Categories
from apps.database.db_users import Users
from apps.database.db_workshops import Workshops
from apps.utilities.utilities import *


##########################################################################################################
# VALIDATION

# AUTH VALIDATION ============================================================ Begin
def signup_validator(username, email, password, repassword):
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
        checker_result.append("Email belum terdaftar.")
    # Check Data in Database ---------------------------------------- Finish

    # Password Validation ---------------------------------------- Start
    # Check password
    if result_data:
        # Check activated
        if result_data.is_active == 0:
            stts = 400
            checker_result.append("Your account has not been activated. Please verify it first.")
            return checker_result, result_data, stts
        
        # Cek password
        passwd_compare = password_comparison(result_data.password, password)
        if not passwd_compare:
            stts = 400
            checker_result.append("Invalid account.")
    # Password Validation ---------------------------------------- Finish

    # Get photo profile
    
    return checker_result, result_data, stts

# def vld_auth(email):
    checkResult = []
    
    if email_checker(email):
        checkResult.append(f"Email tidak valid.")

    token = auth_token()

    return checkResult, token

# def vld_profile(userId, userLevel, fName, mName, lName, phone):
#     checkResult = []
 
#     # Validation For First Name ---------------------------------------- Start
#     if fName == "":
#         # Sanitize String Input ======================================== 
#         sanitFName, charFName = sanitize_all_char(fName)
#         if sanitFName:
#             checkResult.append(f"Nama tidak boleh mengandung karakter {charFName}")

#         # Filter String Input ======================================== 
#         if string_checker(mName):
#             checkResult.append(f"Nama tidak valid.")
#     # Validation For First Name ---------------------------------------- Finish

#     # Validation For Middle Name - If Set ---------------------------------------- Start
#     if mName != "":
#         # Sanitize String Input ======================================== 
#         sanitMName, charMName = sanitize_all_char(mName)
#         if sanitMName:
#             checkResult.append(f"Nama tidak boleh mengandung karakter {charMName}")

#         # Filter String Input ======================================== 
#         if string_checker(mName):
#             checkResult.append(f"Nama tidak valid.")
#     # Validation For Middle Name - If Set ---------------------------------------- Finish
    
#     # Validation For Last Name - If Set ---------------------------------------- Start
#     if lName != "":
#         # Sanitize String Input ======================================== 
#         sanitLName, charLName = sanitize_all_char(lName)
#         if sanitLName:
#             checkResult.append(f"Nama tidak boleh mengandung karakter {charLName}")

#         # Filter String Input ======================================== 
#         if string_checker(lName):
#             checkResult.append(f"Nama tidak valid.")
#     # Validation For Last Name - If Set ---------------------------------------- Finish

#     # Validation For Phone - If Set ---------------------------------------- Start
#     if (phone != "") or (phone != 0):
#         # Sanitize Integer Input ======================================== 
#         sanitPhone, charPhone = sanitize_all_char(phone)
#         if sanitPhone:
#             checkResult.append(f"Phone tidak boleh mengandung karakter {charPhone}")

#         # Filter Integer Input ======================================== 
#         if phone_checker(phone):
#             checkResult.append(f"Phone tidak valid.")
#     # Validation For Phone - If Set ---------------------------------------- Finish

#     # Checking Email on DB ---------------------------------------- Start
#     query = PROF_CHECK_QUERY
#     values = (userId, userLevel, )
#     result = DBHelper().get_data(query, values)
#     if (len(result) == 0) or (result == None):
#         checkResult.append(f"Profile user tidak ditemukan.")
#     # Checking Email on DB ---------------------------------------- Finish

#     # Return Checker ======================================== 
#     return checkResult, result

# def vld_edit_profile(userId, userLevel, fName, mName, lName, phone):
#     checkResult = []

#     # Checking Email on DB ---------------------------------------- Start
#     query = PROF_CHECK_QUERY
#     values = (userId, userLevel, )
#     result = DBHelper().get_data(query, values)
#     if len(result) < 1:
#         checkResult.append(f"Profile user tidak ditemukan.")
#     profile = result[0]
#     # Checking Email on DB ---------------------------------------- Finish
 
#     # Validation For First Name ---------------------------------------- Start
#     if fName != profile['first_name']:
#         # Sanitize String Input ======================================== 
#         sanitFName, charFName = sanitize_all_char(fName)
#         if sanitFName:
#             checkResult.append(f"Nama tidak boleh mengandung karakter {charFName}")

#         # Filter String Input ======================================== 
#         if string_checker(mName):
#             checkResult.append(f"Nama tidak valid.")
#     # Validation For First Name ---------------------------------------- Finish

#     # Validation For Middle Name - If Set ---------------------------------------- Start
#     if mName != profile['middle_name']:
#         # Sanitize String Input ======================================== 
#         sanitMName, charMName = sanitize_all_char(mName)
#         if sanitMName:
#             checkResult.append(f"Nama tidak boleh mengandung karakter {charMName}")

#         # Filter String Input ======================================== 
#         if string_checker(mName):
#             checkResult.append(f"Nama tidak valid.")
#     # Validation For Middle Name - If Set ---------------------------------------- Finish
    
#     # Validation For Last Name - If Set ---------------------------------------- Start
#     if lName != profile['last_name']:
#         # Sanitize String Input ======================================== 
#         sanitLName, charLName = sanitize_all_char(lName)
#         if sanitLName:
#             checkResult.append(f"Nama tidak boleh mengandung karakter {charLName}")

#         # Filter String Input ======================================== 
#         if string_checker(lName):
#             checkResult.append(f"Nama tidak valid.")
#     # Validation For Last Name - If Set ---------------------------------------- Finish

#     # Validation For Phone - If Set ---------------------------------------- Start
#     if phone != profile['phone']:
#         # Sanitize Integer Input ======================================== 
#         sanitPhone, charPhone = sanitize_all_char(phone)
#         if sanitPhone:
#             checkResult.append(f"Phone tidak boleh mengandung karakter {charPhone}")

#         # Filter Integer Input ======================================== 
#         if phone_checker(phone):
#             checkResult.append(f"Phone tidak valid.")
#     # Validation For Phone - If Set ---------------------------------------- Finish

#     # Return Checker ======================================== 
#     return checkResult
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
        checker_result.append(f"No telepon bengkel tidak boleh mengandung karakter {char_wsphone}")
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

# GUEST VALIDATION ============================================================ Begin
def vld_guest(name, address, phone, invCode, is_create=True):
    checkResult = []

    if name == "":
        checkResult.append(f"Nama tidak boleh kosong.")
    if address == "":
        checkResult.append(f"Alamat tidak boleh kosong.")
    if phone == "":
        checkResult.append(f"Nomor handphone tidak boleh kosong.")


    sanitName, charName = sanitize_all_char(name)
    if sanitName:
        checkResult.append(f"Nama tidak boleh mengandung karakter {charName}.")
    sanitPhone, charPhone = sanitize_phone_char(phone)
    if sanitPhone:
        checkResult.append(f"Nomor handphone tidak boleh mengandung karakter {charPhone}.")
        
    
    if string_checker(name):
        checkResult.append(f"Nama tidak valid")
    if phone_checker(phone):
        checkResult.append(f"Nomor handphone tidak valid")
    
    if phone != "":
        if phone[0] == "0":
            phone = "62"+phone[1:]

    if is_create:
        query = GUEST_CHK_QUERY
        values = (invCode, phone, )
        result = DBHelper().get_count_filter_data(query, values)
        if result > 0 :
            checkResult.append(f"Data tamu dengan nomor telepon '{phone}' telah terdaftar.")

    return checkResult, phone
# GUEST VALIDATION ============================================================ End

# GREETING VALIDATION ============================================================ Begin
def vld_greeting(invCode, name, status, greeting):
    checkResult = []

    if name == "":
        checkResult.append("Nama tidak boleh kosong.")
    if status == "":
        checkResult.append("Konfirmasi kehadiran tidak boleh kosong")
    if greeting == "":
        checkResult.append("Pesan tidak boleh kosong.")


    sanitName, charName = sanitize_all_char(name)
    if sanitName:
        checkResult.append(f"Nama tidak boleh mengandung karakter {charName}")
        
    
    if string_checker(name):
        checkResult.append("Nama tidak valid.")
    
    
    query = INV_CHK_CODE_QUERY
    values = (invCode,)
    result = DBHelper().get_data(query, values)
    if len(result) < 1:
        checkResult.append("Data Undangan tidak dapat ditemukan.")

    return checkResult 
# GREETING VALIDATION ============================================================ End

# TEMPLATE VALIDATION ============================================================ Begin
def vld_template(title, thumbnail, css, js, wallpaper1, wallpaper2, category, is_create=True):
    checkResult = []

    if title == "":
        checkResult.append(f"Judul template tidak boleh kosong.")
    if thumbnail == "":
        checkResult.append(f"Thumbnail tidak boleh kosong.")
    if css == "":
        checkResult.append(f"Css tidak boleh kosong.")
    if wallpaper1 == "":
        checkResult.append(f"Wallpaper 1 tidak boleh kosong.")
    if wallpaper2 == "":
        checkResult.append("Wallpaper 2 tidak boleh kosong.")
    if category == "0":
        checkResult.append("Kategori tidak boleh kosong.")
    
    # Sanitize Title ---------------------------------------- Start
    sanitTitle, charTitle = sanitize_title_char(title)
    if sanitTitle:
        checkResult.append(f"Judul tidak boleh mengandung karakter {charTitle}.")
    # Sanitize Title ---------------------------------------- Finish
    
    if is_create:
        query = TMPLT_CHK_QUERY
        values = (title,)
        result = DBHelper().get_count_filter_data(query, values)
        if result != 0:
            checkResult.append("Judul sudah terdaftar.")

        # Photo Check ---------------------------------------- Start
        if thumbnail != "":
            # Memisahkan bagian 'data:' dari base64 string
            header, encoded = thumbnail.split(',', 1)
            # Memisahkan 'data:' dan mengambil MIME type
            mime_type = header.split(':')[1].split(';')[0].split('/')[0]
            if mime_type != "image":
                checkResult.append("File thumbnail yang diinputkan harus berupa gambar.")

        
        if css != "":
            # Memisahkan bagian 'data:' dari base64 string
            header, encoded = css.split(',', 1)
            # Memisahkan 'data:' dan mengambil MIME type
            mime_type = header.split(':')[1].split(';')[0]

            if mime_type != "text/css":
                checkResult.append("File css yang diinputkan harus berupa gambar.")
        
        
        if js != "":
            # Memisahkan bagian 'data:' dari base64 string
            header, encoded = js.split(',', 1)
            # Memisahkan 'data:' dan mengambil MIME type
            mime_type = header.split(':')[1].split(';')[0]
 
            if mime_type != "text/javascript":
                checkResult.append("File javascript yang diinputkan harus berupa gambar.")

        
        if wallpaper1 != "":
            # Memisahkan bagian 'data:' dari base64 string
            header, encoded = wallpaper1.split(',', 1)
            # Memisahkan 'data:' dan mengambil MIME type
            mime_type = header.split(':')[1].split(';')[0].split('/')[0]
            if mime_type != "image":
                checkResult.append("File wallpaper yang diinputkan harus berupa gambar.")

        
        if wallpaper2 != "":
            # Memisahkan bagian 'data:' dari base64 string
            header, encoded = wallpaper2.split(',', 1)
            # Memisahkan 'data:' dan mengambil MIME type
            mime_type = header.split(':')[1].split(';')[0].split('/')[0]
            if mime_type != "image":
                checkResult.append("File wallpaper yang diinputkan harus berupa gambar.")
        # Photo Check ---------------------------------------- Finish
        
    randomNumber = str(random_number(5))

    return checkResult, randomNumber

def vld_request_template(design, deadline, categoryId):
    checkResult = []

    # Input Check ---------------------------------------- Start
    if int(categoryId) == 0:
        checkResult.append("Kategori tidak boleh kosong.")
    if design == "":
        checkResult.append("Desain tidak boleh kosong.")
    if deadline == "":
        checkResult.append("Batas waktu tidak boleh kosong.")
    # Input Check ---------------------------------------- Finish

    # Datetime Check ---------------------------------------- Start
    if deadline != "":
        deadline = datetime.strptime(deadline, "%d %B %Y")
        now = datetime.now()
        oneweek = now + timedelta(days=6)
        if deadline < now:
            checkResult.append("Batas waktu yang diinputkan sudah terlewat.")
        elif deadline < oneweek:
            checkResult.append("Batas waktu minimal 7 hari dari sekarang.")
        deadline = int(round(datetime.timestamp(deadline)*1000))
    # Datetime Check ---------------------------------------- Finish

    # Photo Check ---------------------------------------- Start
    if design != "":
        # Memisahkan bagian 'data:' dari base64 string
        header, encoded = design.split(',', 1)
        # Memisahkan 'data:' dan mengambil MIME type
        mime_type = header.split(':')[1].split(';')[0].split('/')[0]
        if mime_type != "image":
            checkResult.append("Data desain yang diinputkan harus berupa gambar.")
    # Photo Check ---------------------------------------- Finish
    
    return checkResult, deadline
# TEMPLATE VALIDATION ============================================================ End

# INVITATION VALIDATION ============================================================ Begin
def vld_invitation_code():
    invCode = str(random_string_number(6))

    # Check Code ---------------------------------------- Start
    query = INV_CHK_CODE_QUERY
    values = (invCode, )
    result = DBHelper().get_count_filter_data(query, values)
    if result > 0:
        return vld_invitation_code()
    # Check Code ---------------------------------------- Finish

    # Return Value ========================================
    return invCode

def vld_invitation(userId, categoryId, templateId, title, personalData, detailInfo):
    checkResult = []

    # Validation Null Data ---------------------------------------- Start
    if title == "":
        checkResult.append(f"Judul template tidak boleh kosong.")
    if personalData == None:
        checkResult.append(f"Data pribadi tidak boleh kosong tidak boleh kosong.")
    if detailInfo == None:
        checkResult.append(f"Data acara tidak boleh kosong tidak boleh kosong.")
    # Validation Null Data ---------------------------------------- Finish
    
    # Check Data Title & Template ---------------------------------------- Start
    # Template
    query = TMPLT_GET_BY_ID_QUERY
    values = (templateId,)
    ckTemplate = DBHelper().get_count_filter_data(query, values)
    if ckTemplate < 1:
        checkResult.append(f"Data template tidak dapat ditemukan.")
    # Title
    query = INV_CHK_TITLE_QUERY
    values = (title, )
    ckInvit = DBHelper().get_count_filter_data(query, values)
    if ckInvit > 0:
        checkResult.append(f"Judul sudah terpakai.")
    # Check Data Title & Template ---------------------------------------- Finish
    
    # Sanitize Title ---------------------------------------- Start
    sanitTitle, charTitle = sanitize_title_char(title)
    if sanitTitle:
        checkResult.append(f"Judul tidak boleh mengandung karakter {charTitle}.")
    # Sanitize Title ---------------------------------------- Finish
    
    # String Filter ---------------------------------------- Start
    if string_checker(title):
        checkResult.append(f"Judul tidak valid.")
    # String Filter ---------------------------------------- Finish
    
    # Check Data Category ---------------------------------------- Start
    query = CTGR_GET_BY_ID_QUERY
    values = (categoryId,)
    ckCategory = DBHelper().get_data(query, values)
    if len(ckCategory) < 1:
        checkResult.append(f"Data kategori tidak dapat ditemukan.")
    # Check Data Category ---------------------------------------- Finish

    # Check Detail Data ---------------------------------------- Start
    detail = True
    if len(detailInfo) < 1:
        detail = False
        checkResult.append("Info acara tidak boleh kosong.")
    personData = True
    if len(personalData) < 1:
        personData = False
        checkResult.append("Data diri tidak boleh kosong.")
    # Check Detail Data ---------------------------------------- Finish

    # Create Invitation Code ========================================
    invCode = vld_invitation_code()

    # Check By Category ---------------------------------------- Start
    # Wedding
    if ckCategory[0]['category'].upper() == "PERNIKAHAN":
        print("kategori => ", ckCategory[0]['category'].upper())
        # Check Detail Info ---------------------------------------- Start
        if detail:
            marriageDate = detailInfo["marriage_date"]
            marriageStart = detailInfo["marriage_start"]
            marriageEnd = detailInfo["marriage_end"]
            receptionDate = detailInfo["reception_date"]
            receptionStart = detailInfo["reception_start"]
            receptionEnd = detailInfo["reception_end"]
            now = datetime.now()

            # Akad
            if marriageDate != "":
                marriageDate = datetime.strptime(marriageDate, "%d %B %Y")
                marriageStart = datetime.strptime(marriageStart, "%I:%M %p")
                mergeDTS = datetime.combine(datetime.date(marriageDate), datetime.time(marriageStart))
                if mergeDTS <= now:
                    checkResult.append("Tanggal yang diinputkan sudah terlewat.")

                if marriageEnd != "1":
                    marriageEnd = datetime.strptime(marriageEnd, "%I:%M %p")
                    mergeDTE = datetime.combine(datetime.date(marriageDate), datetime.time(marriageEnd))
                    if mergeDTS >= mergeDTE:
                        checkResult.append("Waktu akad yang anda masukkan tidak valid.")
                    detailInfo['marriage_end'] = int(round(datetime.timestamp(mergeDTE)*1000))

                detailInfo["marriage_date"] = datetime.strftime(marriageDate, "%d %B %Y")
                detailInfo["marriage_start"] = int(round(datetime.timestamp(mergeDTS)*1000))

            # Resepsi
            if receptionDate != "":
                receptionDate = datetime.strptime(receptionDate, "%d %B %Y")
                receptionStart = datetime.strptime(receptionStart, "%I:%M %p")
                mergeDTS = datetime.combine(datetime.date(receptionDate), datetime.time(receptionStart))
                if mergeDTS <= now:
                    checkResult.append("Tanggal yang diinputkan sudah terlewat.")

                if receptionEnd != "1":
                    receptionEnd = datetime.strptime(receptionEnd, "%I:%M %p")
                    mergeDTE = datetime.combine(datetime.date(receptionDate), datetime.time(receptionEnd))
                    if mergeDTS >= mergeDTE:
                        checkResult.append("Waktu resepsi yang anda masukkan tidak valid.")
                    detailInfo['reception_end'] = int(round(datetime.timestamp(mergeDTE)*1000))

                detailInfo["reception_date"] = datetime.strftime(receptionDate, "%d %B %Y")
                detailInfo["reception_start"] = int(round(datetime.timestamp(mergeDTS)*1000))
        # Check Detail Info ---------------------------------------- Finish

        # Check Personal Data ---------------------------------------- Start
        if personData:
            mFName = personalData["man_fullname"]
            wFName = personalData["woman_fullname"]
            mCName = personalData["man_name"]
            wCName = personalData["woman_name"]
            dNo = personalData["daughter_no"]
            sNo = personalData["son_no"]
            mDad = personalData["mans_dad"]
            mMom = personalData["mans_mom"]
            wDad = personalData["womans_dad"]
            wMom = personalData["womans_mom"]

            # Check Unnullable Input ---------------------------------------- Start
            if mFName == "":
                checkResult.append("Nama lengkap mempelai pria tidak boleh kosong.")
            if wFName == "":
                checkResult.append("Nama lengkap mempelai wanita tidak boleh kosong.")
            if mCName == "":
                checkResult.append("Nama panggilan mempelai pria tidak boleh kosong.")
            if wCName == "":
                checkResult.append("Nama panggilan mempelai wanita tidak boleh kosong.")
            if mDad == "":
                checkResult.append("Nama ayah mempelai pria tidak boleh kosong.")
            if wDad == "":
                checkResult.append("Nama ayah mempelai wanita tidak boleh kosong.")
            if mMom == "":
                checkResult.append("Nama ibu mempelai pria tidak boleh kosong.")
            if wMom == "":
                checkResult.append("Nama ibu mempelai wanita tidak boleh kosong.")
            if sNo == "":
                checkResult.append("Urutan mempelai pria sebagai anak dalam keluarga tidak boleh kosong.")
            if dNo == "":
                checkResult.append("Urutan mempelai wanita sebagai anak dalam keluarga tidak boleh kosong.")
            # SCheck Unnullable Input---------------------------------------- Finish

            # Sanitize String ---------------------------------------- Start
            sanit, char = sanitize_all_char(mFName)
            if sanit:
                checkResult.append(f"Nama mempelai pria tidak boleh mengandung karakter {char}.")
            sanit, char = sanitize_all_char(wFName)
            if sanit:
                checkResult.append(f"Nama mempelai wanita tidak boleh mengandung karakter {char}.")
            sanit, char = sanitize_all_char(mCName)
            if sanit:
                checkResult.append(f"Nama mempelai pria tidak boleh mengandung karakter {char}.")
            sanit, char = sanitize_all_char(wCName)
            if sanit:
                checkResult.append(f"Nama mempelai wanita tidak boleh mengandung karakter {char}.")
            sanit, char = sanitize_all_char(mDad)
            if sanit:
                checkResult.append(f"Nama ayah mempelai pria tidak boleh mengandung karakter {char}.")
            sanit, char = sanitize_all_char(wDad)
            if sanit:
                checkResult.append(f"Nama ayah mempelai wanita tidak boleh mengandung karakter {char}.")
            sanit, char = sanitize_all_char(mMom)
            if sanit:
                checkResult.append(f"Nama ibu mempelai pria tidak boleh mengandung karakter {char}.")
            sanit, char = sanitize_all_char(wMom)
            if sanit:
                checkResult.append(f"Nama ibu mempelai wanita tidak boleh mengandung karakter {char}.")
            # Sanitize String ---------------------------------------- Finish
            
            # String Filter ---------------------------------------- Start
            if string_checker(mFName):
                checkResult.append("Nama mempelai pria tidak valid.")
            if string_checker(wFName):
                checkResult.append("Nama mempelai wanita tidak valid.")
            if string_checker(mCName):
                checkResult.append("Nama mempelai pria tidak valid.")
            if string_checker(wCName):
                checkResult.append("Nama mempelai wanita  tidak valid.")
            if string_checker(mDad):
                checkResult.append("Nama ayah mempelai pria tidak valid.")
            if string_checker(wDad):
                checkResult.append("Nama ayah mempelai wanita tidak valid.")
            if string_checker(mMom):
                checkResult.append("Nama ibu mempelai pria tidak valid.")
            if string_checker(wMom):
                checkResult.append("Nama ibu mempelai wanita tidak valid.")
            # String Filter ---------------------------------------- Finish

            mansPhotos = personalData["mans_photo"]
            womansPhotos = personalData["womans_photo"]
            if mansPhotos != "":
                # Memisahkan bagian 'data:' dari base64 string
                mheader, mencoded = mansPhotos.split(',', 1)
                # Memisahkan 'data:' dan mengambil MIME type
                mime_type = mheader.split(':')[1].split(';')[0].split('/')[0]
                if mime_type != "image":
                    checkResult.append("Data foto yang diinputkan harus berupa gambar.")
                else:
                    # Saving File ---------------------------------------- Start
                    mpFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+invCode+"_man_photo_"+userId+".jpg")
                    mpPath = os.path.join(app.config['USER_INVITATION_FILE'], mpFileName)
                    saving_image(mansPhotos, mpPath)
                    personalData['mans_photo'] = mpFileName
                    # Saving File ---------------------------------------- Finish
            else:
                checkResult.append("Foto mempelai pria tidak boleh kosong.")
            
            if womansPhotos != "":
                wheader, wencoded = womansPhotos.split(',', 1)
                mime_type = wheader.split(':')[1].split(';')[0].split('/')[0]
                if mime_type != "image":
                    checkResult.append("Data foto yang diinputkan harus berupa gambar.")
                else:
                    # Saving File ---------------------------------------- Start
                    wpFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+invCode+"_woman_photo_"+userId+".jpg")
                    wpPath = os.path.join(app.config['USER_INVITATION_FILE'], wpFileName)
                    saving_image(womansPhotos, wpPath)
                    personalData['womans_photo'] = wpFileName
                    # Saving File ---------------------------------------- Finish
            else:
                checkResult.append("Foto mempelai wanita tidak boleh kosong.")
        # Check Personal Data ---------------------------------------- Finish

    # Birthday
    elif ckCategory[0]['category'].upper() == "ULANG TAHUN":
        print("kategori => ", ckCategory[0]['category'].upper())
        # Check Detail Info ---------------------------------------- Start
        if detail:
            dates = detailInfo["date"]
            starts = detailInfo["start"]
            ends = detailInfo["end"]
            now = datetime.now()

            # Acara
            if dates != "":
                dates = datetime.strptime(dates, "%d %B %Y")
                starts = datetime.strptime(starts, "%I:%M %p")
                mergeDTS = datetime.combine(datetime.date(dates), datetime.time(starts))
                if mergeDTS <= now:
                    checkResult.append("Tanggal yang diinputkan sudah terlewat.")

                if ends != "1":
                    ends = datetime.strptime(ends, "%I:%M %p")
                    mergeDTE = datetime.combine(datetime.date(dates), datetime.time(ends))
                    if mergeDTS >= mergeDTE:
                        checkResult.append("Waktu pesta ulang tahun yang anda masukkan tidak valid.")
                    detailInfo['end'] = int(round(datetime.timestamp(mergeDTE)*1000))

                detailInfo["date"] = datetime.strftime(dates, "%d %B %Y")
                detailInfo["start"] = int(round(datetime.timestamp(mergeDTS)*1000))
        # Check Detail Info ---------------------------------------- Finish

        # Check Personal Data ---------------------------------------- Start
        if personData:
            fullname = personalData["fullname"]
            callname = personalData["callname"]
            birthday = personalData["birthday"]

            if fullname == "":
                checkResult.append("Nama lengkap tidak boleh kosong.")
            if callname == "":
                checkResult.append("Nama panggilan tidak boleh kosong.")
            if birthday == "":
                checkResult.append("Usia tidak boleh kosong.")

            # Sanitize String ---------------------------------------- Start
            sanitTitle, charTitle = sanitize_all_char(fullname)
            if sanitTitle:
                checkResult.append(f"Nama lengkap tidak boleh mengandung karakter {charTitle}.")
            
            sanitTitle, charTitle = sanitize_all_char(callname)
            if sanitTitle:
                checkResult.append(f"Nama panggilan tidak boleh mengandung karakter {charTitle}.")
            # Sanitize String ---------------------------------------- Finish
            
            # String Filter ---------------------------------------- Start
            if string_checker(fullname):
                checkResult.append(f"Nama tidak valid.")
            # String Filter ---------------------------------------- Finish

            myphoto = personalData["myphoto"]
            if myphoto != "":
                # Memisahkan bagian 'data:' dari base64 string
                mheader, mencoded = myphoto.split(',', 1)
                # Memisahkan 'data:' dan mengambil MIME type
                mime_type = mheader.split(':')[1].split(';')[0].split('/')[0]
                if mime_type != "image":
                    checkResult.append("Data foto yang diinputkan harus berupa gambar.")
                else:
                    # Saving File ---------------------------------------- Start
                    pFName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+invCode+"_mybd_photo_"+userId+".jpg")
                    photoPath = os.path.join(app.config['USER_INVITATION_FILE'], pFName)
                    saving_image(myphoto, photoPath)
                    personalData['myphoto'] = pFName
                    # Saving File ---------------------------------------- Finish
            else:
                checkResult.append("Foto anda tidak boleh kosong.")
        # Check Personal Data ---------------------------------------- Finish
    
    # Graduation
    elif ckCategory[0]['category'].upper() == "GRADUATION PARTY":
        print("kategori => ", ckCategory[0]['category'].upper())
        # Check Detail Info ---------------------------------------- Start
        if detail:
            dates = detailInfo["date"]
            starts = detailInfo["start"]
            ends = detailInfo["end"]
            now = datetime.now()

            # Acara
            if dates != "":
                dates = datetime.strptime(dates, "%d %B %Y")
                starts = datetime.strptime(starts, "%I:%M %p")
                mergeDTS = datetime.combine(datetime.date(dates), datetime.time(starts))
                if mergeDTS <= now:
                    checkResult.append("Tanggal yang diinputkan sudah terlewat.")

                if ends != "1":
                    ends = datetime.strptime(ends, "%I:%M %p")
                    mergeDTE = datetime.combine(datetime.date(dates), datetime.time(ends))
                    if mergeDTS >= mergeDTE:
                        checkResult.append("Waktu akad yang anda masukkan tidak valid.")
                    detailInfo['end'] = int(round(datetime.timestamp(mergeDTE)*1000))

                detailInfo["date"] = datetime.strftime(dates, "%d %B %Y")
                detailInfo["start"] = int(round(datetime.timestamp(mergeDTS)*1000))
        # Check Detail Info ---------------------------------------- Finish

        # Check Personal Data ---------------------------------------- Start
        if personData:
            fullname = personalData["fullname"]
            school = personalData["school"]
            graduate = personalData["graduate"]

            if fullname == "":
                checkResult.append("Nama lengkap tidak boleh kosong.")
            if school == "":
                checkResult.append("Nama sekolah tidak boleh kosong.")
            if graduate == "":
                checkResult.append("Tahun lulus tidak boleh kosong.")

            # Sanitize Title ---------------------------------------- Start
            sanitTitle, charTitle = sanitize_title_char(fullname)
            if sanitTitle:
                checkResult.append(f"Nama tidak boleh mengandung karakter {charTitle}.")
            # Sanitize Title ---------------------------------------- Finish
            
            # String Filter ---------------------------------------- Start
            if string_checker(fullname):
                checkResult.append(f"Nama tidak valid.")
            # String Filter ---------------------------------------- Finish
        # Check Personal Data ---------------------------------------- Finish
    # Check By Category ---------------------------------------- Finish

    # Return Value ========================================
    return checkResult, personalData, detailInfo, invCode

def vld_edit_invitation(result, title, personalData, detailInfo):
    checkResult = []

    oldData = result[0]
    oldData['personal_data'] = json.loads(oldData['personal_data'])
    oldData['detail_info'] = json.loads(oldData['detail_info'])
    # Validation Null Data ---------------------------------------- Start
    if title == "":
        checkResult.append(f"Judul template tidak boleh kosong.")
    if personalData == None:
        checkResult.append(f"Data pribadi tidak boleh kosong tidak boleh kosong.")
    if detailInfo == None:
        checkResult.append(f"Data acara tidak boleh kosong tidak boleh kosong.")
    # # Validation Null Data ---------------------------------------- Finish
    
    # Check Data Title & Template ---------------------------------------- Start
    # Template
    query = TMPLT_GET_BY_ID_QUERY
    values = (oldData['template_id'],)
    ckTemplate = DBHelper().get_count_filter_data(query, values)
    if ckTemplate < 1:
        checkResult.append(f"Data template tidak dapat ditemukan.")
    # Check Data Title & Template ---------------------------------------- Finish
    
    # Sanitize Title ---------------------------------------- Start
    sanitTitle, charTitle = sanitize_title_char(title)
    if sanitTitle:
        checkResult.append(f"Judul tidak boleh mengandung karakter {charTitle}.")
    # Sanitize Title ---------------------------------------- Finish
    
    # String Filter ---------------------------------------- Start
    if string_checker(title):
        checkResult.append(f"Judul tidak valid.")
    # String Filter ---------------------------------------- Finish
    
    # Check Data Category ---------------------------------------- Start
    query = CTGR_GET_BY_ID_QUERY
    values = (oldData['category_id'],)
    ckCategory = DBHelper().get_data(query, values)
    if len(ckCategory) < 1:
        checkResult.append(f"Data kategori tidak dapat ditemukan.")
    # Check Data Category ---------------------------------------- Finish

    # Check Detail Data ---------------------------------------- Start
    detail = True
    if len(detailInfo) < 1:
        detail = False
        checkResult.append("Info acara tidak boleh kosong.")
    personData = True
    if len(personalData) < 1:
        personData = False
        checkResult.append("Info acara tidak boleh kosong.")
    # Check Detail Data ---------------------------------------- Finish

    # Check By Category ---------------------------------------- Start
    # Wedding
    if ckCategory[0]['category'].upper() == "PERNIKAHAN":
        print("kategori => ", ckCategory[0]['category'].upper())
        # Check Detail Info ---------------------------------------- Start
        if detail:
            marriageDate = detailInfo["marriage_date"]
            marriageStart = detailInfo["marriage_start"]
            marriageEnd = detailInfo["marriage_end"]
            receptionDate = detailInfo["reception_date"]
            receptionStart = detailInfo["reception_start"]
            receptionEnd = detailInfo["reception_end"]
            now = datetime.now()

            # Akad
            if marriageDate != "":
                marriageDate = datetime.strptime(marriageDate, "%d %B %Y")
                marriageStart = datetime.strptime(marriageStart, "%I:%M %p")
                mergeDTS = datetime.combine(datetime.date(marriageDate), datetime.time(marriageStart))
                if mergeDTS <= now:
                    checkResult.append("Tanggal yang diinputkan sudah terlewat.")

                if marriageEnd != "1":
                    marriageEnd = datetime.strptime(marriageEnd, "%I:%M %p")
                    mergeDTE = datetime.combine(datetime.date(marriageDate), datetime.time(marriageEnd))
                    if mergeDTS >= mergeDTE:
                        checkResult.append("Waktu akad yang anda masukkan tidak valid.")
                    detailInfo['marriage_end'] = int(round(datetime.timestamp(mergeDTE)*1000))

                detailInfo["marriage_date"] = datetime.strftime(marriageDate, "%d %B %Y")
                detailInfo["marriage_start"] = int(round(datetime.timestamp(mergeDTS)*1000))
            else:
                checkResult.append("Data tanggal tidak boleh kosong")

            # Resepsi
            if receptionDate != "":
                receptionDate = datetime.strptime(receptionDate, "%d %B %Y")
                receptionStart = datetime.strptime(receptionStart, "%I:%M %p")
                mergeDTS = datetime.combine(datetime.date(receptionDate), datetime.time(receptionStart))
                if mergeDTS <= now:
                    checkResult.append("Tanggal yang diinputkan sudah terlewat.")

                if receptionEnd != "1":
                    receptionEnd = datetime.strptime(receptionEnd, "%I:%M %p")
                    mergeDTE = datetime.combine(datetime.date(receptionDate), datetime.time(receptionEnd))
                    if mergeDTS >= mergeDTE:
                        checkResult.append("Waktu resepsi yang anda masukkan tidak valid.")
                    detailInfo['reception_end'] = int(round(datetime.timestamp(mergeDTE)*1000))

                detailInfo["reception_date"] = datetime.strftime(receptionDate, "%d %B %Y")
                detailInfo["reception_start"] = int(round(datetime.timestamp(mergeDTS)*1000))
            else:
                checkResult.append("Data tanggal tidak boleh kosong")
        # Check Detail Info ---------------------------------------- Finish

        # Check Personal Data ---------------------------------------- Start
        if personData:
            mansPhotos = personalData["mans_photo"]
            womansPhotos = personalData["womans_photo"]
            if mansPhotos != oldData['personal_data']['mans_photo']:
                # Memisahkan bagian 'data:' dari base64 string
                mheader, mencoded = mansPhotos.split(',', 1)
                # Memisahkan 'data:' dan mengambil MIME type
                mime_type = mheader.split(':')[1].split(';')[0].split('/')[0]
                if mime_type != "image":
                    checkResult.append("Data foto yang diinputkan harus berupa gambar.")
                else:
                    mpFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+oldData['code']+"_man_photo_"+str(oldData['user_id'])+".jpg")
                    mpPath = os.path.join(app.config['USER_INVITATION_FILE'], mpFileName)
                    saving_image(personalData['mans_photo'], mpPath)
                    personalData['mans_photo'] = mpFileName
                
            if womansPhotos != oldData['personal_data']['womans_photo']:
                wheader, wencoded = womansPhotos.split(',', 1)
                mime_type = wheader.split(':')[1].split(';')[0].split('/')[0]
                if mime_type != "image":
                    checkResult.append("Data foto yang diinputkan harus berupa gambar.")
                else:
                    wpFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+oldData['code']+"_woman_photo_"+str(oldData['user_id'])+".jpg")
                    wpPath = os.path.join(app.config['USER_INVITATION_FILE'], wpFileName)
                    saving_image(personalData['womans_photo'], wpPath)
                    personalData['womans_photo'] = wpFileName
        # Check Personal Data ---------------------------------------- Finish
    
    # Birthday
    elif ckCategory[0]['category'].upper() == "ULANG TAHUN":
        print("kategori => ", ckCategory[0]['category'].upper())
        # Check Detail Info ---------------------------------------- Start
        if detail:
            dates = detailInfo["date"]
            starts = detailInfo["start"]
            ends = detailInfo["end"]
            now = datetime.now()

            # Akad
            if dates != "":
                dates = datetime.strptime(dates, "%d %B %Y")
                starts = datetime.strptime(starts, "%I:%M %p")
                mergeDTS = datetime.combine(datetime.date(dates), datetime.time(starts))
                if mergeDTS <= now:
                    checkResult.append("Tanggal yang diinputkan sudah terlewat.")

                if ends != "1":
                    ends = datetime.strptime(ends, "%I:%M %p")
                    mergeDTE = datetime.combine(datetime.date(dates), datetime.time(ends))
                    if mergeDTS >= mergeDTE:
                        checkResult.append("Waktu pesta ulang tahun yang anda masukkan tidak valid.")
                    detailInfo['end'] = int(round(datetime.timestamp(mergeDTE)*1000))

                detailInfo["date"] = datetime.strftime(dates, "%d %B %Y")
                detailInfo["start"] = int(round(datetime.timestamp(mergeDTS)*1000))
        # Check Detail Info ---------------------------------------- Finish

        # Check Personal Data ---------------------------------------- Start
        if personData:
            myphoto = personalData["myphoto"]
            if myphoto != oldData['personal_data']['myphoto']:
                # Memisahkan bagian 'data:' dari base64 string
                mheader, mencoded = myphoto.split(',', 1)
                # Memisahkan 'data:' dan mengambil MIME type
                mime_type = mheader.split(':')[1].split(';')[0].split('/')[0]
                if mime_type != "image":
                    checkResult.append("Data foto yang diinputkan harus berupa gambar.")
                else:
                    # Saving File ---------------------------------------- Start
                    pFName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+oldData['code']+"_photo_"+str(oldData['user_id'])+".jpg")
                    photoPath = os.path.join(app.config['USER_INVITATION_FILE'], pFName)
                    saving_image(myphoto, photoPath)
                    personalData['myphoto'] = pFName
                    # Saving File ---------------------------------------- Finish
        # Check Personal Data ---------------------------------------- Finish
    
    # Graduation
    elif ckCategory[0]['category'].upper() == "GRADUATION PARTY":
        print("kategori => ", ckCategory[0]['category'].upper())
        # Check Detail Info ---------------------------------------- Start
        if detail:
            dates = detailInfo["date"]
            starts = detailInfo["start"]
            ends = detailInfo["end"]
            now = datetime.now()

            # Akad
            if dates != "":
                dates = datetime.strptime(dates, "%d %B %Y")
                starts = datetime.strptime(starts, "%I:%M %p")
                mergeDTS = datetime.combine(datetime.date(dates), datetime.time(starts))
                if mergeDTS <= now:
                    checkResult.append("Tanggal yang diinputkan sudah terlewat.")

                if ends != "1":
                    ends = datetime.strptime(ends, "%I:%M %p")
                    mergeDTE = datetime.combine(datetime.date(dates), datetime.time(ends))
                    if mergeDTS >= mergeDTE:
                        checkResult.append("Waktu akad yang anda masukkan tidak valid.")
                    detailInfo['end'] = int(round(datetime.timestamp(mergeDTE)*1000))

                detailInfo["date"] = datetime.strftime(dates, "%d %B %Y")
                detailInfo["start"] = int(round(datetime.timestamp(mergeDTS)*1000))
        # Check Detail Info ---------------------------------------- Finish

        # Check Personal Data ---------------------------------------- Start
        if personData:
            fullname = personalData["fullname"]
            school = personalData["school"]
            graduate = personalData["graduate"]

            if fullname != oldData['personal_data']['fullname']:
                if fullname == "":
                    checkResult.append("Nama lengkap tidak boleh kosong.")
                
                # Sanitize Title ---------------------------------------- Start
                sanitTitle, charTitle = sanitize_title_char(fullname)
                if sanitTitle:
                    checkResult.append(f"Nama tidak boleh mengandung karakter {charTitle}.")
                # Sanitize Title ---------------------------------------- Finish
                
                # String Filter ---------------------------------------- Start
                if string_checker(fullname):
                    checkResult.append(f"Nama tidak valid.")
                # String Filter ---------------------------------------- Finish

            if school != oldData['personal_data']['school']:
                if school == "":
                    checkResult.append("Nama sekolah tidak boleh kosong.")
            
            if graduate != oldData['personal_data']['graduate']:
                if graduate == "":
                    checkResult.append("Tahun lulus tidak boleh kosong.")

            
        # Check Personal Data ---------------------------------------- Finish
    
    # Check By Category ---------------------------------------- Finish

    # Return Value ========================================
    return checkResult, personalData, detailInfo
# INVITATION VALIDATION ============================================================ End