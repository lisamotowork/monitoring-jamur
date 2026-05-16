import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# Pengaturan halaman mobile-friendly
st.set_page_config(page_title="Musi Mushee - Data Pertanian", layout="centered")

st.title("🍄 Monitoring & Update Data Jamur")
st.subheader("Koperasi Produsen Musi Mushee Indonesia")

# Membuat Menu Tab di Bagian Atas Aplikasi
tab1, tab2 = st.tabs(["📝 Input Data", "📊 Lihat Laporan"])

# Hubungkan ke Google Sheets secara otomatis
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_existing = conn.read(ttl=0) # Membaca data yang sudah ada
except:
    df_existing = pd.DataFrame()

# --- TAB 1: FORM INPUT DATA ---
with tab1:
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

        # Tampilkan Hasil Sementara di Layar
        st.success("📊 Data Berhasil Dihitung & Dikirim!")
        st.metric(label="Net Profit (Bersih)", value=f"Rp {net_profit:,.0f}")
        
        # PROSES SIMPAN KE GOOGLE SHEETS
        data_baru = pd.DataFrame([{
            "Tanggal": tanggal.strftime('%Y-%m-%d'),
            "Lokasi": nama_lokasi,
            "Petani": nama_petani,
            "Suhu": suhu,
            "Kelembaban": kelembaban,
            "Panen (Gram)": panen_gram,
            "Jumlah Baglog": jumlah_baglog,
            "Net Profit": net_profit,
            "Bagi Hasil Petani": porsi_petani,
            "Tabungan Petani": tabungan_petani,
            "Musi Mushee": porsi_musi_mushee
        }])
        
        # Gabungkan data lama dan baru lalu upload kembali
        df_update = pd.concat([df_existing, data_baru], ignore_index=True)
        conn.update(data=df_update)
        st.balloons() # Efek perayaan data tersimpan!

# --- TAB 2: LIHAT LAPORAN HISTORIS ---
with tab2:
    st.header("📋 Laporan Historis Pertanian")
    if not df_existing.empty:
        st.dataframe(df_existing, use_container_width=True)
    else:
        st.write("Belum ada data yang tersimpan atau koneksi sedang memuat.")
