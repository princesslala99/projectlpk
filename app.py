import streamlit as st
import numpy as np
import pandas as pd
import base64
import time

st.markdown("""
<style>
/* Sidebar container */
[data-testid="stSidebar"] {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    color: white;
}

/* Container radio */
div[data-baseweb="radio"] {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

/* Hide radio input */
div[data-baseweb="radio"] input[type="radio"] {
    display: none !important;
}

/* Style radio label */
label[data-baseweb="radio"] {
    display: flex;
    align-items: center;
    background-color: #1e293b;
    padding: 0.7rem 1rem;
    border-radius: 12px;
    border: 1.5px solid #334155;
    color: #e2e8f0;
    font-weight: 500;
    font-size: 0.95rem;
    transition: all 0.25s ease-in-out;
    box-shadow: inset 0 0 0 0 transparent;
    min-height: 3.2rem;
}

/* Hover efek */
label[data-baseweb="radio"]:hover {
    background-color: #334155;
    transform: scale(1.03);
    cursor: pointer;
    border-color: #64748b;
}

/* Active radio item */
div[data-baseweb="radio"] > div[aria-checked="true"] label {
    background-color: #0ea5e9 !important;
    border-color: #38bdf8 !important;
    color: white !important;
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.5);
}

/* Jaga jarak dan rapi */
label svg {
    margin-right: 0.6rem;
    min-width: 1rem;
    max-height: 1rem;
}

/* Tekstnya tetap rata kiri */
label[data-baseweb="radio"] > div {
    text-align: left;
    flex-grow: 1;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Background gradient & text */
    .stApp {
        background: linear-gradient(to right, #141e30, #243b55);
        color: white;
    }

    /* Tombol efek */
    div.stButton > button {
        background: #1f6feb;
        color: white;
        padding: 0.6em 1.2em;
        font-weight: bold;
        border-radius: 12px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    div.stButton > button:hover {
        background: #1a4fcc;
        transform: scale(1.05);
    }

    /* Judul dan teks lainnya */
    .stMarkdown, .stText, .stTitle, .stHeader, .stSubheader {
        color: white !important;
    }

    /* Table & dataframe style */
    .stDataFrame, .stTable {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* Fade in efek saat load */
.stApp {
    animation: fadeIn 1.5s ease-in;
}

@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* Tombol animasi glow saat hover */
button[kind="primary"] {
    transition: 0.3s ease;
    box-shadow: 0 0 0px transparent;
}
button[kind="primary"]:hover {
    box-shadow: 0 0 12px rgba(255, 255, 255, 0.5);
    transform: translateY(-2px);
}

/* Efek float untuk icon judul */
.black-box span {
    display: inline-block;
    animation: floatIcon 3s ease-in-out infinite;
}
@keyframes floatIcon {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}

/* Transisi halus di elemen teks */
.black-box, .stMarkdown, .stText, .stTitle, .stHeader, .stSubheader {
    transition: all 0.3s ease-in-out;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Fade in saat load halaman */
.stApp {
    animation: fadeIn 1.2s ease-in;
}

@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(10px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* Custom tombol */
div.stButton > button {
    background-color: #1f77b4;
    color: white;
    padding: 0.6em 1.2em;
    border: none;
    border-radius: 12px;
    font-weight: bold;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    position: relative;
    overflow: hidden;
}

div.stButton > button:hover {
    background-color: #105f99;
    transform: translateY(-2px);
    box-shadow: 0 6px 14px rgba(0,0,0,0.2);
}

div.stButton > button:active {
    transform: scale(0.98);
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

/* Loading spinner (gunakan bersama tombol) */
.spinner-container {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
}

.spinner {
    width: 36px;
    height: 36px;
    border: 4px solid rgba(255, 255, 255, 0.2);
    border-top: 4px solid white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
""", unsafe_allow_html=True)



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
    Langkah kerja aplikasi:  
    1. Masukkan data standar pada menu Regresi & Grafik untuk mendapatkan persamaan linear kalibrasi.
    2. Lanjut ke Hitung Konsentrasi & Presisi untuk menghitung nilai konsentrasi sampel dan uji presisi.
    3. Gunakan menu Evaluasi Akurasi untuk menghitung akurasi metode (%Recovery) berdasarkan uji spike.
    """)
    st.info(
        "Tips: Lakukan input data standar dan klik tombol di setiap langkah. Seluruh fitur bekerja tanpa perlu refresh halaman!"
    )
    st.success("Gunakan sidebar di kiri layar untuk memilih fitur utama.")
# --- MENU: REGRESI & GRAFIK ---
elif menu == "📈 Regresi & Grafik":
    st.markdown("<h2 style='color:#1abc9c;'>📈 Step 1: Regresi & Grafik Kalibrasi</h2>", unsafe_allow_html=True)

    st.markdown("""
        <style>
        button {
            transition: all 0.2s ease-in-out;
            transform: scale(1);
        }
        button:hover {
            transform: scale(1.05);
            background-color: #1d4ed8 !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.header("📈 Analisis Regresi Linier & Grafik Kalibrasi")
    st.caption("Masukkan data konsentrasi dan absorbansi untuk membuat kurva kalibrasi dan persamaan regresi.")

    c1, c2 = st.columns(2)
    with c1:
        conc_str = st.text_area("📏 Konsentrasi (ppm)", "0, 1, 2, 3, 4, 5")
    with c2:
        abs_str = st.text_area("📊 Absorbansi", "0.005, 0.105, 0.205, 0.305, 0.405, 0.505")

    if st.button("⚗ Proses Regresi & Tampilkan Grafik"):
        with st.spinner("Menghitung regresi... mohon tunggu 🙏"):
            x = parse_numbers(conc_str)
            y = parse_numbers(abs_str)

            if x is None or y is None:
                st.error("❌ Input hanya boleh angka dan koma. Periksa kembali format data.")
                st.session_state.reg_ready = False
            elif len(x) < 2 or len(y) < 2:
                st.error("⚠ Minimal dua data konsentrasi dan absorbansi harus terisi.")
                st.session_state.reg_ready = False
            elif len(x) != len(y):
                st.error(f"📉 Jumlah data tidak sama: Konsentrasi: {len(x)}, Absorbansi: {len(y)}")
                st.session_state.reg_ready = False
            else:
                slope, intercept, r2 = linear_regression(x, y)
                if None in [slope, intercept, r2]:
                    st.error("❌ Data tidak bisa di-regresi. Cek nilai input Anda, hindari semua data sama.")
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
                        "Luar Biasa Sempurna! 🎯" if r2 > 0.99
                        else ("Sangat Baik! 👍" if r2 > 0.95 else ("Cukup Baik 💡" if r2 > 0.90 else "Perlu Perbaikan 🔧"))
                    )
                    st.info(f"Status Korelasi: {desc}")

                    import altair as alt
                    chart_df = pd.DataFrame({"Konsentrasi": x, "Absorbansi": y})
                    st.subheader("📊 Grafik Interaktif Kurva Kalibrasi")
                    base = alt.Chart(chart_df).mark_circle(size=80).encode(
                        x="Konsentrasi",
                        y="Absorbansi",
                        tooltip=["Konsentrasi", "Absorbansi"]
                    ).interactive()

                    reg_line = alt.Chart(pd.DataFrame({
                        "Konsentrasi": np.linspace(x.min(), x.max(), 100)
                    })).mark_line(color='orange').encode(
                        x="Konsentrasi",
                        y=alt.Y("y:Q", title="Absorbansi (regresi)")
                    ).transform_calculate(
                        y=f"{slope:.4f} * datum.Konsentrasi + {intercept:.4f}"
                    )

                    st.altair_chart(base + reg_line, use_container_width=True)
    else:
        if st.session_state.get("reg_ready", False):
            st.info("✅ Persamaan regresi sudah tersedia. Lanjutkan ke menu berikutnya untuk hitung sampel.")


