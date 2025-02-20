import time
import requests
import hashlib
import hmac
import base64
from datetime import datetime, timedelta
from openpyxl import Workbook
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# 네이버 API 인증 정보 (사용자가 실제 정보로 대체해야 함)
API_KEY = '01000000003d6b685cab0e176867f19861c805a7144e987fa37d4bf28b06763f0cfeb3fc68'
SECRET_KEY = 'AQAAAAA9a2hcqw4XaGfxmGHIBacURkemcrYGBP3AXv0yRZfZKw=='
CUSTOMER_ID = '1660926'
NAVER_CLIENT_ID = 's9Wm7PWSiMMUJNXdF9eB'
NAVER_CLIENT_SECRET = 'qPVJadsXN0'

BASE_URL = 'https://api.searchad.naver.com'
DATELAB_URL = "https://openapi.naver.com/v1/datalab/search"

def generate_signature(method, uri, timestamp, secret_key):
    message = f"{timestamp}.{method}.{uri}"
    hash_value = hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(hash_value).decode('utf-8')

def get_searchad_data(keyword):
    # 이전에 월간 검색량을 성공적으로 가져오던 로직 복원
    timestamp = str(int(time.time() * 1000))
    uri = '/keywordstool'
    signature = generate_signature('GET', uri, timestamp, SECRET_KEY)

    headers = {
        "X-Timestamp": timestamp,
        "X-API-KEY": API_KEY,
        "X-Customer": CUSTOMER_ID,
        "X-Signature": signature,
        "Content-Type": "application/json"
    }

    params = {
        'hintKeywords': keyword,
        'showDetail': 1
    }

    response = requests.get(BASE_URL + uri, headers=headers, params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    if response.status_code == 200:
        result = response.json()
        for item in result.get('keywordList', []):
            if item.get('relKeyword') == keyword:
                pc_search_volume = int(round(item.get('monthlyPcQcCnt', 0) or 0))
                mobile_search_volume = int(round(item.get('monthlyMobileQcCnt', 0) or 0))
                total_search_volume = pc_search_volume + mobile_search_volume
                return pc_search_volume, mobile_search_volume, total_search_volume

    print(f"Error {response.status_code}: {response.text}")
    return 0, 0, 0

def get_datalab_period_data(keyword, start_date, end_date):
    headers = {
        'X-Naver-Client-Id': NAVER_CLIENT_ID,
        'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,
        'Content-Type': 'application/json'
    }

    body_pc = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": "date",
        "keywordGroups": [{"groupName": keyword, "keywords": [keyword]}],
        "device": "pc",
        "ages": ["1","2","3","4","5","6"]
    }

    body_mo = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": "date",
        "keywordGroups": [{"groupName": keyword, "keywords": [keyword]}],
        "device": "mo",
        "ages": ["1","2","3","4","5","6"]
    }

    response_pc = requests.post(DATELAB_URL, headers=headers, json=body_pc)
    response_mo = requests.post(DATELAB_URL, headers=headers, json=body_mo)

    print("PC 요청 결과:")
    print(f"Status Code: {response_pc.status_code}")
    print(f"Response Text: {response_pc.text}")

    print("모바일 요청 결과:")
    print(f"Status Code: {response_mo.status_code}")
    print(f"Response Text: {response_mo.text}")

    if response_pc.status_code == 200 and response_mo.status_code == 200:
        pc_data = response_pc.json().get('results', [])[0].get('data', [])
        mo_data = response_mo.json().get('results', [])[0].get('data', [])
        return pc_data, mo_data
    else:
        return [], []

def save_excel_file(wb):
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        wb.save(file_path)
        print(f"엑셀 파일이 '{file_path}'에 저장되었습니다.")
    else:
        messagebox.showerror("경로 오류", "파일 경로를 지정하지 않았습니다.")

