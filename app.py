import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config
(
    page_title==("🧪 Aplikasi Analisis Regresi dan Evaluasi Kinerja Metode",
    layout=="wide")
    )

st.title("🧪 Aplikasi Analisis Regresi & Evaluasi Kinerja Metode")
st.caption("Lab Digital Pintar Spektrofotometri – Streamlit Edition")

# --- Utility Functions ---
def parse_numbers(text):
    return np.array([float(x.strip()) for x in text.split(",") if x.strip() != ""])

def linear_regression(x, y):
    n = len(x)
    sum_x, sum_y = np.sum(x), np.sum(y)
    sum_xx, sum_xy = np.sum(x**2), np.sum(x*y)
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x**2)
    intercept = (sum_y - slope * sum_x) / n
    # R squared
    y_mean = np.mean(y)
    ss_tot = np.sum((y - y_mean)**2)
    ss_res = np.sum((y - (slope * x + intercept))**2)
    r2 = 1 - ss_res/ss_tot if ss_tot else 1.0
    return slope, intercept, r2

def precision(concs):
    n = len(concs)
    if n < 2: return None, ""
    if n == 2:
        c1, c2 = concs
        pval = abs(c1-c2)/((c1+c2)/2)*100
        typ = "%RPD"
    else:
        mean = np.mean(concs)
        std = np.std(concs, ddof=0)
        pval = (std/mean)*100 if mean else 0
        typ = "%RSD"
    return pval, typ

def info_precision(val, typ):
    if typ=="%RPD":
        if val<=5: e,s="🌟","Presisi Luar Biasa!"
        elif val<=10: e,s="🟢","Presisi Sangat Baik!"
        elif val<=20: e,s="🟡","Presisi Cukup Baik"
        else: e,s="🔴","Presisi Perlu Diperbaiki"
    else:
        if val<=2: e,s="🌟","Presisi Luar Biasa!"
        elif val<=5: e,s="🟢","Presisi Sangat Baik!"
        elif val<=10: e,s="🟡","Presisi Cukup Baik"
        else: e,s="🔴","Presisi Perlu Diperbaiki"
    return e,s

def info_akurasi(val):
    if 95<=val<=105: e,s="🌟","Akurasi Sempurna!"
    elif 90<=val<=110: e,s="🟢","Akurasi Sangat Baik!"
    elif 80<=val<=120: e,s="🟡","Akurasi Cukup Baik"
    else: e,s="🔴","Akurasi Perlu Diperbaiki"
    return e,s

# ---- Step 1: Input Data Standar ----
st.header("Step 1: Input Data Standar")
c1, c2 = st.columns(2)
with c1:
    conc_str = st.text_area("📏 Konsentrasi (ppm)", "0, 1, 2, 3, 4, 5")
with c2:
    abs_str = st.text_area("📊 Absorbansi", "0.005, 0.105, 0.205, 0.305, 0.405, 0.505")

x, y = parse_numbers(conc_str), parse_numbers(abs_str)
reg_ready = (len(x)==len(y)) and len(x)>=2

show_reg = st.button("⚗ Buat Grafik & Persamaan Regresi")

slope = intercept = r2 = None

