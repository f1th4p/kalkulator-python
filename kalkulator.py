import streamlit as st
from scipy.optimize import brentq

def calculate_net_old(P, C, ZUS, target_net=6350.00, tax_rate=0.12, tax_deduction=300, health_rate=0.09):
    """
    Uproszczony model obliczeń:
    
      Przychód: P
      Koszty: C
      Społeczne: ZUS
      
      Dochód (podstawa) = P - C - ZUS
      Podatek = 0.12 * (P - C - ZUS) - 300
      Zdrowotna = 0.09 * (P - C - ZUS)
      Na rękę = (P - C - ZUS) - Podatek - Zdrowotna
      
    Funkcja zwraca różnicę między uzyskanym wynagrodzeniem netto a docelową kwotą (target_net).
    """
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

# Inicjalizacja stanu aplikacji
if "koszty" not in st.session_state:
    reset_settings()

# Tytuł strony
st.title("Kalkulator przychodu na podstawie wynagrodzenia netto")

# Zakres poszukiwań przychodu
P_min, P_max = 9000, 10000

# Obliczenia wyniku przed formularzem
ZUS_year = st.session_state["zus_year"]
ZUS_type = st.session_state["zus_type"]
ZUS_value = 1646.47 if (ZUS_year == "2025" and ZUS_type == "Bez chorobowego") else 1773.96 if ZUS_year == "2025" else 1485.31 if ZUS_type == "Bez chorobowego" else 1600.45
P_solution = brentq(calculate_net_old, P_min, P_max, args=(st.session_state["koszty"], ZUS_value, st.session_state["target_net"]))

# Wyświetlenie wyniku na samej górze
st.write(f"### 📌 Rozwiązanie: Przychód dla {ZUS_year} - {ZUS_type} = **{P_solution:.2f} zł**")

# Przycisk do resetowania
if st.button("Resetuj ustawienia"):
    reset_settings()

# Pola do wprowadzenia danych
st.session_state["koszty"] = st.number_input("Koszty (C):", min_value=0.0, value=st.session_state["koszty"], step=1.0, key="koszty")
st.session_state["target_net"] = st.number_input("Docelowa kwota netto:", min_value=0.0, value=st.session_state["target_net"], step=1.0, key="target_net")

# Wybór roku ZUS – guziki jednokrotnego wyboru
st.session_state["zus_year"] = st.radio("Wybierz rok ZUS:", options=["2025", "2024"], index=0 if st.session_state["zus_year"] == "2025" else 1, horizontal=True, key="zus_year")

# Wybór rodzaju ZUS
st.session_state["zus_type"] = st.radio("Rodzaj ZUS:", options=["Bez chorobowego", "Z chorobowym"], index=0 if st.session_state["zus_type"] == "Bez chorobowego" else 1, key="zus_type")
