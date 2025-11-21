from datetime import datetime

# Taux d'emprunt moyens historiques (approx. Banque de France)
# Pour une implémentation réelle, ces données devraient venir d'une DB ou API
HISTORICAL_RATES = {
    2019: 1.20,
    2020: 1.20,
    2021: 1.10,
    2022: 1.50,
    2023: 3.00,
    2024: 3.80,
    2025: 3.50  # Taux actuel estimé
}

CURRENT_RATE = HISTORICAL_RATES[2025]

def get_historical_rate(date_transaction: datetime) -> float:
    """Récupère le taux historique pour une date donnée."""
    year = date_transaction.year
    # Fallback sur l'année la plus proche si non trouvée
    if year not in HISTORICAL_RATES:
        if year < min(HISTORICAL_RATES.keys()):
            return HISTORICAL_RATES[min(HISTORICAL_RATES.keys())]
        else:
            return CURRENT_RATE
    return HISTORICAL_RATES[year]

def calculate_adjusted_price(price: float, date_transaction: datetime) -> float:
    """
    Calcule le prix ajusté en fonction de l'évolution des taux d'emprunt.
    Formule: Prix Ajusté = Prix * (1 - (Delta Taux * 0.10))
    """
    historical_rate = get_historical_rate(date_transaction)
    delta_rate = CURRENT_RATE - historical_rate
    
    # Impact: +1% de taux = -10% de pouvoir d'achat
    adjustment_coeff = 1 - (delta_rate * 0.10)
    
    return price * adjustment_coeff