# --- MENU: HITUNG KONSENTRASI & PRESISI ---
elif menu == "🧮 Hitung Konsentrasi & Presisi":
    st.markdown("<h2 style='color:#1abc9c;'>🧮 Step 2: Multi Sampel Absorbansi & Hitung Konsentrasi</h2>", unsafe_allow_html=True)

    if not st.session_state.get("reg_ready", False) or st.session_state.slope is None:
        st.warning(
            "⚠ Lakukan perhitungan regresi terlebih dahulu pada menu Regresi & Grafik, agar persamaan regresi tersedia!"
        )
    else:
        abs_samp = st.text_area(
            "📥 Absorbansi Sampel (misal: 0.250, 0.255, 0.248)", "0.250, 0.255, 0.248"
        )

        button_css = """
        <style>
        div.stButton > button:first-child {
            background-color: #3498db;
            color: white;
            border-radius: 8px;
            padding: 0.5em 1em;
            transition: all 0.3s ease-in-out;
            font-weight: bold;
        }
        div.stButton > button:first-child:hover {
            background-color: #2ecc71;
            transform: scale(1.03);
            box-shadow: 0 0 10px rgba(46, 204, 113, 0.7);
        }
        </style>
        """
        st.markdown(button_css, unsafe_allow_html=True)

        if st.button("🧪 Hitung Semua Konsentrasi Sampel"):
            with st.spinner("⏳ Menghitung konsentrasi dan presisi..."):
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

                    st.success("✅ Perhitungan selesai!")

                    st.dataframe(
                        df.style.format({"Absorbansi": "{:.4f}", "C-terukur (ppm)": "{:.4f}"}),
                        use_container_width=True
                    )

                    mean_, std_ = np.mean(c_terukur), np.std(c_terukur, ddof=0)
                    st.markdown(
                        f"<p style='color:#34495e;font-weight:bold;'>📊 Rata-rata: {mean_:.4f} ppm &nbsp;&nbsp;|&nbsp;&nbsp; Standar Deviasi: {std_:.4f} ppm &nbsp;&nbsp;|&nbsp;&nbsp; Jumlah Sampel: {len(c_terukur)}</p>",
                        unsafe_allow_html=True,
                    )

                    prec_val, prec_typ = precision(c_terukur)
                    if prec_val is not None:
                        emoji, status = info_precision(prec_val, prec_typ)
                        st.info(f"{emoji} {prec_typ}: {prec_val:.2f}% — {status}")
                    else:
                        st.info("Isi minimal 2 data konsentrasi untuk hitung presisi.")


