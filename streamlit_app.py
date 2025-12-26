import streamlit as st
import sys
from io import StringIO
from contextlib import redirect_stdout
import time
import matplotlib.pyplot as plt 

st.set_page_config(page_title="Harmonic Series", layout="centered")

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}
a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: black;
color: white;
text-align: center;
z-index: 100;
}
</style>
"jangan lupa mampir ke github.com/SidikYaeger"
<div class="footer">
<p>~Made by Ravananda & Zhafir~</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)

st.title("🧮 Kalkulator Deret Harmonik: Iteratif VS Rekursif")
st.write("Menghitung jumlah deret: 1/1 + 1/2 + ... + 1/n")

def rekursif_visual(n):
    if n == 1:
        print("1/1", end="")
        return 1.0
    x = rekursif_visual(n - 1)
    print(" + 1/" + str(n), end="")
    return x + (1.0 / n)

def iteratif_visual(n):
    total = 0.0
    for i in range(1, n + 1):
        print("1/" + str(i), end="")
        if i < n:
            print(" + ", end="")
        total = total + (1.0 / i)
    return total

def iteratif_pure(n):
    total = 0.0
    for i in range(1, n + 1):
        total = total + (1.0 / i)
    return total

def rekursif_pure(n):
    if n == 1:
        return 1.0
    return (1.0 / n) + rekursif_pure(n - 1)

n = st.number_input("Masukkan nilai n:", min_value=1, step=1, value=5)

if st.button("Hitung & Analisis", type="primary"):
    

    st.divider()
    st.header("1. Visualisasi Proses (Single Run)")

    st.subheader("Metode Iteratif")
    buffer_iter = StringIO()
    with redirect_stdout(buffer_iter):
        res_iter = iteratif_visual(n)
    teks_iter = buffer_iter.getvalue()
    st.code(teks_iter, language="text")
    st.success(f"Hasil: {res_iter}")

    st.subheader("Metode Rekursif")
    limit_aman = 990 
    
    if n > limit_aman:
        st.warning(f"⚠️ Nilai n terlalu besar untuk visualisasi Rekursif (batas aman: {limit_aman}).")
        run_recursive = False
    else:
        run_recursive = True
        buffer_rec = StringIO()
        with redirect_stdout(buffer_rec):
            res_rec = rekursif_visual(n)
        teks_rec = buffer_rec.getvalue()
        st.code(teks_rec, language="text")
        st.success(f"Hasil: {res_rec}")

    st.divider()
    st.header("2. Benchmark Rata-rata (1000x Percobaan)")
    st.caption("Menguji performa murni algoritma (tanpa proses print) untuk hasil yang lebih akurat.")

    progress_bar = st.progress(0)
    status_text = st.empty()
    
    NUM_TRIALS = 1000

    status_text.text("Menguji Iteratif...")
    start_iter = time.perf_counter()
    for _ in range(NUM_TRIALS):
        iteratif_pure(n)
    end_iter = time.perf_counter()

    avg_iteratif = ((end_iter - start_iter) / NUM_TRIALS) * 1000
    progress_bar.progress(50)

    avg_rekursif = None
    if run_recursive:
        status_text.text("Menguji Rekursif...")

        sys.setrecursionlimit(max(2000, n + 500)) 
        
        try:
            start_rec = time.perf_counter()
            for _ in range(NUM_TRIALS):
                rekursif_pure(n)
            end_rec = time.perf_counter()
            
            avg_rekursif = ((end_rec - start_rec) / NUM_TRIALS) * 1000
        except RecursionError:
            st.error("Terjadi Stack Overflow saat benchmark rekursif.")
            avg_rekursif = None
    else:
        status_text.text("Rekursif dilewati (Limit Exceeded)")

    progress_bar.progress(100)
    status_text.empty()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Rata-rata Waktu Iteratif", value=f"{avg_iteratif:.6f} ms")
    
    with col2:
        if avg_rekursif is not None:
            delta_val = avg_iteratif - avg_rekursif
            st.metric(label="Rata-rata Waktu Rekursif", value=f"{avg_rekursif:.6f} ms", delta=f"{delta_val:.6f} ms")
        else:
            st.metric(label="Rata-rata Waktu Rekursif", value="Gagal/Dilewati")

    st.write("### Grafik Perbandingan Rata-rata")
    
    kategori = ['Iteratif', 'Rekursif']
    val_rec_plot = avg_rekursif if avg_rekursif is not None else 0
    waktu = [avg_iteratif, val_rec_plot]
    
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(kategori, waktu, color=['#3498db', '#e74c3c'])
    
    ax.set_ylabel('Rata-rata Waktu (ms)')
    ax.set_title(f'Benchmark 1000x Iterasi (Input n={n})')

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.6f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), 
                    textcoords="offset points",
                    ha='center', va='bottom')
    
    st.pyplot(fig)

    if avg_rekursif is not None:
        if avg_iteratif < avg_rekursif:
            st.success("🏆 **Kesimpulan:** Algoritma **Iteratif** lebih cepat secara rata-rata.")
        else:
            st.success("🏆 **Kesimpulan:** Algoritma **Rekursif** lebih cepat secara rata-rata.")
