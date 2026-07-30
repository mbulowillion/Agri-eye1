import requests
import re
import json
import time
from datetime import datetime, timedelta

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

CACHE = {}
CACHE_DURATION = timedelta(hours=4)

ZAMBIAN_CROP_MAP = {
    "maize": ["maize", "corn", "chimanga"],
    "cassava": ["cassava", "chinangwa", "makopa"],
    "sweet_potato": ["sweet potato", "kandolo"],
    "potato": ["irish potato", "potato", "kandunya"],
    "soybean": ["soybean", "soya", "soya beans"],
    "groundnuts": ["groundnut", "groundnuts", "mbalala", "peanut"],
    "beans": ["beans", "nyemba", "edible beans", "mixed beans"],
    "sorghum": ["sorghum", "mapira"],
    "rice": ["rice", "mupunga"],
    "sunflower": ["sunflower", "sanamvula"],
    "chili": ["chili", "chilli", "pepper", "sabola"],
    "tomato": ["tomato", "matimati"],
    "coffee": ["coffee", "kofi", "arabica"],
    "avocado": ["avocado", "mapapa"],
    "watermelon": ["watermelon", "chipapa"],
    "citrus": ["citrus", "orange", "ndimu", "malambe", "amaolange"],
    "cotton": ["cotton", "pamba"],
    "tobacco": ["tobacco", "fwaka"],
    "wheat": ["wheat", "tirigu", "gano"],
    "millet": ["millet", "malezi", "luku"],
    "cocoa": ["cocoa", "cacao"],
    "tea": ["tea", "tiyi"],
    "sugarcane": ["sugarcane", "nsukali"],
    "banana": ["banana", "ntofu"],
    "mango": ["mango", "imango"],
    "pineapple": ["pineapple", "chinafuta"],
    "papaya": ["papaya", "mapwapwa"],
    "onion": ["onion", "anyenye"],
    "cabbage": ["cabbage", "kabichi"],
    "okra": ["okra", "dete"],
    "eggplant": ["eggplant", "entula"],
    "carrot": ["carrot", "kaloti"],
    "ginger": ["ginger", "tsogolo"],
    "cashew": ["cashew", "mkanju"],
}

INTERNATIONAL_CROP_MAP = {
    "maize": ["maize", "corn"],
    "soybean": ["soybean", "soybeans", "soya"],
    "wheat": ["wheat"],
    "rice": ["rice"],
    "coffee": ["coffee", "arabica"],
    "cocoa": ["cocoa", "cacao"],
    "sugarcane": ["sugar", "sugarcane"],
    "cotton": ["cotton"],
    "groundnuts": ["groundnuts", "peanuts"],
    "sunflower": ["sunflower oil", "sunflower seed"],
    "palm_oil": ["palm oil"],
    "tea": ["tea"],
    "tobacco": ["tobacco"],
    "banana": ["banana"],
    "orange": ["orange"],
    "cassava": ["cassava"],
}


def _cached(key, fetch_fn, ttl=None):
    if ttl is None:
        ttl = CACHE_DURATION
    if key in CACHE:
        entry = CACHE[key]
        if datetime.now() - entry["ts"] < ttl:
            return entry["data"]
    data = fetch_fn()
    CACHE[key] = {"data": data, "ts": datetime.now()}
    return data


def _scrape_zamfarm_shop():
    """Scrape product listings from zamfarm2market.com shop page"""
    if not HAS_BS4:
        return None
    try:
        r = requests.get("https://zamfarm2market.com/shop/",
                         headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, "lxml")
        products = soup.select(".product, li.product, .type-product")
        results = []
        for p in products:
            title_el = p.select_one(".woocommerce-loop-product__title, h2, .product-title, .wc-block-grid__product-title")
            price_el = p.select_one(".price, .woocommerce-Price-amount, .wc-block-grid__product-price")
            if title_el:
                title = title_el.get_text(strip=True)
                price_text = price_el.get_text(strip=True) if price_el else ""
                prices_found = re.findall(r"ZK?([\d,]+\.?\d*)", price_text)
                price_val = None
                if prices_found:
                    price_val = float(prices_found[0].replace(",", ""))
                results.append({"title": title, "price": price_val})
        return results if results else None
    except Exception:
        return None