# --- MENU: EVALUASI AKURASI (%RECOVERY) ---
elif menu == "✅ Evaluasi Akurasi":
    st.markdown("<h2 style='color:#1abc9c;'>✅ Step 3: Evaluasi Akurasi (%Recovery)</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        s_measured = st.text_input("🧪 C-spike terukur (ppm)", "0")
    with col2:
        s_added = st.text_input("➕ C-spike ditambahkan (ppm)", "0")
    with col3:
        s_awal = st.text_input("🔬 C-sampel awal (ppm)", "0")

    # Tambahkan gaya tombol dengan animasi hover
    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #e67e22;
            color: white;
            border-radius: 8px;
            padding: 0.5em 1em;
            transition: all 0.3s ease-in-out;
            font-weight: bold;
        }
        div.stButton > button:first-child:hover {
            background-color: #27ae60;
            transform: scale(1.05);
            box-shadow: 0 0 10px rgba(39, 174, 96, 0.5);
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("✅ Hitung %Recovery"):
        with st.spinner("⏳ Menghitung akurasi sampel..."):
            def tofloat(x):
                try:
                    return float(x)
                except Exception:
                    return None

            val_measured = tofloat(s_measured)
            val_added = tofloat(s_added)
            val_awal = tofloat(s_awal)

            if None in [val_measured, val_added, val_awal]:
                st.error("❌ Semua input harus berupa angka (gunakan titik untuk desimal).")
            elif val_added == 0:
                st.error("⚠ C-spike ditambahkan harus lebih dari 0.")
            else:
                recovery = ((val_measured - val_awal) / val_added) * 100
                emoji, status = info_akurasi(recovery)
            st.success(f"{emoji} %Recovery = {recovery:.2f}%")
            if 85 <= recovery <= 115:
                st.markdown("<span style='color:#2ecc71;font-weight:bold;'>✅ Hasilnya Bagus! Akurasi pengukuran dalam rentang ideal (85–115%).</span>", unsafe_allow_html=True)
            elif recovery < 85:
                st.markdown("<span style='color:#f39c12;font-weight:bold;'>⚠ %Recovery terlalu rendah. Kemungkinan ada kehilangan analit saat pengujian.</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span style='color:#e74c3c;font-weight:bold;'>⚠ %Recovery terlalu tinggi. Bisa jadi ada kontaminasi atau kesalahan pengukuran.</span>", unsafe_allow_html=True)
            st.caption("📐 Formula: ((C-spike terukur - C-awal) / C-ditambahkan) × 100%")


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
