import streamlit as st
from scipy.optimize import brentq

# Funkcja obliczająca netto
def calculate_net_old(P, C, ZUS, target_net=6350.00, tax_rate=0.12, tax_deduction=300, health_rate=0.09):
    base = P - C - ZUS
    tax = tax_rate * base - tax_deduction
    health = health_rate * base
    net = base - tax - health
    return net - target_net

# Funkcja obliczająca składki ZUS
def calculate_ZUS(social_rate, ZUS_base):
    emerytalne = 0.1952 * ZUS_base
    rentowe = 0.08 * ZUS_base
    chorobowe = 0.0245 * ZUS_base
    wypadkowe = 0.0167 * ZUS_base
    zdrowotne = 0.09 * ZUS_base

    total_ZUS = emerytalne + rentowe + chorobowe + wypadkowe + zdrowotne
    return {
        'Emerytalne': emerytalne,
        'Rentowe': rentowe,
        'Chorobowe': chorobowe,
        'Wypadkowe': wypadkowe,
        'Zdrowotne': zdrowotne,
        'Łączny ZUS': total_ZUS
    }

# Parametry
C_example = 252.15    # Koszty
ZUS_example = 1485.31 # ZUS (społeczne)
target_net = 6350.00  # Docelowa kwota "na rękę"
P_min, P_max = 9000, 10000

# Streamlit UI
st.title("Kalkulator Przychodu na Rękę")

# Wybór ZUS i kosztów
selected_ZUS_option = st.radio(
    "Wybierz ZUS:",
    ["Bez chorobowego (2025)", "Z chorobowym (2025)"],
    index=0
)

# Ustalanie wartości ZUS w zależności od wyboru
if selected_ZUS_option == "Bez chorobowego (2025)":
    ZUS_value = 1646.47
else:
    ZUS_value = 1773.96

# Koszty - interaktywne pole
koszty = st.number_input("Koszty (C):", min_value=0.0, value=C_example, step=1.0)

# Obliczanie przychodu
P_solution = brentq(calculate_net_old, P_min, P_max, args=(koszty, ZUS_value, target_net))
st.subheader(f"Wyliczony przychód: {P_solution:.2f} zł")

# Obliczenie składek ZUS
zus_details = calculate_ZUS(ZUS_value, ZUS_value)
st.write("**Szczegóły obliczeń ZUS:**")
st.write(f"Emerytalne: {zus_details['Emerytalne']:.2f} zł")
st.write(f"Rentowe: {zus_details['Rentowe']:.2f} zł")
st.write(f"Chorobowe: {zus_details['Chorobowe']:.2f} zł")
st.write(f"Wypadkowe: {zus_details['Wypadkowe']:.2f} zł")
st.write(f"Zdrowotne: {zus_details['Zdrowotne']:.2f} zł")
st.write(f"Łączny ZUS: {zus_details['Łączny ZUS']:.2f} zł")

# Przyciski resetujące
if st.button("Resetuj ustawienia"):
    st.session_state.clear()
    st.experimental_rerun()

