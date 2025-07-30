import streamlit as st
import numpy as np
import pandas as pd
import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-image: url("data:image/jpg;base64,{encoded}");
             background-size: cover;
             background-attachment: fixed;
             background-position: center;
         }}

         /* Kotak transparan hitam di belakang teks */
         .black-box {{
             background-color: rgba(0, 0, 0, 0.6);
             padding: 1.2rem;
             border-radius: 12px;
             color: white;
             margin-bottom: 1rem;
         }}

         /* Ubah warna teks default menjadi putih */
         .stMarkdown, .stText, .stTitle, .stHeader, .stSubheader, .stDataFrame, .stTable {{
             color: white !important;
         }}
         </style>
         """,
        unsafe_allow_html=True
    )
add_bg_from_local("images/background_avif.jpg")

# --- COVER & SIDEBAR MENU ---
st.set_page_config(
    page_title="🧪 Website Kalkulator Analisis Presisi dan Akurasi",
    layout="wide"
)
# COVER: Judul & Deskripsi
with st.container():
    st.markdown(
        """
        <div class="black-box" style='width:100%;text-align:center; margin-bottom:1rem;'>
        <span style='font-size:3rem;'>🧪</span>
        </div>
        <h1 class="black-box" style='text-align:center;'>Website Kalkulator Analisis Presisi & Akurasi</h1>
        <p class="black-box" style='text-align:center; max-width:600px; margin:0 auto;'>
            <em>Lab Digital Pintar Spektrofotometri – Streamlit Edition</em><br>
            Hitung regresi linier, presisi (%RPD/%RSD), dan akurasi (%Recovery) dengan mudah, berbasis input absorbansi dan konsentrasi.
        </p>
        """, unsafe_allow_html=True
    )
    st.markdown("---")

# --- SIDEBAR MENU ---
menu = st.sidebar.radio(
    "Menu Navigasi",
    ["🏠 Beranda", "📈 Regresi & Grafik", "🧮 Hitung Konsentrasi & Presisi", "✅ Evaluasi Akurasi"],
    index=0
)

# --- UTILITIES ---
def parse_numbers(text):
    text = text.strip()
    if not text:
        return np.array([])
    try:
        numbers = [float(x.strip()) for x in text.split(",") if x.strip() != ""]
        return np.array(numbers)
    except Exception:
        return None

def linear_regression(x, y):
    n = len(x)
    sum_x, sum_y = np.sum(x), np.sum(y)
    sum_xx, sum_xy = np.sum(x**2), np.sum(x*y)
    denominator = n * sum_xx - sum_x**2
    if denominator == 0:
        return None, None, None
    slope = (n * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / n
    y_pred = slope * x + intercept
    y_mean = np.mean(y)
    ss_tot = np.sum((y - y_mean)**2)
    ss_res = np.sum((y - y_pred)**2)
    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 1.0
    return slope, intercept, r2

def precision(concs):
    if concs is None or len(concs) < 2:
        return None, ""
    if len(concs) == 2:
        c1, c2 = concs
        pval = abs(c1 - c2) / ((c1 + c2) / 2) * 100 if (c1 + c2) != 0 else 0
        typ = "%RPD"
    else:
        mean = np.mean(concs)
        std = np.std(concs, ddof=0)
        pval = (std / mean) * 100 if mean else 0
        typ = "%RSD"
    return pval, typ

def info_precision(val, typ):
    if val is None:
        return "", ""
    if typ == "%RPD":
        if val <= 5:
            e, s = "🌟", "Presisi Luar Biasa!"
        elif val <= 10:
            e, s = "🟢", "Presisi Sangat Baik!"
        elif val <= 20:
            e, s = "🟡", "Presisi Cukup Baik"
        else:
            e, s = "🔴", "Presisi Perlu Diperbaiki"
    else:
        if val <= 2:
            e, s = "🌟", "Presisi Luar Biasa!"
        elif val <= 5:
            e, s = "🟢", "Presisi Sangat Baik!"
        elif val <= 10:
            e, s = "🟡", "Presisi Cukup Baik"
        else:
            e, s = "🔴", "Presisi Perlu Diperbaiki"
    return e, s

def info_akurasi(val):
    if val is None:
        return "", ""
    if 95 <= val <= 105:
        e, s = "🌟", "Akurasi Sempurna!"
    elif 90 <= val <= 110:
        e, s = "🟢", "Akurasi Sangat Baik!"
    elif 80 <= val <= 120:
        e, s = "🟡", "Akurasi Cukup Baik"
    else:
        e, s = "🔴", "Akurasi Perlu Diperbaiki"
    return e, s

# --- INISIALISASI SESSION STATE REGRESI ---
if "slope" not in st.session_state:
    st.session_state.slope = None
if "intercept" not in st.session_state:
    st.session_state.intercept = None
if "r2" not in st.session_state:
    st.session_state.r2 = None
if "reg_ready" not in st.session_state:
    st.session_state.reg_ready = False

# --- MENU: HOME / COVER ---
if menu == "🏠 Beranda":
    st.subheader("Aplikasi Kalkulator Laboratorium Digital")
    st.markdown("""
    **Langkah kerja aplikasi:**  
    1. Masukkan data standar pada menu **Regresi & Grafik** untuk mendapatkan persamaan linear kalibrasi.
    2. Lanjut ke **Hitung Konsentrasi & Presisi** untuk menghitung nilai konsentrasi sampel dan uji presisi.
    3. Gunakan menu **Evaluasi Akurasi** untuk menghitung akurasi metode (%Recovery) berdasarkan uji spike.
    """)
    st.info(
        "Tips: Lakukan input data standar dan klik tombol di setiap langkah. Seluruh fitur bekerja tanpa perlu refresh halaman!"
    )
    st.success("Gunakan sidebar di kiri layar untuk memilih fitur utama.")
# --- MENU: REGRESI & GRAFIK ---
elif menu == "📈 Regresi & Grafik":
    st.header("Step 1: Input Data Standar (Regresi Linier)")

    c1, c2 = st.columns(2)
    with c1:
        conc_str = st.text_area("📏 Konsentrasi (ppm)", "0, 1, 2, 3, 4, 5")
    with c2:
        abs_str = st.text_area("📊 Absorbansi", "0.005, 0.105, 0.205, 0.305, 0.405, 0.505")

    if st.button("⚗ Buat Grafik & Persamaan Regresi"):
        x = parse_numbers(conc_str)
        y = parse_numbers(abs_str)

        if x is None or y is None:
            st.error("Input hanya boleh angka dan koma. Periksa kembali format data.")
            st.session_state.reg_ready = False
        elif len(x) < 2 or len(y) < 2:
            st.error("Minimal dua data konsentrasi dan absorbansi harus terisi.")
            st.session_state.reg_ready = False
        elif len(x) != len(y):
            st.error(f"Jumlah data tidak sama: Konsentrasi: {len(x)}, Absorbansi: {len(y)}")
            st.session_state.reg_ready = False
        else:
            slope, intercept, r2 = linear_regression(x, y)
            if None in [slope, intercept, r2]:
                st.error("Data tidak bisa di-regresi (cek nilai input Anda, hindari semua data sama).")
                st.session_state.reg_ready = False
            else:
                st.session_state.slope = slope
                st.session_state.intercept = intercept
                st.session_state.r2 = r2
                st.session_state.reg_ready = True
                pers_eq = f"y = {slope:.4f} x + {intercept:.4f}"
                st.success(f"✨ Persamaan Regresi: {pers_eq}")
                st.caption(f"R² = {r2:.4f}")

                desc = (
                    "Luar Biasa Sempurna!"
                    if r2 > 0.99
                    else ("Sangat Baik!" if r2 > 0.95 else ("Cukup Baik" if r2 > 0.90 else "Perlu Perbaikan"))
                )
                st.info(f"Status Korelasi: {desc}")

                chart_df = pd.DataFrame({"Konsentrasi": x, "Absorbansi": y})
                st.subheader("📈 Grafik Kurva Kalibrasi (standar)")
                st.line_chart(chart_df.rename(columns={"Konsentrasi": "index"}).set_index("index"))

                # Grafik prediksi regresi
                pred_df = pd.DataFrame({"Konsentrasi": np.linspace(x.min(), x.max(), 100)})
                pred_df["Absorbansi (regresi)"] = slope * pred_df["Konsentrasi"] + intercept
                plot_df = pd.DataFrame({"Absorbansi": y}, index=x)
                plot_df_pred = pd.DataFrame({"Absorbansi (regresi)": pred_df["Absorbansi (regresi)"]}, index=pred_df["Konsentrasi"])
                st.line_chart(pd.concat([plot_df, plot_df_pred], axis=1))
    else:
        if st.session_state.get("reg_ready", False):
            st.info("Persamaan regresi sudah tersedia. Lanjutkan ke menu berikutnya untuk perhitungan sampel.")

# --- MENU: HITUNG KONSENTRASI & PRESISI ---
elif menu == "🧮 Hitung Konsentrasi & Presisi":
    st.header("Step 2: Multi Sampel Absorbansi & Hitung Konsentrasi")

    if not st.session_state.get("reg_ready", False) or st.session_state.slope is None:
        st.warning(
            "Lakukan perhitungan regresi terlebih dahulu pada menu **Regresi & Grafik**, agar persamaan regresi tersedia!"
        )
    else:
        abs_samp = st.text_area(
            "Absorbansi Sampel (misal: 0.250, 0.255, 0.248)", "0.250, 0.255, 0.248"
        )
        if st.button("🧪 Hitung Semua Konsentrasi Sampel"):
            ys = parse_numbers(abs_samp)
            if ys is None:
                st.error("Absorbansi sampel hanya boleh angka dan koma.")
            elif len(ys) < 1:
                st.error("Isi minimal 1 data absorbansi sampel.")
            else:
                slope = st.session_state.slope
                intercept = st.session_state.intercept
                c_terukur = (ys - intercept) / slope if slope != 0 else np.zeros_like(ys)
                df = pd.DataFrame(
                    {
                        "Sampel": [f"Sampel {i+1}" for i in range(len(ys))],
                        "Absorbansi": ys,
                        "C-terukur (ppm)": c_terukur,
                    }
                )
                st.dataframe(df.style.format({"Absorbansi": "{:.4f}", "C-terukur (ppm)": "{:.4f}"}), use_container_width=True)

                mean_, std_ = np.mean(c_terukur), np.std(c_terukur, ddof=0)
                st.success(f"Rata-rata: {mean_:.4f} ppm | Standar Deviasi: {std_:.4f} ppm | Jumlah Sampel: {len(c_terukur)}")

                prec_val, prec_typ = precision(c_terukur)
                if prec_val is not None:
                    emoji, status = info_precision(prec_val, prec_typ)
                    st.info(f"{emoji} {prec_typ}: {prec_val:.2f}% — {status}")
                else:
                    st.info("Isi minimal 2 data konsentrasi untuk hitung presisi.")

# --- MENU: EVALUASI AKURASI (%RECOVERY) ---
elif menu == "✅ Evaluasi Akurasi":
    st.header("Step 3: Evaluasi Akurasi (%Recovery)")

    k1, k2, k3 = st.columns(3)
    with k1:
        s_measured = st.text_input("🧪 C-spike terukur (ppm)", "0")
    with k2:
        s_added = st.text_input("➕ C-spike ditambahkan (ppm)", "0")
    with k3:
        s_awal = st.text_input("🔬 C-sampel awal (ppm)", "0")
    if st.button("✅ Hitung %Recovery"):
        def tofloat(x):
            try:
                return float(x)
            except Exception:
                return None

        val_measured = tofloat(s_measured)
        val_added = tofloat(s_added)
        val_awal = tofloat(s_awal)
        if None in [val_measured, val_added, val_awal]:
            st.error("Semua input harus berupa angka (dan desimal gunakan titik).")
        elif val_added == 0:
            st.error("C-spike ditambahkan harus > 0.")
        else:
            recovery = ((val_measured - val_awal) / val_added) * 100
            emoji, status = info_akurasi(recovery)
            st.success(f"{emoji} %Recovery = {recovery:.2f}%")
            st.caption(f"Status Akurasi: {status}  \nFormula: ((C-spike terukur - C-awal) / C-ditambahkan) × 100%")

st.markdown(
    """
    <div class="black-box" style='text-align:left;color:gray;font-size:13px;line-height:1.6; margin-top: 2rem;'>
        <p>Web App by Kelompok 10 Kelas 1A</p>
        <p>ALIVIA AZZAHRA - 2460317</p>
        <p>KARINA RAHMA YULITHA - 2460398</p>
        <p>NAILA NASYWA FADHILAH - 2460454</p>
        <p>REVANSHA M. ALAM F. - 2460495</p>
        <p>ZASKIA ADYA RACHMA - 2460545</p>
    </div>
    """,
    unsafe_allow_html=True
)
