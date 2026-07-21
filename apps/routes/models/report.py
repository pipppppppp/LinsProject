from datetime import datetime
import time

from apps import db
from apps.database.db_workshops import Workshops
from apps.database.db_purchases import Purchases
from apps.utilities.responseHelpers import *
from apps.utilities.utilities import split_date_time
from apps.utilities.validators import role_validator, report_validator
from apps.utilities.formatter import format_date

# Excle
from io import BytesIO
from flask import send_file
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

# pdf
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

# PURCHASE HELPER ============================================================ Begin
def _purchase_report_helper(
    workshop_id,
    start_date,
    end_date,
    supplier_id
):
    purchases = Purchases.query.filter(
        Purchases.workshop_id == workshop_id,
        Purchases.is_delete == 0,
        Purchases.purchase_date >= int(start_date),
        Purchases.purchase_date <= int(end_date)
    )

    if supplier_id != "":
        purchases = purchases.filter(
            Purchases.supplier_id == int(supplier_id)
        )

    purchases = purchases.order_by(
        Purchases.purchase_date.desc()
    ).all()

    total_purchase = len(purchases)
    total_expense = 0

    data = []

    for purchase in purchases:

        purchase_date = split_date_time(
            datetime.fromtimestamp(
                purchase.purchase_date / 1000
            )
        )

        total_expense += purchase.total

        data.append({
            "id": purchase.id,
            "purchase_date": purchase_date,
            "supplier_id": purchase.supplier_id,
            "supplier_name": purchase.suppliers.name if purchase.suppliers else "-",
            "total": purchase.total
        })

    return {
        "summary": {
            "total_purchase": total_purchase,
            "total_expense": total_expense
        },
        "data": data
    }
# PURCHASE HELPER ============================================================ End

# PURCHASE REPORT ============================================================ Begin
def purchase_report(user_role, workshop_id, datas):
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
            "start_date",
            "end_date"
        ]

        for req in required_data:
            if req not in datas:
                return parameter_error(
                    f"Missing {req} in request body."
                )
        # Check Request Body ---------------------------------------- Finish

        # Initialize Data Input ---------------------------------------- Start
        start_date = datas["start_date"]
        end_date = datas["end_date"]
        supplier_id = datas.get("supplier_id", "")
        # Initialize Data Input ---------------------------------------- Finish

        # Data Validation ---------------------------------------- Start
        checker_result = report_validator(
            start_date,
            end_date,
            workshop_id,
            supplier_id=supplier_id
        )

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
        
        result = _purchase_report_helper(
            workshop_id,
            start_date,
            end_date,
            supplier_id
        )

        return success_data(
            data=result,
            status_code=200
        )

    except Exception as e:
        return bad_request(str(e))
# PURCHASE REPORT ============================================================ End

# EXPORT PURCHASE EXCEL ============================================================ Begin
def export_purchase_excel(user_role, workshop_id, datas):
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
            "start_date",
            "end_date"
        ]

        for req in required_data:
            if req not in datas:
                return parameter_error(
                    f"Missing {req} in request body."
                )
        # Check Request Body ---------------------------------------- Finish

        # Initialize Data Input ---------------------------------------- Start
        start_date = datas["start_date"]
        end_date = datas["end_date"]
        supplier_id = datas.get("supplier_id", "")
        # Initialize Data Input ---------------------------------------- Finish

        # Data Validation ---------------------------------------- Start
        checker_result = report_validator(
            start_date,
            end_date,
            workshop_id,
            supplier_id=supplier_id
        )

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

        
        # Create Workbook ---------------------------------------- Start
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Purchase Report"

        # Header Report ---------------------------------------- Start
        worksheet.merge_cells("A1:C1")
        worksheet["A1"] = "LAPORAN PEMBELIAN"
        worksheet.append([])
        worksheet["A1"].font = Font(
            bold=True,
            size=16
        )

        worksheet["A1"].alignment = Alignment(
            horizontal="center"
        )

        worksheet.append([
            "Nama Bengkel",
            workshop.workshop_name
        ])

        worksheet.append([
            "Periode",
            f"{format_date(start_date)} s.d. {format_date(end_date)}"
        ])

        worksheet.append([])
        # Header Report ---------------------------------------- Finish

        worksheet.append([
            "Tanggal",
            "Supplier",
            "Total"
        ])
        # Create Workbook ---------------------------------------- Finish

        result = _purchase_report_helper(
            workshop_id,
            start_date,
            end_date,
            supplier_id
        )

        for item in result["data"]:

            worksheet.append([
                  item["purchase_date"]["date"],
                  item["supplier_name"],
                  f"Rp {item['total']:,}".replace(",", ".")
            ])

        worksheet.append([])

        worksheet.append([
            "Jumlah Pembelian",
            result["summary"]["total_purchase"]
        ])

        worksheet.append([
            "Total Pengeluaran",
            result["summary"]["total_expense"]
        ])

        # Response File ---------------------------------------- Start
        buffer = BytesIO()

        workbook.save(buffer)

        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name="purchase_report.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        # Response File ---------------------------------------- Finish

    except Exception as e:
        raise e
        # return bad_request(str(e))
