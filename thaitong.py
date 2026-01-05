import streamlit as st
import json
import os
import requests
from datetime import datetime
import config

# --- DÒNG NÀY PHẢI ĐƯA LÊN ĐẦU TIÊN ---
st.set_page_config(page_title=config.TEN_QUAN, layout="wide")

# --- CÁC BIẾN KẾT NỐI ---
URL_EXCEL = "https://script.google.com/macros/s/AKfycbzVObamCOlhvvBk2bq3j7KIJsBCIMhl_mNnIYQ_AoqfERTkQ12xD-XUH-W1KkayvJa6IQ/exec"
TELE_TOKEN = "8591455674:AAGkmfCidq4rG7ZLYBrFBgOV79wRvt4D_Jk"
TELE_CHAT_ID = "5538657668"

# --- CÁC HÀM HỖ TRỢ ---
def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
        payload = {"chat_id": TELE_CHAT_ID, "text": message, "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=5)
    except: pass

def send_to_excel(so_ban, mon_an, tong_tien):
    bay_gio = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data = {"thoi_gian": bay_gio, "so_ban": so_ban, "mon_an": mon_an, "tong_tien": tong_tien}
    try: requests.post(URL_EXCEL, json=data, timeout=5)
    except: pass

def save_data(data):
    with open("backup_orders.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

def load_data():
    if os.path.exists("backup_orders.json"):
        try:
            with open("backup_orders.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {f"Bàn {i}": {m: 0 for m in config.menu} for i in range(1, 21)}

# --- KHỞI TẠO SESSION STATE ---
if 'orders' not in st.session_state: st.session_state.orders = load_data()
if 'reset_key' not in st.session_state: st.session_state.reset_key = 0

# --- GIAO DIỆN ---
st.markdown(f"<div style='text-align: center; padding: 10px; border-radius: 15px; background-color: #f8f9fa; border: 2px solid #ce1010;'><h1 style='color: #ce1010; margin: 0;'>👌 {config.TEN_QUAN}</h1><p style='margin: 0; font-weight: bold;'>VietinBank: {config.STK} - {config.TEN_CHU_TK}</p></div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🎮 ĐIỀU KHIỂN")
    so_ban = st.selectbox("CHỌN BÀN", list(st.session_state.orders.keys()))
    if st.button("🔄 LÀM MỚI TOÀN BỘ QUÁN"):
        st.session_state.orders = {f"Bàn {i}": {m: 0 for m in config.menu} for i in range(1, 21)}
        save_data(st.session_state.orders)
        st.session_state.reset_key += 1
        st.rerun()

st.subheader(f"📍 TRẠM TỔNG: {so_ban}")

total_price = 0
order_summary = []
cols = st.columns(3)
for i, (item, price) in enumerate(config.menu.items()):
    with cols[i % 3]:
        qty = st.number_input(f"{item}", min_value=0, step=1, key=f"in_{so_ban}_{item}_{st.session_state.reset_key}", value=st.session_state.orders[so_ban].get(item, 0))
        if qty != st.session_state.orders[so_ban].get(item, 0):
            st.session_state.orders[so_ban][item] = qty
            save_data(st.session_state.orders)
            st.rerun()
        if qty > 0:
            total_price += qty * price
            order_summary.append(f"{item} x{qty}")

if total_price > 0:
    st.divider()
    st.markdown(f"## TỔNG: :red[{total_price:,} VNĐ]")
    if st.button("🔥 THANH TOÁN & BÁO CÁO", type="primary"):
        chuoi_mon = ", ".join(order_summary)
        send_to_excel(so_ban, chuoi_mon, total_price)
        send_telegram(f"<b>🔔 {config.TEN_QUAN}:</b>\n✅ {so_ban} đã trả: <b>{total_price:,}đ</b>\n📝 {chuoi_mon}")
        st.balloons()
        st.session_state.orders[so_ban] = {m: 0 for m in config.menu}
        save_data(st.session_state.orders)
        st.session_state.reset_key += 1
        st.rerun()
    
    qr_url = f"https://img.vietqr.io/image/{config.NGAN_HANG}-{config.STK}-compact2.png?amount={total_price}&addInfo=THANH%20TOAN%20{so_ban.replace(' ', '%20')}"
    st.image(qr_url, width=300)

st.markdown("<br><br><br><hr>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align: center; color: #555;'><p>🚀 <b>{config.TEN_QUAN} - QUẢN LÝ THÔNG MINH</b></p><p>Hỗ trợ Zalo: <b>0814830562</b></p></div>", unsafe_allow_html=True)

