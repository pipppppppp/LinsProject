import base64
import hashlib
import os
import random
import re
import string
import uuid
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import cv2
import numpy as np
from flask import current_app as app
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from werkzeug.utils import secure_filename

from .responseHelpers import *


# **************************************************************
# FILE MANAGEMENT | START
# **************************************************************
def default_image():
    file_path = os.path.join(
        app.config["DEFAULT_PHOTOS"],
        "default_avatar.png",
    )

    with open(file_path, "rb") as file:
        return file.read()


def saving_image(encodedData, fileName):
    encoded_data = encodedData.split(",", 1)[1]
    image_buffer = np.frombuffer(
        base64.b64decode(encoded_data),
        np.uint8,
    )
    image = cv2.imdecode(image_buffer, cv2.IMREAD_UNCHANGED)

    return cv2.imwrite(fileName, image)


def saving_file(encodedData, fileName):
    encoded_data = encodedData.split(",", 1)[1]
    file_data = base64.b64decode(encoded_data)

    with open(fileName, "wb") as file:
        file.write(file_data)


def saving_upload_image(file, folder_path):
    if file is None or not file.filename:
        return None

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = (
        f"{uuid.uuid4().hex}_"
        f"{secure_filename(file.filename)}"
    )
    file_path = os.path.join(folder_path, filename)

    file.save(file_path)

    return filename
# **************************************************************
# FILE MANAGEMENT | END
# **************************************************************


# **************************************************************
# CURRENT TIMESTAMP | START
# **************************************************************
def current_timestamp():
    """Return current Unix timestamp in milliseconds."""
    return int(datetime.now().timestamp() * 1000)
# **************************************************************
# CURRENT TIMESTAMP | END
# **************************************************************


# **************************************************************
# RANDOM CHARACTER | START
# **************************************************************
def random_string_number(length):
    characters = (
        string.ascii_lowercase
        + string.ascii_uppercase
        + string.digits
    )

    return "".join(
        random.choice(characters)
        for _ in range(length)
    )


def random_string(length):
    characters = string.ascii_lowercase + string.ascii_uppercase

    return "".join(
        random.choice(characters)
        for _ in range(length)
    )


def random_number(length):
    return "".join(
        random.choice(string.digits)
        for _ in range(length)
    )


def auth_token():
    token = random_string_number(20)

    query = AUTH_GET_BY_TOKEN_QUERY
    values = (token,)
    result = DBHelper().get_count_filter_data(query, values)

    if result > 0:
        return auth_token()

    return token
# **************************************************************
# RANDOM CHARACTER | END
# **************************************************************


# **************************************************************
# SANITIZING STRING | START
# **************************************************************
def _find_forbidden_char(value, forbidden_chars):
    for char in str(value):
        if char in forbidden_chars:
            return True, char

    return False, ""


def sanitize_all_char(value):
    forbidden_chars = {
        "(", ")", "{", "}", "[", "]", "<", ">",
        "_", "-", "*", "%", "+", "/", "'", "$",
        "&", "`", "#", ",", '"', ";", ":", "!",
        "?", "@", "^", "=", "~",
    }

    return _find_forbidden_char(value, forbidden_chars)


def sanitize_title_char(value):
    forbidden_chars = {
        "(", ")", "{", "}", "[", "]", "<", ">",
        "*", "%", "+", "/", "'", "$", "`", "#",
        ",", '"', ";", ":", "!", "?", "@", "^",
        "=", "~",
    }

    return _find_forbidden_char(value, forbidden_chars)


def sanitize_passwd_char(value):
    forbidden_chars = {
        "(", ")", "{", "}", "[", "]", "<", ">",
        "'", "`", ".", ",", '"', ";",
    }

    return _find_forbidden_char(value, forbidden_chars)


def sanitize_email_char(email):
    forbidden_chars = {
        "(", ")", "{", "}", "[", "]", "<", ">",
        "*", "/", "'", "$", "&", "`", ",", '"',
        ";", ":", "?", "^", "=", "~", " ",
    }

    return _find_forbidden_char(email, forbidden_chars)


def sanitize_phone_char(number):
    allowed_chars = set("0123456789+-() ")

    for char in str(number):
        if char not in allowed_chars:
            return True, char

    return False, ""


def sanitize_plate_char(plate_number):
    allowed_pattern = r"^[A-Za-z0-9\s-]+$"
    plate_number = str(plate_number)

    if re.fullmatch(allowed_pattern, plate_number):
        return False, ""

    for char in plate_number:
        if not re.fullmatch(r"[A-Za-z0-9\s-]", char):
            return True, char

    return False, ""

def sanitize_barcode_char(barcode):
    allowed_characters = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "-"
        "_"
        "."
    )

    for character in str(barcode):
        if character not in allowed_characters:
            return True, character

    return False, None

# **************************************************************
# SANITIZING STRING | END
# **************************************************************


# **************************************************************
# NORMALIZE DATA | START
# **************************************************************
def normalize_phone(phone_number):
    phone_number = str(phone_number).strip()
    phone_number = re.sub(r"[\s\-()]", "", phone_number)

    if phone_number.startswith("+62"):
        phone_number = "0" + phone_number[3:]

    elif phone_number.startswith("62"):
        phone_number = "0" + phone_number[2:]

    return phone_number


def normalize_plate_number(plate_number):
    plate_number = str(plate_number).strip().upper()
    compact_plate = re.sub(r"[\s-]+", "", plate_number)

    match = re.fullmatch(
        r"([A-Z]{1,2})([0-9]{1,4})([A-Z]{0,3})",
        compact_plate,
    )

    if not match:
        return re.sub(r"\s+", " ", plate_number)

    prefix, number, suffix = match.groups()

    if suffix:
        return f"{prefix} {number} {suffix}"

    return f"{prefix} {number}"