# EXPORT PURCHASE EXCEL ============================================================ End

# EXPORT PURCHASE PDF ============================================================ Begin
def export_purchase_pdf(user_role, workshop_id, datas):
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
            "start_date",
            "end_date"
        ]

        for req in required_data:
            if req not in datas:
                return parameter_error(
                    f"Missing {req} in request body."
                )
        # Check Request Body ---------------------------------------- Finish

        # Initialize Data Input ---------------------------------------- Start
        start_date = datas["start_date"]
        end_date = datas["end_date"]
        supplier_id = datas.get("supplier_id", "")
        # Initialize Data Input ---------------------------------------- Finish

        # Data Validation ---------------------------------------- Start
        checker_result = report_validator(
            start_date,
            end_date,
            workshop_id,
            supplier_id=supplier_id
        )

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

        result = _purchase_report_helper(
            workshop_id,
            start_date,
            end_date,
            supplier_id
        )

        table_data = [
            [
                  "Tanggal",
                  "Supplier",
                  "Total"
            ]
        ]

        for item in result["data"]:

            table_data.append([
                  item["purchase_date"]["date"],
                  item["supplier_name"],
                  f"Rp {item['total']:,}".replace(",", ".")
            ])       
        # Initialize PDF ---------------------------------------- Start
        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=1.5 * cm,
            rightMargin=1.5 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm
        )

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "<b>LAPORAN PEMBELIAN</b>",
                styles["Title"]
            )
        )
        elements.append(
            Paragraph(
                f"<b>Nama Bengkel :</b> {workshop.workshop_name}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Periode Laporan:</b> "
                f"{format_date(start_date)} "
                f"s.d "
                f"{format_date(end_date)}",
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 0.4 * cm))

        table = Table(
            table_data,
            colWidths=[
                4 * cm,   # Tanggal
                8 * cm,   # Supplier
                5 * cm    # Total
            ],
            repeatRows=1
        )

        table.setStyle(
        TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0d6efd")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),

                ("ALIGN", (0, 0), (0, -1), "CENTER"),   # Tanggal
                ("ALIGN", (1, 0), (1, -1), "LEFT"),     # Supplier
                ("ALIGN", (2, 0), (2, -1), "RIGHT"),    # Total

                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 1), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
            ])
        )

        elements.append(table)

        elements.append(Spacer(1,0.5*cm))

        elements.append(
            Paragraph(
                  f"<b>Jumlah Pembelian :</b> {result['summary']['total_purchase']}",
                  styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                  f"<b>Total Pengeluaran :</b> Rp {result['summary']['total_expense']:,}".replace(",", "."),
                  styles["Normal"]
            )
        )

        document.build(elements)

        buffer.seek(0)
        # Initialize PDF ---------------------------------------- Finish

        # Return File ---------------------------------------- Start
        return send_file(
            buffer,
            as_attachment=True,
            download_name="purchase_report.pdf",
            mimetype="application/pdf"
        )
        # Return File ---------------------------------------- Finish

    except Exception as e:
        raise e
        # return bad_request(str(e))
# EXPORT PURCHASE PDF ============================================================ End