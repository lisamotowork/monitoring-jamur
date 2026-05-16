import streamlit as st
import pandas as pd
from datetime import datetime

# Pengaturan halaman untuk tampilan mobile-friendly
st.set_page_config(page_title="Musi Mushee - Data Pertanian", layout="centered")

st.title("🍄 Monitoring & Update Data Jamur")
st.subheader("Koperasi Produsen Musi Mushee Indonesia")
st.write("Form input performa budidaya dan kalkulasi bagi hasil.")

# --- SECTION 1: MARKET PRICE CONFIGURATION (Bisa Di-update) ---
st.sidebar.header("⚙️ Pengaturan Harga Pasar")
harga_baglog = st.sidebar.number_input("Harga Per Baglog (Rp)", value=5000, step=500)
harga_jual_kg = st.sidebar.number_input("Harga Jual Jamur / Kg (Rp)", value=25000, step=1000)
asumsi_hasil_per_baglog = 0.25 # 250 gram dalam kg

st.sidebar.markdown("---")
st.sidebar.write("**Asumsi Proporsional:** 1 Baglog = 250 gram")

# --- SECTION 2: FORM INPUT DATA PERTANIAN ---
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

    submitted = st.form_submit_data = st.form_submit_button("Hitung & Simpan Data")

# --- SECTION 3: PROSES KALKULASI & LOGIKA BISNIS ---
if submitted:
    # 1. Konversi Panen ke Kilogram
    panen_kg = panen_gram / 1000
    
    # 2. Hitung Nilai Rupiah (Potensi Omzet)
    potensi_omzet = panen_kg * harga_jual_kg
    
    # 3. Hitung Biaya Baglog Proporsional
    # Jika 1 baglog menghasilkan 250g (0.25kg), maka baglog yang "terpakai" secara proporsional untuk hasil panen ini adalah:
    baglog_terpakai_proporsional = panen_kg / asumsi_hasil_per_baglog
    biaya_baglog_proporsional = baglog_terpakai_proporsional * harga_baglog
    
    # 4. Net Profit
    net_profit = potensi_omzet - biaya_baglog_proporsional
    if net_profit < 0:
        net_profit = 0
        
    # 5. Prediksi Penerimaan / Bagi Hasil
    porsi_petani = net_profit * 0.50
    tabungan_petani = net_profit * 0.20
    porsi_musi_mushee = net_profit * 0.30

    # --- SECTION 4: TAMPILAN HASIL (DASHBOARD MOBIL) ---
    st.success("📊 **Hasil Kalkulasi Otomatis:**")
    
    # Menampilkan indikator utama
    st.metric(label="Total Hasil Panen", value=f"{panen_kg:.2f} Kg ({panen_gram} gram)")
    st.metric(label="Potensi Omzet (Kotor)", value=f"Rp {potensi_omzet:,.0f}")
    st.metric(label="Net Profit (Bersih)", value=f"Rp {net_profit:,.0f}")
    
    st.markdown("---")
    st.write("### 💰 Distribusi Bagi Hasil Bersih:")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.info(f"**Petani (50%)**\n\nRp {porsi_petani:,.0f}")
    with col_b:
        st.warning(f"**Tabungan (20%)**\n\nRp {tabungan_petani:,.0f}")
    with col_c:
        st.success(f"**Musi Mushee (30%)**\n\nRp {porsi_musi_mushee:,.0f}")

    # Catatan metodologi akuntansi
    with st.expander("Lihat Detail Perhitungan"):
        st.write(f"- **Baglog Terpakai (Proporsional):** {baglog_terpakai_proporsional:.1f} pcs")
        st.write(f"- **Beban Baglog Diakui:** Rp {biaya_baglog_proporsional:,.0f}")
        st.write("_Beban baglog dihitung proporsional berdasarkan jumlah gram yang dipanen agar cashflow harian tetap mencerminkan profitabilitas yang adil._")