if show_reg:
    if not reg_ready:
        st.error("Data tidak valid: jumlah x dan y tidak sama/minimal 2.")
    else:
        slope, intercept, r2 = linear_regression(x, y)
        pers_eq = f"y = {slope:.4f} x + {intercept:.4f}"
        st.success(f"✨ Persamaan Regresi: {pers_eq}")
        st.caption(f"R² = {r2:.4f}")

        desc = "Luar Biasa Sempurna!" if r2 > 0.99 else ("Sangat Baik!" if r2 > 0.95 else ("Cukup Baik" if r2 > 0.90 else "Perlu Perbaikan"))
        st.info(f"Status Korelasi: {desc}")

        # Tampilkan Grafik
        # Data + garis regresi: pakai DataFrame multi-column
        chart_df = pd.DataFrame({'Konsentrasi': x, 'Absorbansi': y})
        st.subheader("📈 Grafik Kurva Kalibrasi")
        st.line_chart(chart_df.rename(columns={'Konsentrasi':'index'}).set_index('index'))

        # Buat prediksi regresi untuk seluruh rentang hubungan
        pred_df = pd.DataFrame({
            'Konsentrasi': np.linspace(x.min(), x.max(), 100)
        })
        pred_df['Absorbansi_pred'] = slope * pred_df['Konsentrasi'] + intercept
        # Gabung data asli + garis prediksi
        fig_chart = pd.DataFrame({'Absorbansi': y}, index=x)
        fig_chart_pred = pd.DataFrame({'Absorbansi (regresi)': pred_df['Absorbansi_pred'].values}, index=pred_df['Konsentrasi'])
        st.line_chart(pd.concat([fig_chart, fig_chart_pred], axis=1))
else:
    st.info("Klik tombol untuk membuat persamaan & grafik regresi.")

# ---- Step 2: Multi Sampel Absorbansi ----
st.header("Step 2: Multi Sampel Absorbansi & Hitung Konsentrasi")
abs_samp = st.text_area("Absorbansi Sampel (koma, mis: 0.250, 0.255, 0.248)", "0.250, 0.255, 0.248")
cek_kons = st.button("🧪 Hitung Semua Konsentrasi Sampel!")
c_terukur = None

if cek_kons:
    if not (slope and intercept):
        st.error("Buat regresi dulu pada Step 1!")
    else:
        ys = parse_numbers(abs_samp)
        c_terukur = (ys - intercept) / slope if slope else [0]*len(ys)
        df = pd.DataFrame({
            'Sampel': [f"Sampel {i+1}" for i in range(len(ys))],
            'Absorbansi': ys,
            'C-terukur (ppm)': c_terukur
        })
        st.dataframe(df.style.format({'Absorbansi':'{:.4f}','C-terukur (ppm)':'{:.4f}'}), use_container_width=True)

        mean_, std_ = np.mean(c_terukur), np.std(c_terukur, ddof=0)
        st.success(f"Rata-rata: {mean_:.4f} ppm | Standar Deviasi: {std_:.4f} ppm | Jumlah Sampel: {len(c_terukur)}")

        prec_val, prec_typ = precision(c_terukur)
        if prec_val is not None:
            emoji, status = info_precision(prec_val, prec_typ)
            st.info(f"{emoji} {prec_typ}: {prec_val:.2f}% — {status}")
        else:
            st.info("Isi minimal 2 data konsentrasi untuk hitung presisi.")

# --- Step 3: Evaluasi Akurasi (%Recovery) ---
st.header("Step 3: Evaluasi Akurasi (%Recovery)")
k1, k2, k3 = st.columns(3)
with k1:
    s_measured = st.number_input("🧪 C-spike terukur (ppm)", min_value=0.0, format="%.4f")
with k2:
    s_added = st.number_input("➕ C-spike ditambahkan (ppm)", min_value=0.0, format="%.4f")
with k3:
    s_awal = st.number_input("🔬 C-sampel awal (ppm)", min_value=0.0, format="%.4f")
rekov = st.button("✅ Hitung %Recovery")

if rekov:
    if s_added == 0:
        st.error("C-spike ditambahkan harus > 0.")
    else:
        recovery = ((s_measured-s_awal)/s_added)*100
        emoji, status = info_akurasi(recovery)
        st.success(f"{emoji} %Recovery = {recovery:.2f}%")
        st.caption(f"Status Akurasi: {status}\n\nFormula: ((C-spike terukur - C-awal) / C-ditambahkan) × 100%")

st.markdown("""
---
<div style='text-align:center;color:gray;font-size:13px;line-height:1.5;'>
Smart Chemistry Analysis — Streamlit • Made with ❤
</div>
""", unsafe_allow_html=True)
