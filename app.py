import streamlit as st
from datetime import datetime
import requests

# Pengaturan halaman mobile-friendly
st.set_page_config(page_title="Musi Mushee - Data Pertanian", layout="centered")

st.title("🍄 Monitoring & Update Data Jamur")
st.subheader("Koperasi Produsen Musi Mushee Indonesia")

# Pengaturan Harga Pasar
st.sidebar.header("⚙️ Pengaturan Harga Pasar")
harga_baglog = st.sidebar.number_input("Harga Per Baglog (Rp)", value=5000, step=500)
harga_jual_kg = st.sidebar.number_input("Harga Jual Jamur / Kg (Rp)", value=25000, step=1000)
asumsi_hasil_per_baglog = 0.25 

with st.form("form_pertanian", clear_on_submit=True):
    st.header("📝 Input Data Harian")
    nama_lokasi = st.text_input("Nama Lokasi / Greenhouse", placeholder="Contoh: GH Sukarami")
    nama_petani = st.text_input("Nama Petani", placeholder="Contoh: Ibu Siti")
    tanggal = st.date_input("Tanggal Input", datetime.now())
    
    col1, col2 = st.columns(2)
    with col1:
        suhu = st.number_input("Nilai Suhu (°C)", value=27.0, step=0.1)
        panen_gram = st.number_input("Hasil Panen (Gram)", value=0, step=100)
    with col2:
        kelembaban = st.number_input("Kelembaban (%)", value=85, step=1)
        jumlah_baglog = st.number_input("Jumlah Baglog Aktif", value=0, step=10)

    submitted = st.form_submit_button("Hitung & Simpan Permanen")

if submitted:
    panen_kg = panen_gram / 1000
    potensi_omzet = panen_kg * harga_jual_kg
    baglog_terpakai = panen_kg / asumsi_hasil_per_baglog
    biaya_baglog = baglog_terpakai * harga_baglog
    net_profit = max(0, potensi_omzet - biaya_baglog)
    
    porsi_petani = net_profit * 0.50
    tabungan_petani = net_profit * 0.20
    porsi_musi_mushee = net_profit * 0.30

    # TAMPILKAN HASIL DI LAYAR HP PETANI
    st.success("📊 Kalkulasi Berhasil!")
    st.metric(label="Net Profit (Bersih)", value=f"Rp {net_profit:,.0f}")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a: st.info(f"Petani: Rp {porsi_petani:,.0f}")
    with col_b: st.warning(f"Tabungan: Rp {tabungan_petani:,.0f}")
    with col_c: st.success(f"Musi Mushee: Rp {porsi_musi_mushee:,.0f}")

    # --- BAGIAN PENGIRIMAN DATA ---
    # GANTI LINK DI BAWAH INI DENGAN 'WEB APP URL' YANG ANDA SALIN DARI LANGKAH 1
    url_penerima = "https://script.google.com/macros/s/AKfycbztWsRY3K-IqwLvTxYpfPOEmP7_OzY1ZmnfXz98xdMWyr_oWMGDQI6pNW_dNvP83aQUQw/exec"
    
    payload = {
        "Tanggal": tanggal.strftime('%Y-%m-%d'),
        "Lokasi": nama_lokasi,
        "Petani": nama_petani,
        "Suhu": suhu,
        "Kelembaban": kelembaban,
        "Panen_Gram": panen_gram,
        "Jumlah_Baglog": jumlah_baglog,
        "Net_Profit": net_profit,
        "Bagi_Hasil_Petani": porsi_petani,
        "Tabungan_Petani": tabungan_petani,
        "Musi_Mushee": porsi_musi_mushee
    }
    
    try:
        response = requests.post(url_penerima, json=payload)
        if response.status_code == 200:
            st.balloons()
            st.success("✅ Data Laporan Berhasil Dikirim ke Google Sheets!")
        else:
            st.error("Gagal menyimpan ke Google Sheets, periksa link Web App Anda.")
    except:
        st.error("Koneksi gagal, silakan coba beberapa saat lagi.")
