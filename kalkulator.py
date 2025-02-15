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
ZUS_example = st.number_input("ZUS:", min_value=0.0, value=1485.31, step=1.0)

# Pole do wyboru docelowej kwoty netto
target_net = st.number_input("Docelowa kwota netto:", min_value=0.0, value=6350.00, step=1.0)

# Zakres poszukiwań przychodu
P_min, P_max = 9000, 10000

# Obliczenia
P_solution_1 = brentq(calculate_net_old, P_min, P_max, args=(C_example, ZUS_example, target_net))
P_solution_2 = brentq(calculate_net_old, P_min, P_max, args=(C_example, 1773.96, target_net))

# Wyświetlanie wyników
st.write(f"Rozwiązanie: Przychód nowy ZUS bez chorobowego = {P_solution_1:.2f} zł")
st.write(f"Rozwiązanie: Przychód nowy ZUS z chorobowym = {P_solution_2:.2f} zł")
