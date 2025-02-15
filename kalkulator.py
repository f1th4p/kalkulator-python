import streamlit as st
from scipy.optimize import brentq

# Funkcja obliczająca przychód
def calculate_net_old(P, C, ZUS, target_net=6350.00, tax_rate=0.12, tax_deduction=300, health_rate=0.09):
    base = P - C - ZUS
    tax = tax_rate * base - tax_deduction
    health = health_rate * base
    net = base - tax - health
    return net - target_net

# Funkcja resetująca ustawienia
def reset_settings():
    st.session_state["koszty"] = 263.22
    st.session_state["zus_year"] = "2025"
    st.session_state["zus_type"] = "Bez chorobowego"
    st.session_state["target_net"] = 6350.00

# Inicjalizacja wartości domyślnych w session_state (jeśli jeszcze nie istnieją)
if "koszty" not in st.session_state:
    reset_settings()

# Tytuł strony
st.title("Kalkulator przychodu na podstawie wynagrodzenia netto")

# --- Sekcja obliczeń przed formularzem ---
P_min, P_max = 9000, 10000

ZUS_values = {
    ("2025", "Bez chorobowego"): 1646.47,
    ("2025", "Z chorobowym"): 1773.96,
    ("2024", "Bez chorobowego"): 1485.31,
    ("2024", "Z chorobowym"): 1600.45
}

ZUS_value = ZUS_values[(st.session_state["zus_year"], st.session_state["zus_type"])]

P_solution = brentq(calculate_net_old, P_min, P_max, args=(st.session_state["koszty"], ZUS_value, st.session_state["target_net"]))

# Wyświetlenie wyniku u góry
st.write(f"### 📌 Rozwiązanie: Przychód dla {st.session_state['zus_year']} - {st.session_state['zus_type']} = **{P_solution:.2f} zł**")

# --- Formularz ---
col1, col2 = st.columns(2)

with col1:
    st.session_state["koszty"] = st.number_input("Koszty (C):", min_value=0.0, value=st.session_state["koszty"], step=1.0)

with col2:
    st.session_state["target_net"] = st.number_input("Docelowa kwota netto:", min_value=0.0, value=st.session_state["target_net"], step=1.0)

# Wybór roku ZUS
st.session_state["zus_year"] = st.radio("Wybierz rok ZUS:", options=["2025", "2024"], horizontal=True)

# Wybór rodzaju ZUS
st.session_state["zus_type"] = st.radio("Rodzaj ZUS:", options=["Bez chorobowego", "Z chorobowym"])

# Guzik resetowania
if st.button("Resetuj ustawienia"):
    reset_settings()
    st.experimental_rerun()
