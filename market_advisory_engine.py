import market_api

FALLBACK_CROPS = [
    {"id": "maize", "name": "Maize (Grain)", "zambian_name": "Chimanga", "category": "Grains & Cereals", "price_zk_kg": 5.2, "demand": 8.5, "margin": 35, "stability": 8.5, "is_export": False},
    {"id": "sorghum", "name": "Sorghum Grain", "zambian_name": "Mapira", "category": "Grains & Cereals", "price_zk_kg": 7.5, "demand": 6.8, "margin": 34, "stability": 9.2, "is_export": False},
    {"id": "rice", "name": "Mongu Polished Rice", "zambian_name": "Mupunga", "category": "Grains & Cereals", "price_zk_kg": 16.0, "demand": 9.2, "margin": 50, "stability": 8.5, "is_export": False},
    {"id": "sunflower", "name": "Sunflower Seed", "zambian_name": "Sanamvula", "category": "Grains & Cereals", "price_zk_kg": 11.5, "demand": 8.2, "margin": 46, "stability": 7.8, "is_export": False},
    {"id": "wheat", "name": "Winter Wheat", "zambian_name": "Gano", "category": "Grains & Cereals", "price_zk_kg": 9.8, "demand": 8.5, "margin": 41, "stability": 8.2, "is_export": False},
    {"id": "millet", "name": "Finger Millet", "zambian_name": "Luku", "category": "Grains & Cereals", "price_zk_kg": 9.0, "demand": 6.5, "margin": 32, "stability": 9.0, "is_export": False},
    {"id": "cassava", "name": "Cassava (Dried Chips)", "zambian_name": "Makopa", "category": "Roots & Tubers", "price_zk_kg": 4.5, "demand": 8.8, "margin": 42, "stability": 9.0, "is_export": False},
    {"id": "sweet_potato", "name": "Sweet Potato", "zambian_name": "Kandolo", "category": "Roots & Tubers", "price_zk_kg": 6.8, "demand": 7.0, "margin": 38, "stability": 8.8, "is_export": False},
    {"id": "potato", "name": "Irish Potato", "zambian_name": "Kandunya", "category": "Roots & Tubers", "price_zk_kg": 13.5, "demand": 8.9, "margin": 49, "stability": 8.1, "is_export": False},
    {"id": "soybean", "name": "Soybean", "zambian_name": "Soya Beans", "category": "Legumes & Pulses", "price_zk_kg": 12.8, "demand": 9.5, "margin": 55, "stability": 7.5, "is_export": True},
    {"id": "groundnuts", "name": "Groundnuts (Shelled)", "zambian_name": "Mbalala", "category": "Legumes & Pulses", "price_zk_kg": 18.5, "demand": 8.9, "margin": 52, "stability": 8.2, "is_export": True},
    {"id": "beans", "name": "Mixed Beans", "zambian_name": "Kabulangeti", "category": "Legumes & Pulses", "price_zk_kg": 17.2, "demand": 8.7, "margin": 48, "stability": 8.0, "is_export": False},
    {"id": "cotton", "name": "Seed Cotton", "zambian_name": "Pamba", "category": "Cash / Industrial", "price_zk_kg": 14.2, "demand": 7.2, "margin": 40, "stability": 6.8, "is_export": True},
    {"id": "tobacco", "name": "Flue-Cured Tobacco", "zambian_name": "Fwaka", "category": "Cash / Industrial", "price_zk_kg": 34.0, "demand": 8.4, "margin": 65, "stability": 6.5, "is_export": True},
    {"id": "coffee", "name": "Arabica Coffee", "zambian_name": "Kofi", "category": "Cash / Industrial", "price_zk_kg": 65.0, "demand": 9.1, "margin": 72, "stability": 7.9, "is_export": True},
    {"id": "avocado", "name": "Hass Avocado", "zambian_name": "Avocado", "category": "Fruits", "price_zk_kg": 22.0, "demand": 9.3, "margin": 68, "stability": 7.6, "is_export": True},
    {"id": "watermelon", "name": "Watermelon", "zambian_name": "Chipapa", "category": "Fruits", "price_zk_kg": 8.5, "demand": 8.7, "margin": 54, "stability": 7.2, "is_export": False},
    {"id": "citrus", "name": "Citrus (Sweet Oranges)", "zambian_name": "Amaolange", "category": "Fruits", "price_zk_kg": 12.0, "demand": 8.4, "margin": 47, "stability": 8.3, "is_export": False},
    {"id": "chili", "name": "Birdseye Chili Pepper", "zambian_name": "Sabola", "category": "Vegetables", "price_zk_kg": 29.5, "demand": 8.1, "margin": 62, "stability": 6.2, "is_export": True},
    {"id": "tomato", "name": "Fresh Tomato", "zambian_name": "Matimati", "category": "Vegetables", "price_zk_kg": 15.0, "demand": 9.6, "margin": 58, "stability": 6.9, "is_export": False},
]

