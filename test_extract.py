import sys, io
sys.path.insert(0, "/Users/user/ai_agent")
from auth import get_drive_service
import openpyxl

drive = get_drive_service()

def test_fetch():
    # 1. 2026 расчеты с персоналом
    sid_payroll = "1OjK3sigpw9sGUvsJOpxtQFyAd0YKBH7fNVNbjIdIT9g"
    raw = drive.files().export(fileId=sid_payroll, mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet").execute()
    wb = openpyxl.load_workbook(io.BytesIO(raw), data_only=True)
    ws_pay = wb["всего оплачено"]
    print("всего оплачено: R3C7 (июль):", ws_pay.cell(3, 7).value)
    print("оплата норматив: R4C4 (март):", ws_pay.cell(4, 4).value)

    # 2. План факт производства
    sid_prod = "1_xHRTSoDfQdLy9GCcAc71xJlmSUaQYCctJuNVJfCIfg"
    raw2 = drive.files().export(fileId=sid_prod, mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet").execute()
    wb2 = openpyxl.load_workbook(io.BytesIO(raw2), data_only=True)
    print("План факт производства tabs:", wb2.sheetnames)

test_fetch()
