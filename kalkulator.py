# Automatyczna instalacja wymaganych pakietów (po otwarciu notebooka)
import sys
import subprocess

# Instalacja pakietów, jeśli nie są zainstalowane
packages = ['scipy', 'numpy']

for package in packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print("Pakiety zostały zainstalowane.")

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
    # print(f"Debug: P={P:.2f}, C={C:.2f}, ZUS={ZUS:.2f}, base={base:.2f}, tax={tax:.2f}, health={health:.2f}, net={net:.2f}")
    return net - target_net

# Przykładowe parametry z zeszłego roku:
C_example = 252.15    # Koszty
ZUS_example = 1485.31 # Społeczne (składki społeczne)
target_net = 6350.00  # Docelowa kwota "na rękę"

# Zakres poszukiwań przychodu – dobierzemy taki, aby zawierał wartość z przykładu (9285 zł)
P_min, P_max = 9000, 10000

# P_solution = brentq(calculate_net_old, P_min, P_max, args=(C_example, ZUS_example, target_net))
# print(f"Rozwiązanie: Przychód = {P_solution:.2f} zł")

P_solution = brentq(calculate_net_old, P_min, P_max, args=(263.22, 1646.47, target_net))
print(f"Rozwiązanie: Przychód nowy ZUS bez chorobowego = {P_solution:.2f} zł")

P_solution = brentq(calculate_net_old, P_min, P_max, args=(263.22, 1773.96, target_net))
print(f"Rozwiązanie: Przychód nowy ZUS z chorobowym = {P_solution:.2f} zł")
