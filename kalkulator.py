import streamlit as st
from scipy.optimize import brentq

# Definicja progów podatkowych
TAX_BRACKET = 120000
TAX_RATE_LOW = 0.12
TAX_RATE_HIGH = 0.32
TAX_DEDUCTION = 300

# Funkcja obliczeniowa
def calculate_net_details_annual(P, C, ZUS, ZUS_breakdown, target_net, health_rate=0.09):
    # Obliczenia dla jednego miesiąca
    monthly_base = P - C - ZUS
    # Roczny dochód przed opodatkowaniem
    annual_base = monthly_base * 12  
    
    # Obliczenia kwartalne
    quarterly_base = monthly_base * 3  
    
    # Jeśli w kwartale dochód nie przekracza 30 000 zł, podatek wynosi 0
    if quarterly_base <= 30000:
        quarterly_tax = 0
        tax_low = 0
        tax_high = 0
    else:
        # Za pierwsze 30 000 zł stosujemy 12%
        tax_low = 0.12 * 30000  
        # Dla nadwyżki powyżej 30 000 zł stosujemy 32%
        tax_high = 0.32 * (quarterly_base - 30000)
        # Uśrednione odliczenie podatkowe kwartalne (300 zł rocznie = 75 zł na kwartał)
        quarterly_tax = tax_low + tax_high - (300 / 4)
        # Zapewnienie, że podatek nie jest ujemny
        if quarterly_tax < 0:
            quarterly_tax = 0

    # Roczny podatek to suma podatków za 4 kwartały
    annual_tax = quarterly_tax * 4
    
    # Roczna składka zdrowotna
    health = health_rate * annual_base  
    # Wyliczenie miesięcznego "na rękę" po odliczeniu podatku i zdrowotki
    net = (annual_base - annual_tax - health) / 12  

    return {
        "Przychód": round(P, 2),
        "Roczny dochód podlegający opodatkowaniu": round(annual_base, 2),
        "Podatek dochodowy 12% (kwartalnie)": round(tax_low, 2),
        "Podatek dochodowy 32% (kwartalnie)": round(tax_high, 2),
        "Łączny podatek (rocznie)": round(annual_tax, 2),
        "Składka zdrowotna (rocznie)": round(health, 2),
        "Składki ZUS": round(ZUS, 2),
        "ZUS - Emerytalne": round(ZUS_breakdown['Emerytalne'], 2),
        "ZUS - Rentowe": round(ZUS_breakdown['Rentowe'], 2),
        "ZUS - Chorobowe": round(ZUS_breakdown['Chorobowe'], 2),
        "ZUS - Wypadkowe": round(ZUS_breakdown['Wypadkowe'], 2),
        "ZUS - FP": round(ZUS_breakdown['FP'], 2),
        "Na rękę (miesiącznie)": round(net, 2),
        "Różnica do celu": round(net - target_net, 2)
    }

    
def calculate_net_details(P, C, ZUS, ZUS_breakdown, target_net, health_rate=0.09):
    base = P - C - ZUS
    annual_base = base

    if annual_base <= TAX_BRACKET:
        tax_low = TAX_RATE_LOW * annual_base
        tax_high = 0
    else:
        tax_low = TAX_RATE_LOW * TAX_BRACKET
        tax_high = TAX_RATE_HIGH * (annual_base - TAX_BRACKET)
    
    tax = tax_low + tax_high - TAX_DEDUCTION
    health = health_rate * annual_base  # Roczna składka zdrowotna
    net = annual_base - tax - health  # Przeliczenie na miesiąc

    return {
        "Przychód": round(P, 2),
        "Dochód podlegający opodatkowaniu": round(annual_base, 2),
        "Podatek dochodowy 12%": round(tax_low, 2),
        "Podatek dochodowy 32%": round(tax_high, 2),
        "Łączny podatek": round(tax, 2),
        "Składka zdrowotna": round(health, 2),
        "Składki ZUS": round(ZUS, 2),
        "ZUS - Emerytalne": round(ZUS_breakdown["Emerytalne"], 2),
        "ZUS - Rentowe": round(ZUS_breakdown["Rentowe"], 2),
        "ZUS - Chorobowe": round(ZUS_breakdown["Chorobowe"], 2),
        "ZUS - Wypadkowe": round(ZUS_breakdown["Wypadkowe"], 2),
        "ZUS - FP": round(ZUS_breakdown["FP"], 2),
        "Na rękę": round(net, 2),
        "Różnica do celu": round(net - target_net, 2)
    }

# Funkcja resetująca ustawienia
def reset_settings():
    st.session_state["koszty"] = 263.22
    st.session_state["target_net"] = 6350.00
    st.session_state["zus_year"] = "2025"
    st.session_state["zus_type"] = "Bez chorobowego"
    # st.rerun()

