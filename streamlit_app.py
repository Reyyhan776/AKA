import streamlit as st
import time
import random

# =========================
# STRUKTUR MULTI LINKED LIST
# =========================

class Child:
    def __init__(self, data):
        self.data = data
        self.next = None

class Parent:
    def __init__(self):
        self.first_child = None
        self.next = None


# =========================
# MEMBANGUN MULTI LINKED LIST
# =========================

def build_multi_linked_list(num_parent, num_child):
    head = Parent()
    current_parent = head

    value = 1
    for i in range(num_parent):
        first_child = Child(value)
        current_child = first_child
        value += 1

        for j in range(1, num_child):
            new_child = Child(value)
            current_child.next = new_child
            current_child = new_child
            value += 1

        current_parent.first_child = first_child

        if i < num_parent - 1:
            new_parent = Parent()
            current_parent.next = new_parent
            current_parent = new_parent

    return head


# =========================
# PENCARIAN ITERATIF
# =========================

def search_iterative(head, key):
    p = head
    while p is not None:
        c = p.first_child
        while c is not None:
            if c.data == key:
                return True
            c = c.next
        p = p.next
    return False


# =========================
# PENCARIAN REKURSIF
# =========================

def search_child_recursive(c, key):
    if c is None:
        return False
    if c.data == key:
        return True
    return search_child_recursive(c.next, key)

def search_recursive(p, key):
    if p is None:
        return False
    if search_child_recursive(p.first_child, key):
        return True
    return search_recursive(p.next, key)


# =========================
# STREAMLIT UI
# =========================

st.title("Analisis Kompleksitas Algoritma")
st.subheader("Pencarian Data pada Multi Linked List")
st.write("Perbandingan Algoritma Iteratif vs Rekursif")

st.sidebar.header("Parameter Data")

num_parent = st.sidebar.number_input(
    "Jumlah Parent",
    min_value=1,
    max_value=500,
    value=10
)

num_child = st.sidebar.number_input(
    "Jumlah Child per Parent",
    min_value=1,
    max_value=200,
    value=10
)

iterations = st.sidebar.number_input(
    "Jumlah Pengulangan Eksperimen",
    min_value=1,
    max_value=50,
    value=10
)

if st.sidebar.button("Jalankan Analisis"):
    st.info("Membangun Multi Linked List...")
    head = build_multi_linked_list(num_parent, num_child)

    max_value = num_parent * num_child
    key = random.randint(1, max_value)

    iter_times = []
    rec_times = []

    st.info("Menjalankan eksperimen...")

    for i in range(iterations):
        # Iteratif
        start = time.perf_counter()
        search_iterative(head, key)
        end = time.perf_counter()
        iter_times.append(end - start)

        # Rekursif
        start = time.perf_counter()
        search_recursive(head, key)
        end = time.perf_counter()
        rec_times.append(end - start)

    avg_iter = sum(iter_times) / iterations
    avg_rec = sum(rec_times) / iterations

    st.success("Eksperimen selesai!")

    st.subheader("Hasil Running Time")
    st.write(f"**Rata-rata Iteratif:** {avg_iter:.6f} detik")
    st.write(f"**Rata-rata Rekursif:** {avg_rec:.6f} detik")

    st.subheader("Grafik Perbandingan Running Time")
    st.line_chart({
        "Iteratif": iter_times,
        "Rekursif": rec_times
    })

    st.subheader("Analisis Singkat")
    if avg_iter < avg_rec:
        st.write(
            "Algoritma iteratif menunjukkan performa yang lebih baik "
            "dibandingkan algoritma rekursif karena tidak memiliki overhead "
            "pemanggilan fungsi dan penggunaan stack."
        )
    else:
        st.write(
            "Algoritma rekursif memiliki running time yang sebanding, "
            "namun overhead stack dapat memengaruhi performa pada ukuran data besar."
        )

st.markdown("---")
st.caption("Tugas Besar Analisis Kompleksitas Algoritma")
