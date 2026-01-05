import streamlit as st
import json
import os
import requests
from datetime import datetime
import config 

# 1. PHẢI LÀ LỆNH ĐẦU TIÊN
st.set_page_config(page_title=config.TEN_QUAN, layout="wide")

# 2. KHAI BÁO THÔNG TIN (Chỉ khai báo 1 lần)
TELE_TOKEN = "8591455674:AAGkmfCidq4rG7ZLYBrFBgOV79wRvt4D_Jk"
TELE_CHAT_ID = "5538657668"
URL_EXCEL = "https://script.google.com/macros/s/AKfycbzVObamCOlhvvBk2bq3j7KIJsBCIMhl_mNnIYQ_AoqfERTkQ12xD-XUH-W1KkayvJa6IQ/exec"

# 3. HÀM GỬI TELEGRAM (Viết gọn lại)
def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
        payload = {"chat_id": TELE_CHAT_ID, "text": message, "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=10)
    except:
        pass

def send_to_excel(so_ban, mon_an, tong_tien):
    bay_gio = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data = {"thoi_gian": bay_gio, "so_ban": so_ban, "mon_an": mon_an, "tong_tien": tong_tien}
    try: requests.post(URL_EXCEL, json=data, timeout=5)
    except: pass

# --- PHẦN CÒN LẠI CỦA GIAO DIỆN GIỮ NGUYÊN ---
# (Bạn dán tiếp phần code hiển thị bàn và món ăn vào đây)
