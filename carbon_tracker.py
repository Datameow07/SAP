def calculate_emissions(order_id, artisan, distance_km):
    if distance_km <= 3:
        mode = "bicycle"
        co2_emitted = 0
        co2_saved = 0.15 * distance_km
    elif distance_km <= 25:
        mode = "ev"
        co2_emitted = 0.03 * distance_km  # hypothetical EV emission
        co2_saved = (0.15 - 0.03) * distance_km
    else:
        mode = "truck"
        co2_emitted = 0.15 * distance_km
        co2_saved = 0

    return {
        "order_id": order_id,
        "artisan": artisan,
        "distance_km": distance_km,
        "mode": mode,
        "co2_emitted_kg": round(co2_emitted, 2),
        "co2_saved_kg": round(co2_saved, 2)
    }
