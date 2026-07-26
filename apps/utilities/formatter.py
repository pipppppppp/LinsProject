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
# def format_date(timestamp):
#     try:
#         return datetime.fromtimestamp(
#             int(timestamp) 
#         ).strftime("%d-%m-%Y")
#     except:
#         return "-"

# FORMAT DATE ============================================================ Begin
def format_date(value):
    try:
        value = str(value)

        # Format YYYY-MM-DD
        if "-" in value:
            return datetime.strptime(
                value,
                "%Y-%m-%d"
            ).strftime("%d-%m-%Y")

        # Timestamp
        timestamp = int(value)

        # JavaScript timestamp (13 digit)
        if timestamp > 9999999999:
            timestamp //= 1000

        return datetime.fromtimestamp(
            timestamp
        ).strftime("%d-%m-%Y")

    except Exception:
        return "-"
# FORMAT DATE ============================================================ End

# FORMAT TIME ============================================================ Begin
def format_time(timestamp):
    try:
        return datetime.fromtimestamp(
            int(timestamp)
        ).strftime("%H:%M")
    except:
        return "-"
# FORMAT TIME ============================================================ End


# FORMAT DATETIME ============================================================ Begin
def format_datetime(timestamp):
    try:
        timestamp = int(timestamp)

        if timestamp > 9999999999:
            timestamp //= 1000

        return datetime.fromtimestamp(
            timestamp
        ).strftime("%d-%m-%Y %H:%M")

    except Exception:
        return "-"
# FORMAT DATETIME ============================================================ End

# FORMAT DATE TO TIMESTAMP ============================================================ Begin
def format_date_timestamp(date, end_of_day=False):
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")

        if end_of_day:
            dt = dt.replace(
                hour=23,
                minute=59,
                second=59
            )
        else:
            dt = dt.replace(
                hour=0,
                minute=0,
                second=0
            )

        return int(dt.timestamp() * 1000)

    except Exception:
        return 0
# FORMAT DATE TO TIMESTAMP ============================================================ End

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