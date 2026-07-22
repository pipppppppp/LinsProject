from datetime import datetime

# FORMAT RUPIAH ============================================================ Begin
def format_rupiah(number):
    try:
        return f"Rp {int(number):,}".replace(",", ".")
    except:
        return "Rp 0"
# FORMAT RUPIAH ============================================================ End


# FORMAT ANGKA ============================================================ Begin
def format_number(number):
    try:
        return "{:,}".format(int(number)).replace(",", ".")
    except:
        return "0"
# FORMAT ANGKA ============================================================ End


# FORMAT DATE ============================================================ Begin
def format_date(timestamp):
    try:
        return datetime.fromtimestamp(
            int(timestamp) / 1000
        ).strftime("%d-%m-%Y")
    except:
        return "-"
# FORMAT DATE ============================================================ End


# FORMAT TIME ============================================================ Begin
def format_time(timestamp):
    try:
        return datetime.fromtimestamp(
            int(timestamp) / 1000
        ).strftime("%H:%M")
    except:
        return "-"
# FORMAT TIME ============================================================ End


# FORMAT DATETIME ============================================================ Begin
def format_datetime(timestamp):
    try:
        return datetime.fromtimestamp(
            int(timestamp)
        ).strftime("%d-%m-%Y %H:%M")
    except:
        return "-"
# FORMAT DATETIME ============================================================ End


# FORMAT PLATE NUMBER ============================================================ Begin
def format_plate_number(plate_number):
    try:
        return plate_number.strip().upper()
    except:
        return ""
# FORMAT PLATE NUMBER ============================================================ End


# FORMAT PHONE NUMBER ============================================================ Begin
def format_phone_number(phone):
    try:
        return phone.replace(" ", "").replace("-", "")
    except:
        return ""
# FORMAT PHONE NUMBER ============================================================ End


# FORMAT TITLE ============================================================ Begin
def format_title(text):
    try:
        return text.title().strip()
    except:
        return ""
# FORMAT TITLE ============================================================ End


# FORMAT UPPER ============================================================ Begin
def format_upper(text):
    try:
        return text.upper().strip()
    except:
        return ""
# FORMAT UPPER ============================================================ End


# FORMAT LOWER ============================================================ Begin
def format_lower(text):
    try:
        return text.lower().strip()
    except:
        return ""
# FORMAT LOWER ============================================================ End