INTERNATIONAL_CROPS = [
    {"id": "maize", "name": "Maize (Corn)", "unit": "USD/tonne", "price_usd": 180, "demand": 8.0, "trend": "stable"},
    {"id": "soybean", "name": "Soybean", "unit": "USD/tonne", "price_usd": 420, "demand": 9.0, "trend": "rising"},
    {"id": "wheat", "name": "Wheat (HRW)", "unit": "USD/tonne", "price_usd": 250, "demand": 8.5, "trend": "stable"},
    {"id": "rice", "name": "Rice (Thai 5%)", "unit": "USD/tonne", "price_usd": 390, "demand": 9.2, "trend": "rising"},
    {"id": "coffee", "name": "Arabica Coffee", "unit": "USD/lb", "price_usd": 7.37, "demand": 8.8, "trend": "falling"},
    {"id": "cocoa", "name": "Cocoa Beans", "unit": "USD/lb", "price_usd": 3.24, "demand": 7.5, "trend": "falling"},
    {"id": "cotton", "name": "Cotton", "unit": "USD/lb", "price_usd": 0.85, "demand": 7.8, "trend": "stable"},
    {"id": "sugarcane", "name": "Sugar (Raw)", "unit": "USD/lb", "price_usd": 0.22, "demand": 8.5, "trend": "stable"},
    {"id": "groundnuts", "name": "Groundnuts", "unit": "USD/tonne", "price_usd": 1100, "demand": 8.2, "trend": "stable"},
    {"id": "tea", "name": "Tea (Mombasa)", "unit": "USD/kg", "price_usd": 2.45, "demand": 7.8, "trend": "stable"},
    {"id": "tobacco", "name": "Tobacco (Flue-cured)", "unit": "USD/tonne", "price_usd": 4500, "demand": 8.0, "trend": "stable"},
    {"id": "banana", "name": "Banana", "unit": "USD/tonne", "price_usd": 950, "demand": 7.5, "trend": "rising"},
    {"id": "orange", "name": "Oranges", "unit": "USD/tonne", "price_usd": 850, "demand": 7.2, "trend": "stable"},
    {"id": "cassava", "name": "Cassava (Dried)", "unit": "USD/tonne", "price_usd": 250, "demand": 8.0, "trend": "rising"},
    {"id": "sunflower", "name": "Sunflower Oil", "unit": "USD/tonne", "price_usd": 1200, "demand": 8.5, "trend": "stable"},
]


def calculate_score(crop):
    return (crop["demand"] * 3.0 + crop.get("margin", 35) * 2.5 + crop.get("stability", 7) * 2.0 +
            (15.0 if crop.get("is_export", False) else 0.0) + crop.get("price_zk_kg", 10) * 0.1)


def refresh_live_data():
    """Fetch live market data and merge with fallback"""
    local = market_api.fetch_local_zambian_prices()
    intl = market_api.fetch_international_prices()
    return market_api.merge_market_data(local, intl, FALLBACK_CROPS)


def filter_and_rank(min_demand=6.0, max_price=999, min_margin=0, category="All",
                     export_only=False, search_query=None, sort_by="Score",
                     market_type="local"):
    crops = refresh_live_data()

    if market_type == "international":
        international = [dict(c) for c in INTERNATIONAL_CROPS]
        for c in international:
            c["margin"] = 45
            c["stability"] = 7.5
            c["is_export"] = True
            # Map ZK price from USD (rough conversion: 1 USD ~ 25 ZMW)
            if "price_usd" in c:
                c["price_zk_kg"] = round(c["price_usd"] * 25 / 1000, 2) if c["unit"] == "USD/tonne" else round(c["price_usd"] * 25, 2)
            c["score"] = calculate_score(c)
        crops = international

    if search_query:
        q = search_query.strip().lower()
        matches = [c for c in crops if q in c.get("name", "").lower() or q in c.get("zambian_name", "").lower() or q in c.get("category", "").lower()]
        if matches:
            crops = matches
        else:
            cap = search_query.strip().title()
            crops = [{"id": q.replace(" ", "_"), "name": f"{cap} (Custom)", "zambian_name": f"{cap} Variety",
                      "category": category, "price_zk_kg": 18.0, "demand": 7.5, "margin": 45,
                      "stability": 7.5, "is_export": False, "score": 45.0}]

    if category != "All":
        crops = [c for c in crops if c.get("category") == category]
    crops = [c for c in crops if c.get("demand", 0) >= min_demand]
    crops = [c for c in crops if c.get("price_zk_kg", 0) <= max_price]
    crops = [c for c in crops if c.get("margin", 0) >= min_margin]
    if export_only:
        crops = [c for c in crops if c.get("is_export", False)]

    reverse = True
    key_map = {
        "Score": lambda c: c.get("score", calculate_score(c)),
        "Price": lambda c: c.get("price_zk_kg", 0),
        "Demand": lambda c: c.get("demand", 0),
        "Margin": lambda c: c.get("margin", 0),
        "Stability": lambda c: c.get("stability", 0),
    }
    key_fn = key_map.get(sort_by, key_map["Score"])
    for c in crops:
        if "score" not in c:
            c["score"] = calculate_score(c)
    return sorted(crops, key=key_fn, reverse=reverse)
