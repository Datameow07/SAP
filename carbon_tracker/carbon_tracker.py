# carbon_tracker.py

EMISSION_FACTOR = 0.150  # kg CO₂ per km
TRADITIONAL_DISTANCE = 6.0  # km per order

def calculate_co2(distance_km):
    """Return CO2 emitted for a given distance."""
    return round(distance_km * EMISSION_FACTOR, 3)

def calculate_savings(actual_distance_km, traditional_km=TRADITIONAL_DISTANCE):
    """Compare actual vs traditional delivery emissions."""
    actual = calculate_co2(actual_distance_km)
    traditional = calculate_co2(traditional_km)
    saved = round(traditional - actual, 3)
    return actual, saved
