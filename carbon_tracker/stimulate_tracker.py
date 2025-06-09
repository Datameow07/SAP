# simulate_orders.py
import random
import json
from carbon_tracker import calculate_savings

def generate_mock_orders(n=10):
    orders = []
    for i in range(n):
        dist = round(random.uniform(1.5, 6.0), 2)  # simulate real km
        co2_emitted, co2_saved = calculate_savings(dist)
        orders.append({
            "order_id": f"ORD{i+1:03}",
            "distance_km": dist,
            "co2_emitted": co2_emitted,
            "co2_saved": co2_saved
        })
    return orders

orders = generate_mock_orders()

# Save to JSON (optional)
with open("mock_orders.json", "w") as f:
    json.dump(orders, f, indent=2)

# Show sample
for order in orders:
    print(order)