def gui():
    root = tk.Tk()
    root.title("NAVER 키워드 쿼리량 추출기")
    root.geometry("500x500")
    root.configure(bg="black")

    tk.Label(root, text="NAVER 키워드 쿼리량 추출기", fg="white", bg="black", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(root, text="키워드를 입력하세요 (쉼표로 구분):", fg="white", bg="black", font=("Arial", 10)).pack(pady=10)
    keywords_entry = tk.Entry(root, width=50)
    keywords_entry.pack(pady=5)

    tk.Label(root, text="시작 날짜를 선택하세요:", fg="white", bg="black", font=("Arial", 10)).pack(pady=10)
    date_frame = tk.Frame(root, bg="black")
    date_frame.pack(pady=5)

    year_values = [str(year) for year in range(2020, 2026)]
    month_values = [str(month).zfill(2) for month in range(1, 13)]
    day_values = [str(day).zfill(2) for day in range(1, 32)]

    year_combo = ttk.Combobox(date_frame, values=year_values, width=5)
    year_combo.set(datetime.now().year)
    year_combo.grid(row=0, column=0, padx=5)

    month_combo = ttk.Combobox(date_frame, values=month_values, width=3)
    month_combo.set(str(datetime.now().month).zfill(2))
    month_combo.grid(row=0, column=1, padx=5)

    day_combo = ttk.Combobox(date_frame, values=day_values, width=3)
    day_combo.set(str(datetime.now().day).zfill(2))
    day_combo.grid(row=0, column=2, padx=5)

    def get_selected_date():
        return f"{year_combo.get()}-{month_combo.get()}-{day_combo.get()}"

    def on_run():
        keywords = keywords_entry.get()
        start_date = get_selected_date()
        end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        if not keywords:
            messagebox.showerror("입력 오류", "모든 입력란을 채워주세요.")
            return

        run_program(keywords, start_date, end_date)

    tk.Button(root, text="실행", command=on_run, bg="white", fg="black", font=("Arial", 10)).pack(pady=20)

    tk.Label(root, text="ver.01.03", fg="white", bg="black", font=("Arial", 8)).pack(side="bottom", pady=2)
    tk.Label(root, text="종료일자는 현재일자-1 입니다.", fg="white", bg="black", font=("Arial", 8)).pack(side="bottom", pady=2)
    tk.Label(root, text="실측치가 아닌 계산을 통한 수치이므로 네이버 실제 쿼리수와 차이가 있습니다.", fg="white", bg="black", font=("Arial", 8), justify="center").pack(side="bottom")
    tk.Label(root, text="출처: 네이버데이터랩, 네이버키워드도구", fg="white", bg="black", font=("Arial", 8)).pack(side="bottom", pady=2)
    tk.Label(root, text="ⓒ2024. GARY all rights reserved - 무단배포를 금합니다", fg="white", bg="black", font=("Arial", 8)).pack(side="bottom")

    root.mainloop()

def run_program(keywords_input, start_date_input, end_date_input):
    wb = Workbook()
    ws = wb.active
    ws.title = "Keyword Data"
    ws.append(["키워드", "날짜", "PC 쿼리수", "모바일 쿼리수", "PC+모바일 쿼리수"])

    keywords = [kw.strip() for kw in keywords_input.split(',')]

    for keyword in keywords:
        process_keyword(keyword, start_date_input, end_date_input, ws)

    save_excel_file(wb)

def process_keyword(keyword, start_date, end_date, ws):
    print(f"\n--- 키워드: {keyword} ---")

    # (1) 키워드도구에서 최근 한달 검색량 (PC/모바일)
    pc_search_volume, mobile_search_volume, total_search_volume = get_searchad_data(keyword)
    if total_search_volume == 0:
        print(f"Error: 키워드도구에서 월간 검색량을 가져오지 못했습니다. 키워드: {keyword}")
        return

    # 기준기간: 최근 30일
    end_date_base = (datetime.now() - timedelta(days=1)).date()
    start_date_base = (end_date_base - timedelta(days=29)).strftime('%Y-%m-%d')
    end_date_base_str = end_date_base.strftime('%Y-%m-%d')

    # (2) 최근 한달 데이터랩 비율(PC, 모바일)
    pc_data_base, mo_data_base = get_datalab_period_data(keyword, start_date_base, end_date_base_str)
    if not pc_data_base or not mo_data_base:
        print(f"Error: 기준 기간 데이터가 없습니다. 키워드: {keyword}")
        return

    pc_total_ratio_base = sum(d['ratio'] for d in pc_data_base)
    mo_total_ratio_base = sum(d['ratio'] for d in mo_data_base)

    if pc_total_ratio_base == 0 or mo_total_ratio_base == 0:
        print(f"Error: 기준 기간 비율 합계가 0입니다. 키워드: {keyword}")
        return

    # (3) A 계산
    A_pc = pc_search_volume / pc_total_ratio_base
    A_mo = mobile_search_volume / mo_total_ratio_base

    # (4) B 계산: (데이터랩 최근한달 일자별 비율)*A = B
    B_pc = [{"date": d["period"], "value": d["ratio"] * A_pc} for d in pc_data_base]
    B_mo = [{"date": d["period"], "value": d["ratio"] * A_mo} for d in mo_data_base]

    B_pc_last = B_pc[-1]["value"]
    B_mo_last = B_mo[-1]["value"]

    # (6) 설정기간 데이터
    pc_data_period, mo_data_period = get_datalab_period_data(keyword, start_date, end_date)
    if not pc_data_period or not mo_data_period:
        print(f"Error: 설정 기간 데이터를 가져오지 못했습니다. 키워드: {keyword}")
        return

    # (7) 마지막 일자 비율 C
    pc_last_ratio_period = pc_data_period[-1]["ratio"]
    mo_last_ratio_period = mo_data_period[-1]["ratio"]

    if pc_last_ratio_period == 0 or mo_last_ratio_period == 0:
        print(f"Error: 설정기간 마지막 일자 비율이 0입니다. 키워드: {keyword}")
        return

    # (8) B/C = D
    D_pc = B_pc_last / pc_last_ratio_period
    D_mo = B_mo_last / mo_last_ratio_period

    # 최종 계산: 설정기간 일자별 비율 * D
    # 여기서 사용자가 언급한 대로 A를 다시 곱하지 않음.
    for i in range(len(pc_data_period)):
        date = pc_data_period[i]["period"]
        pc_ratio_day = pc_data_period[i]["ratio"]
        mo_ratio_day = mo_data_period[i]["ratio"]

        pc_calculated_value = int(round(pc_ratio_day * D_pc))
        mobile_calculated_value = int(round(mo_ratio_day * D_mo))
        total_calculated_value = pc_calculated_value + mobile_calculated_value

        ws.append([keyword, date, pc_calculated_value, mobile_calculated_value, total_calculated_value])
        print(f"{keyword}\t{date}\tPC: {pc_calculated_value}\t모바일: {mobile_calculated_value}\tPC+모바일: {total_calculated_value}")

if __name__ == "__main__":
    gui()
    
