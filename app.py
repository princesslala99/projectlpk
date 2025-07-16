
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="🧪 Aplikasi Analisis Regresi dan Evaluasi Kinerja Metode", layout="wide")

st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}
h1, h2, h3 {
    color: white;
}
.stButton > button {
    background: linear-gradient(45deg, #f59e0b, #d97706);
    color: white;
    font-weight: bold;
    font-size: 16px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
}
.stButton > button:hover {
    box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
}
</style>
""", unsafe_allow_html=True)

st.title("🧪 Aplikasi Analisis Regresi dan Evaluasi Kinerja Metode")
st.write("Aplikasi ini membantu menganalisis hubungan antara konsentrasi dan absorbansi, "
         "menghitung presisi (%RPD/%RSD) dan akurasi (%Recovery) untuk data kuantitatif spektrofotometri.")

# --- Step 1: Input Data Standar ---
st.header("🧪 Input Data Standar (Step 1)")
conc_input = st.text_area("📏 Masukkan Konsentrasi (ppm), pisahkan dengan koma:", "0, 1, 2, 3, 4, 5")
abs_input = st.text_area("📊 Masukkan Absorbansi, pisahkan dengan koma:", "0.005, 0.105, 0.205, 0.305, 0.405, 0.505")

def parse_numbers(text):
    try:
        return np.array([float(x.strip()) for x in text.split(",") if x.strip() != ""])
    except:
        return np.array([])

concentrations = parse_numbers(conc_input)
absorbances = parse_numbers(abs_input)

regression_result = {}
calc_concentrations = None

if st.button("⚗ Buat Grafik Regresi Ajaib! ✨"):
    if len(concentrations) < 2 or len(absorbances) < 2:
        st.error("🚨 Masukkan minimal 2 data untuk konsentrasi dan absorbansi!")
    elif len(concentrations) != len(absorbances):
        st.error("🚨 Jumlah data konsentrasi dan absorbansi harus sama!")
    else:
        # Linear regression using sklearn
        x = concentrations.reshape(-1,1)
        y = absorbances
        model = LinearRegression()
        model.fit(x,y)
        slope = model.coef_[0]
        intercept = model.intercept_
        r_squared = model.score(x,y)

        regression_result = {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_squared
        }

        st.success(f"✨ Persamaan Regresi: y = {slope:.4f}x + {intercept:.4f}")
        if r_squared > 0.99:
            status = "🌟 Luar Biasa Sempurna!"
        elif r_squared > 0.95:
            status = "🟢 Sangat Baik!"
        elif r_squared > 0.90:
            status = "🟡 Baik!"
        else:
            status = "🔴 Perlu Perbaikan"
        st.caption(f"Koefisien Determinasi (R²): {r_squared:.6f} {status}")

        # Plot grafis
        fig, ax = plt.subplots()
        ax.scatter(concentrations, absorbances, color='#3B82F6', s=50, label='Data Standar')
        x_line = np.linspace(min(concentrations), max(concentrations), 100)
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, color='#EF4444', linewidth=3, label='Garis Regresi')
        ax.set_xlabel('📏 Konsentrasi (ppm)')
        ax.set_ylabel('📊 Absorbansi')
        ax.set_title('🔬 Kurva Kalibrasi Spektrofotometri 🔬')
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()
        st.pyplot(fig)

# --- Step 2: Input Multi Sampel Absorbansi ---
st.header("🔬 Input Multi Sampel Absorbansi (Step 2)")

sample_absorb_input = st.text_area("📊 Masukkan Absorbansi Sampel (pisahkan dengan koma):", "0.250, 0.255, 0.248")

def calculate_means_and_stddev(values):
    mean_val = np.mean(values)
    std_val = np.std(values, ddof=0)
    return mean_val, std_val

def calculate_precision_auto(concs):
    n = len(concs)
    if n < 2:
        return None, "Minimal 2 data untuk menghitung presisi", None
    if n == 2:
        # %RPD
        c1, c2 = concs
        rpd = abs(c1 - c2) / ((c1 + c2)/2) * 100
        if rpd <= 5:
            status = "🌟 Presisi Luar Biasa!"
        elif rpd <= 10:
            status = "🟢 Presisi Sangat Baik!"
        elif rpd <= 20:
            status = "🟡 Presisi Cukup Baik"
        else:
            status = "🔴 Presisi Perlu Diperbaiki"
        return rpd, status, "%RPD"
    else:
        # %RSD
        mean_val = np.mean(concs)
        std_val = np.std(concs, ddof=0)
        rsd = (std_val / mean_val) * 100
        if rsd <= 2:
            status = "🌟 Presisi Luar Biasa!"
        elif rsd <= 5:
            status = "🟢 Presisi Sangat Baik!"
        elif rsd <= 10:
            status = "🟡 Presisi Cukup Baik"
        else:
            status = "🔴 Presisi Perlu Diperbaiki"
        return rsd, status, "%RSD"

calc_concentrations = None
if st.button("🧪 Hitung Semua Konsentrasi! ⚡"):
    if not regression_result:
        st.error("🚨 Mohon buat grafik regresi terlebih dahulu pada Step 1!")
    else:
        sample_absorbances = parse_numbers(sample_absorb_input)
        if len(sample_absorbances) == 0:
            st.error("🚨 Mohon masukkan nilai absorbansi sampel yang valid!")
        else:
            slope = regression_result['slope']
            intercept = regression_result['intercept']
            calc_concentrations = (sample_absorbances - intercept) / slope

            # Tampilkan tabel hasil
            df_results = pd.DataFrame({
                'Sampel': [f"Sampel {i+1}" for i in range(len(sample_absorbances))],
                'Absorbansi': sample_absorbances,
                'C-terukur (ppm)': calc_concentrations
            })
            st.subheader("📋 Hasil Perhitungan C-terukur")
            st.table(df_results.style.format({"Absorbansi": "{:.4f}", "C-terukur (ppm)": "{:.4f}"}))

            # Statistik ringkas
            mean_c, std_c = calculate_means_and_stddev(calc_concentrations)
            st.markdown(f"*Rata-rata:* {mean_c:.4f} ppm  \n*Standar Deviasi:* {std_c:.4f} ppm  \n*Jumlah Data:* {len(calc_concentrations)}")

            # Evaluasi presisi otomatis
            precision_val, precision_status, precision_type = calculate_precision_auto(calc_concentrations)
            if precision_val is not None:
                st.markdown(f"### 🎯 Evaluasi Presisi ({precision_type})")
                st.markdown(f"{precision_type}:** {precision_val:.2f}%")
                st.markdown(f"*Status:* {precision_status}")
            else:
                st.info(precision_status)

# --- Step 3: Evaluasi Akurasi (%Recovery) ---
st.header("✅ Evaluasi Akurasi (%Recovery)")

col1, col2, col3 = st.columns(3)
with col1:
    c_spike_measured = st.number_input("🧪 C-spike terukur (ppm)", format="%.4f")
with col2:
    c_spike_added = st.number_input("➕ C-spike ditambahkan (ppm)", format="%.4f")
with col3:
    c_sample_initial = st.number_input("🔬 C-sampel awal (ppm)", format="%.4f")

if st.button("✅ Hitung %Recovery 🎉"):
    # Validasi input
    if c_spike_added == 0:
        st.error("🚨 Nilai C-spike ditambahkan harus lebih dari nol!")
    else:
        recovery = ((c_spike_measured - c_sample_initial) / c_spike_added) * 100
        if 95 <= recovery <= 105:
            status = "🌟 Akurasi Sempurna!"
            color = "green"
        elif 90 <= recovery <= 110:
            status = "🟢 Akurasi Sangat Baik!"
            color = "green"
        elif 80 <= recovery <= 120:
            status = "🟡 Akurasi Cukup Baik"
            color = "orange"
        else:
            status = "🔴 Akurasi Perlu Diperbaiki"
            color = "red"

        st.markdown(f"### Hasil %Recovery:")
        st.markdown(f"<div style='font-size: 48px;'>{recovery:.2f}%</div>", unsafe_allow_html=True)
        st.markdown(f"*Status:* <span style='color:{color}; font-weight: bold'>{status}</span>", unsafe_allow_html=True)
        st.caption("Formula: ((C-spike terukur - C-sampel awal) / C-spike ditambahkan) × 100%")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#444; margin-top:20px; margin-bottom:20px;">
    🧪⚗🔬 <br>
    <strong>Lab Digital Pintar!</strong> - Mempercepat analisis data laboratorium dan evaluasi kualitas metode.<br>
    Made with ❤ for Smart Chemistry Analysis
</div>
""", unsafe_allow_html=True)