def _scrape_zamfarm_home():
    """Scrape latest listings from zamfarm2market homepage"""
    if not HAS_BS4:
        return None
    try:
        r = requests.get("https://zamfarm2market.com/",
                         headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, "lxml")
        listings = []
        for el in soup.find_all(["h2", "h3", "h4", "strong"]):
            txt = el.get_text(strip=True)
            if txt and len(txt) > 5 and "kagezi" in txt.lower():
                parent = el.find_parent(["div", "li", "article"])
                price_el = parent.select_one(".price, .amount, .woocommerce-Price-amount") if parent else None
                price_text = price_el.get_text(strip=True) if price_el else ""
                prices_found = re.findall(r"ZK?([\d,]+\.?\d*)", price_text)
                price_val = None
                if prices_found:
                    price_val = float(prices_found[0].replace(",", ""))
                listings.append({"title": txt, "price": price_val})
        return listings if listings else None
    except Exception:
        return None


def _fetch_international_indexmundi():
    """Scrape commodity prices from indexmundi"""
    if not HAS_BS4:
        return None
    try:
        r = requests.get("https://www.indexmundi.com/commodities/",
                         headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, "lxml")
        rows = soup.select("table tr")
        data = {}
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                name = cells[0].get_text(strip=True).lower()
                price_text = cells[1].get_text(strip=True).replace("$", "").replace(",", "")
                try:
                    price = float(price_text)
                    data[name] = price
                except ValueError:
                    pass
        return data if data else None
    except Exception:
        return None


def _fetch_world_bank_commodities():
    """Fetch commodity prices from World Bank API"""
    try:
        r = requests.get(
            "https://api.worldbank.org/v2/country/all/indicator/CM.MKT.INDX.ZG?format=json",
            headers={"User-Agent": "Mozilla/5.0"}, timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            return data
        return None
    except Exception:
        return None


def fetch_local_zambian_prices():
    """Fetch current Zambian market prices from multiple sources"""
    key = "zambian_prices"
    def _fetch():
        prices = {}

        # Source 1: zamfarm shop
        shop = _scrape_zamfarm_shop()
        if shop:
            for item in shop:
                title_lower = item["title"].lower()
                price = item["price"]
                for crop_id, keywords in ZAMBIAN_CROP_MAP.items():
                    if any(kw in title_lower for kw in keywords):
                        existing = prices.get(crop_id, {})
                        existing["price_zk_kg"] = price
                        existing["source"] = "zamfarm2market"
                        existing["name"] = item["title"]
                        prices[crop_id] = existing

        # Source 2: zamfarm home listings
        home = _scrape_zamfarm_home()
        if home:
            for item in home:
                title_lower = item["title"].lower()
                price = item["price"]
                for crop_id, keywords in ZAMBIAN_CROP_MAP.items():
                    if any(kw in title_lower for kw in keywords):
                        if crop_id not in prices or prices[crop_id].get("source") == "fallback":
                            prices[crop_id] = {
                                "price_zk_kg": price,
                                "source": "zamfarm2market",
                                "name": item["title"]
                            }

        return prices if prices else None

    return _cached(key, _fetch)


def fetch_international_prices():
    """Fetch international commodity prices"""
    key = "intl_prices"
    def _fetch():
        prices = {}

        # Source: indexmundi
        idx_data = _fetch_international_indexmundi()
        if idx_data:
            for name, price_usd in idx_data.items():
                for crop_id, keywords in INTERNATIONAL_CROP_MAP.items():
                    if any(kw in name for kw in keywords):
                        prices[crop_id] = {
                            "price_usd": price_usd,
                            "source": "indexmundi",
                        }

        return prices if prices else None

    return _cached(key, _fetch)


def merge_market_data(local_prices, intl_prices, fallback_crops):
    """Merge API data with fallback data, preferring live data"""
    merged = []
    now = datetime.now()

    for crop in fallback_crops:
        c = dict(crop)
        cid = crop["id"]
        c["data_source"] = "fallback"
        c["data_fetched_at"] = None

        if local_prices and cid in local_prices:
            lp = local_prices[cid]
            if lp.get("price_zk_kg") is not None:
                c["price_zk_kg"] = lp["price_zk_kg"]
                c["data_source"] = "live_zambian"
                c["data_fetched_at"] = now.isoformat()

        if intl_prices and cid in intl_prices:
            ip = intl_prices[cid]
            if ip.get("price_usd") is not None:
                c["price_usd"] = ip["price_usd"]
                if c["data_source"] == "fallback":
                    c["data_source"] = "live_international"
                    c["data_fetched_at"] = now.isoformat()
                elif c["data_source"] == "live_zambian":
                    c["data_source"] = "live_both"

        merged.append(c)

    return merged
