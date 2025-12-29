import streamlit as st
import time

class Child:
    def __init__(self, data):
        self.data = data
        self.next = None

class Parent:
    def __init__(self):
        self.first_child = None
        self.next = None

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

st.title("Analisis Kompleksitas Algoritma")
st.subheader("Pencarian Data pada Multi Linked List")
st.write("Perbandingan Algoritma Iteratif vs Rekursif")

st.sidebar.header("Parameter Eksperimen")

num_parent = st.sidebar.number_input(
    "Jumlah Parent", min_value=1, max_value=500, value=10
)

num_child = st.sidebar.number_input(
    "Jumlah Child per Parent", min_value=1, max_value=200, value=10
)

iterations = st.sidebar.number_input(
    "Jumlah Pengulangan Eksperimen", min_value=1, max_value=50, value=10
)

position = st.sidebar.selectbox(
    "Posisi Data yang Dicari",
    ("Paling Awal (Best Case)", "Paling Akhir (Worst Case)")
)

if st.sidebar.button("Jalankan Analisis"):
    head = build_multi_linked_list(num_parent, num_child)

    if position == "Paling Awal (Best Case)":
        key = 1
    else:
        key = num_parent * num_child

    iter_times = []
    rec_times = []

    for _ in range(iterations):
        start = time.perf_counter()
        search_iterative(head, key)
        end = time.perf_counter()
        iter_times.append(end - start)

        start = time.perf_counter()
        search_recursive(head, key)
        end = time.perf_counter()
        rec_times.append(end - start)

    avg_iter = sum(iter_times) / iterations
    avg_rec = sum(rec_times) / iterations

    st.subheader("Hasil Running Time (Rata-rata)")
    st.write(f"Iteratif : {avg_iter:.6f} detik")
    st.write(f"Rekursif : {avg_rec:.6f} detik")

    st.subheader("Grafik Perbandingan Running Time")
    st.line_chart({
        "Iteratif": iter_times,
        "Rekursif": rec_times
    })

    st.subheader("Analisis")
    if position == "Paling Awal (Best Case)":
        st.write(
            "Data berada pada posisi paling awal sehingga pencarian langsung berhenti. "
            "Kedua algoritma memiliki kompleksitas waktu O(1)."
        )
    else:
        st.write(
            "Data berada pada posisi paling akhir sehingga seluruh parent dan child "
            "harus ditelusuri. Kedua algoritma memiliki kompleksitas waktu O(n × m), "
            "namun algoritma iteratif lebih efisien secara praktis."
        )

st.markdown("---")
st.caption("Tugas Besar Analisis Kompleksitas Algoritma")