# **************************************************************
# NORMALIZE DATA | END
# **************************************************************


# **************************************************************
# CHECKER | START
# **************************************************************
def string_checker(strings):
    return any(char.isdigit() for char in str(strings))


def phone_checker(phone_number):
    phone_number = normalize_phone(phone_number)
    pattern = r"^08[1-9][0-9]{7,10}$"

    return re.fullmatch(pattern, phone_number) is None


def email_checker(email):
    email = str(email).strip()
    pattern = (
        r"^[A-Za-z0-9]+"
        r"(?:[._%+-][A-Za-z0-9]+)*"
        r"@[A-Za-z0-9]"
        r"(?:[A-Za-z0-9-]*[A-Za-z0-9])?"
        r"(?:\.[A-Za-z]{2,})+$"
    )

    return re.fullmatch(pattern, email) is None


def password_checker(password):
    password = str(password)
    messages = []

    if len(password) < 6:
        messages.append(
            "Panjang password setidaknya harus 6 karakter."
        )

    if len(password) > 20:
        messages.append(
            "Panjang password tidak boleh lebih dari 20 karakter."
        )

    if not any(char.isdigit() for char in password):
        messages.append(
            "Password harus memiliki setidaknya satu angka."
        )

    if not any(char.isupper() for char in password):
        messages.append(
            "Password harus memiliki setidaknya satu huruf besar."
        )

    if not any(char.islower() for char in password):
        messages.append(
            "Password harus memiliki setidaknya satu huruf kecil."
        )

    error = len(messages) > 0
    message = " ".join(messages)

    return error, message


def plate_checker(plate_number):
    plate_number = normalize_plate_number(plate_number)
    pattern = r"^[A-Z]{1,2} [0-9]{1,4}(?: [A-Z]{1,3})?$"

    return re.fullmatch(pattern, plate_number) is None
# **************************************************************
# CHECKER | END
# **************************************************************


# **************************************************************
# TRANSFORM DATA | START
# **************************************************************
def password_compare(hashedText, password):
    """Compare a plain password with a salted password hash."""
    hashed_text, salt = hashedText.split(":")
    compared_hash = hashlib.sha256(
        salt.encode() + password.encode()
    ).hexdigest()

    return hashed_text == compared_hash


def hash_password(password):
    """Hash a password using SHA-256 and a random salt."""
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha256(
        salt.encode() + password.encode()
    ).hexdigest()

    return f"{hashed_password}:{salt}"


def split_date_time(datetimes):
    months_short = [
        "Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
        "Jul", "Agu", "Sep", "Okt", "Nov", "Des",
    ]
    months_full = [
        "Januari", "Februari", "Maret", "April",
        "Mei", "Juni", "Juli", "Agustus", "September",
        "Oktober", "November", "Desember",
    ]
    days = [
        "Senin", "Selasa", "Rabu", "Kamis",
        "Jumat", "Sabtu", "Minggu",
    ]

    day_format = days[datetimes.weekday()]
    month_format = months_short[datetimes.month - 1]
    full_month_format = months_full[datetimes.month - 1]

    date_data = datetimes.strftime("%d")
    numeric_month_data = datetimes.strftime("%m")
    year_data = datetimes.strftime("%Y")
    time_data = datetimes.strftime("%H:%M")
    time_data_12 = datetimes.strftime("%I:%M")
    hour_data = datetimes.strftime("%H")
    minute_data = datetimes.strftime("%M")
    part_time = datetimes.strftime("%p")

    return {
        "minute": minute_data,
        "hour": hour_data,
        "day": day_format,
        "dates": date_data,
        "month": month_format,
        "fullmonth": full_month_format,
        "no_month": numeric_month_data,
        "year": year_data,
        "time": time_data,
        "etime": f"{time_data_12} {part_time}",
        "day_month": f"{date_data} {month_format}",
        "month_year": f"{month_format} {year_data}",
        "date": f"{date_data} {month_format} {year_data}",
        "date_time": (
            f"{date_data} {month_format} {year_data} "
            f"{time_data_12} {part_time}"
        ),
        "edate_time": datetimes.strftime("%d %B %Y %I:%M %p"),
        "full": (
            f"{day_format}, {date_data} {month_format} "
            f"{year_data}, {datetimes.strftime('%H:%M:%S')}"
        ),
    }
# **************************************************************
# TRANSFORM DATA | END
# **************************************************************


# **************************************************************
# SEND MAIL | START
# **************************************************************
def email_sender(recivier, subject, messages_content):
    """Send an HTML email using the Gmail API."""
    scopes = ["https://www.googleapis.com/auth/gmail.send"]
    credentials = None

    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file(
            "token.json",
            scopes,
        )

    if not credentials or not credentials.valid:
        if (
            credentials
            and credentials.expired
            and credentials.refresh_token
        ):
            try:
                credentials.refresh(Request())

            except Exception:
                if os.path.exists("token.json"):
                    os.remove("token.json")

                credentials = None

        if not credentials or not credentials.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                "apps/utilities/credentials.json",
                scopes,
            )
            credentials = flow.run_local_server(port=5556)

            with open("token.json", "w") as token:
                token.write(credentials.to_json())

    service = build(
        "gmail",
        "v1",
        credentials=credentials,
    )

    message = MIMEMultipart()
    message["to"] = recivier
    message["from"] = "posproject@gmail.com"
    message["subject"] = subject
    message.attach(MIMEText(messages_content, "html"))

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    try:
        result = service.users().messages().send(
            userId="me",
            body={"raw": raw_message},
        ).execute()

        return success_data(result)

    except Exception as error:
        return bad_request(str(error))
# **************************************************************
# SEND MAIL | END
# **************************************************************
