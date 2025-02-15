import streamlit as st
from scipy.optimize import brentq

def calculate_net_old(P, C, ZUS, target_net=6350.00, tax_rate=0.12, tax_deduction=300, health_rate=0.09):
    """
    Uproszczony model obliczeń (model z zeszłego roku):
    
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

# Tytuł strony
st.title("Kalkulator przychodu na podstawie wynagrodzenia netto")

# Pola do wprowadzenia danych
C_example = st.number_input("Koszty (C):", min_value=0.0, value=263.22, step=1.0)

# Wybór ZUS (2024 vs 2025)
ZUS_options = {
    '2025 - ZUS bez chorobowego': 1646.47,
    '2025 - ZUS z chorobowym': 1773.96,
    '2024 - ZUS bez chorobowego': 1485.31,
    '2024 - ZUS z chorobowym': 1600.45
}

# Wybór ZUS z listy
ZUS_example = st.selectbox("Wybierz ZUS (2024 lub 2025):", options=list(ZUS_options.keys()), index=0)
ZUS_value = ZUS_options[ZUS_example]

# Pole do wyboru docelowej kwoty netto
target_net = st.number_input("Docelowa kwota netto:", min_value=0.0, value=6350.00, step=1.0)

# Zakres poszukiwań przychodu
P_min, P_max = 9000, 10000

# Obliczenia
P_solution_1 = brentq(calculate_net_old, P_min, P_max, args=(C_example, ZUS_value, target_net))

# Wyświetlanie wyników
st.write(f"Rozwiązanie: Przychód nowy ZUS bez chorobowego = {P_solution_1:.2f} zł")
