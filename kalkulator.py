import streamlit as st
from scipy.optimize import brentq

# Definicja progów podatkowych
TAX_BRACKET = 120000
TAX_RATE_LOW = 0.12
TAX_RATE_HIGH = 0.32
TAX_DEDUCTION = 300

# Funkcja obliczeniowa
def calculate_net_details(P, C, ZUS, target_net, health_rate=0.09):
    base = P - C - ZUS
    if base <= TAX_BRACKET:
        tax = TAX_RATE_LOW * base - TAX_DEDUCTION
        tax_bracket_used = f"12% dla całej kwoty"
    else:
        tax = (TAX_RATE_LOW * TAX_BRACKET) + (TAX_RATE_HIGH * (base - TAX_BRACKET)) - TAX_DEDUCTION
        tax_bracket_used = f"12% do {TAX_BRACKET} zł, 32% dla nadwyżki"

    health = health_rate * base
    net = base - tax - health

    return {
        "Przychód": P,
        "Dochód podlegający opodatkowaniu": base,
        "Podatek dochodowy": tax,
        "Prog podatkowy": tax_bracket_used,
        "Składka zdrowotna": health,
        "Na rękę": net,
        "Różnica do celu": net - target_net
    }

# Funkcja resetująca ustawienia
def reset_settings():
    st.session_state["koszty"] = 263.22
    st.session_state["target_net"] = 6350.00
    st.session_state["zus_year"] = "2025"
    st.session_state["zus_type"] = "Bez chorobowego"
    st.experimental_rerun()

# Inicjalizacja wartości domyślnych
if "koszty" not in st.session_state:
    reset_settings()

st.title("Kalkulator przychodu na podstawie wynagrodzenia netto")

# --- Słownik wartości ZUS ---
ZUS_values = {
    ("2025", "Bez chorobowego"): 1646.47,
    ("2025", "Z chorobowym"): 1773.96,
    ("2024", "Bez chorobowego"): 1485.31,
    ("2024", "Z chorobowym"): 1600.45
}

# Pobranie wartości ZUS na podstawie wyboru
ZUS_value = ZUS_values[(st.session_state["zus_year"], st.session_state["zus_type"])]

# Zakres poszukiwań przychodu – zwiększony, aby uniknąć błędu
P_min, P_max = 5000, 20000

# Sprawdzenie, czy funkcja zmienia znak w przedziale
F_min = calculate_net_details(P_min, st.session_state["koszty"], ZUS_value, st.session_state["target_net"])["Różnica do celu"]
F_max = calculate_net_details(P_max, st.session_state["koszty"], ZUS_value, st.session_state["target_net"])["Różnica do celu"]

if F_min * F_max > 0:
    st.error("❌ Błąd: Nie można znaleźć rozwiązania w podanym zakresie przychodów. Spróbuj zwiększyć zakres.")
    st.write(f"🔍 F({P_min}) = {F_min:.2f}, F({P_max}) = {F_max:.2f}")
else:
    # Znalezienie rozwiązania
    P_solution = brentq(
        lambda P: calculate_net_details(P, st.session_state["koszty"], ZUS_value, st.session_state["target_net"])["Różnica do celu"],
        P_min, P_max
    )

    # --- Wynik główny ---
    st.write(f"### 📌 Rozwiązanie: Przychód dla {st.session_state['zus_year']} - {st.session_state['zus_type']} = **{P_solution:.2f} zł**")

    # --- Szczegółowe obliczenia ---
    details = calculate_net_details(P_solution, st.session_state["koszty"], ZUS_value, st.session_state["target_net"])

    st.subheader("📊 Szczegóły obliczeń:")
    st.write(f"**Przychód całkowity:** {details['Przychód']:.2f} zł")
    st.write(f"**Dochód podlegający opodatkowaniu:** {details['Dochód podlegający opodatkowaniu']:.2f} zł")
    st.write(f"**Podatek dochodowy:** {details['Podatek dochodowy']:.2f} zł")
    st.write(f"**Prog podatkowy zastosowany:** {details['Prog podatkowy']}")
    st.write(f"**Składka zdrowotna:** {details['Składka zdrowotna']:.2f} zł")
    st.write(f"**Na rękę:** {details['Na rękę']:.2f} zł")

# --- Formularz edycji parametrów ---
col1, col2 = st.columns(2)

with col1:
    st.session_state["koszty"] = st.number_input("Koszty (C):", min_value=0.0, value=st.session_state["koszty"], step=1.0)

with col2:
    st.session_state["target_net"] = st.number_input("Docelowa kwota netto:", min_value=0.0, value=st.session_state["target_net"], step=1.0)

# **Radio Buttony**
st.session_state["zus_year"] = st.radio("Wybierz rok ZUS:", options=["2025", "2024"], index=["2025", "2024"].index(st.session_state["zus_year"]))
st.session_state["zus_type"] = st.radio("Rodzaj ZUS:", options=["Bez chorobowego", "Z chorobowym"], index=["Bez chorobowego", "Z chorobowym"].index(st.session_state["zus_type"]))

# Guzik resetowania
if st.button("Resetuj ustawienia"):
    reset_settings()