# Inicjalizacja wartości domyślnych
if "koszty" not in st.session_state:
    reset_settings()

st.title("Kalkulator przychodu na podstawie wynagrodzenia netto")

# --- Słownik wartości ZUS ---
ZUS_values = {
    ("2025", "Bez chorobowego"): (1646.47, {"Emerytalne": 812.00, "Rentowe": 332.00, "Chorobowe": 0.00, "Wypadkowe": 67.00, "FP": 435.47}),
    ("2025", "Z chorobowym"): (1773.96, {"Emerytalne": 812.00, "Rentowe": 332.00, "Chorobowe": 127.49, "Wypadkowe": 67.00, "FP": 435.47}),
    ("2024", "Bez chorobowego"): (1485.31, {"Emerytalne": 738.00, "Rentowe": 298.00, "Chorobowe": 0.00, "Wypadkowe": 61.00, "FP": 388.31}),
    ("2024", "Z chorobowym"): (1600.45, {"Emerytalne": 738.00, "Rentowe": 298.00, "Chorobowe": 115.14, "Wypadkowe": 61.00, "FP": 388.31})
}

# --- Formularz edycji parametrów ---
col1, col2 = st.columns(2)

with col1:
    st.session_state["zus_year"] = st.radio("Wybierz rok ZUS:", options=["2025", "2024"], index=["2025", "2024"].index(st.session_state["zus_year"]))

with col2:
    st.session_state["zus_type"] = st.radio("Rodzaj ZUS:", options=["Bez chorobowego", "Z chorobowym"], index=["Bez chorobowego", "Z chorobowym"].index(st.session_state["zus_type"]))

# Pobranie wartości ZUS na podstawie wyboru
ZUS_value, ZUS_breakdown = ZUS_values[(st.session_state["zus_year"], st.session_state["zus_type"])]

# --- Pozostałe ustawienia ---
col3, col4 = st.columns(2)

with col3:
    st.session_state["koszty"] = st.number_input("Koszty (C):", min_value=0.0, value=st.session_state["koszty"], step=1.0)

with col4:
    st.session_state["target_net"] = st.number_input("Docelowa kwota netto:", min_value=0.0, value=st.session_state["target_net"], step=1.0)

if st.button("Resetuj ustawienia"):
    reset_settings()

# Zakres poszukiwań przychodu – zwiększony, aby uniknąć błędu
P_min, P_max = 5000, 20000

F_min = calculate_net_details(P_min, st.session_state["koszty"], ZUS_value, ZUS_breakdown, st.session_state["target_net"])['Różnica do celu']
F_max = calculate_net_details(P_max, st.session_state["koszty"], ZUS_value, ZUS_breakdown, st.session_state["target_net"])['Różnica do celu']

if F_min * F_max > 0:
    st.error("❌ Błąd: Nie można znaleźć rozwiązania w podanym zakresie przychodów. Spróbuj zwiększyć zakres.")
else:
    P_solution = brentq(
        lambda P: calculate_net_details(P, st.session_state["koszty"], ZUS_value, ZUS_breakdown, st.session_state["target_net"])['Różnica do celu'],
        P_min, P_max
    )

    details = calculate_net_details(P_solution, st.session_state["koszty"], ZUS_value, ZUS_breakdown, st.session_state["target_net"])
    
    st.subheader("📌 Podsumowanie:")
    st.write(f"**Przychód dla {st.session_state['zus_year']} - {st.session_state['zus_type']} = {P_solution:.2f} zł**")
    st.write(details)

F_min = calculate_net_details_annual(P_min, st.session_state["koszty"], ZUS_value, ZUS_breakdown, st.session_state["target_net"])['Różnica do celu']
F_max = calculate_net_details_annual(P_max, st.session_state["koszty"], ZUS_value, ZUS_breakdown, st.session_state["target_net"])['Różnica do celu']

if F_min * F_max > 0:
    st.error("❌ Błąd: Nie można znaleźć rozwiązania w podanym zakresie przychodów. Spróbuj zwiększyć zakres.")
else:
    P_solution = brentq(
        lambda P: calculate_net_details_annual(P, st.session_state["koszty"], ZUS_value, ZUS_breakdown, st.session_state["target_net"])['Różnica do celu'],
        P_min, P_max
    )

    details = calculate_net_details_annual(P_solution, st.session_state["koszty"], ZUS_value, ZUS_breakdown, st.session_state["target_net"])
    
    # st.subheader("📌 Podsumowanie:")
    # st.write(f"**Przychód dla {st.session_state['zus_year']} - {st.session_state['zus_type']} = {P_solution:.2f} zł**")
    # st.write(details)