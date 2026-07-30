import os
import json
import re
import sys
import time
import hashlib
import base64

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

try:
    import cv2
    import numpy as np
    from open_processor import analyze as open_analyze
    HAS_OPEN = True
except ImportError:
    HAS_OPEN = False

from plant_db import PLANTS, GENERAL_PLANTS


class KeyRotator:
    def __init__(self):
        self._keys = []
        self._idx = 0
        self._load()

    def _load(self):
        keys = []
        primary = os.environ.get("GROQ_API_KEY", "")
        if primary:
            keys.append(primary)
        for i in range(2, 10):
            k = os.environ.get(f"GROQ_API_KEY_{i}", "")
            if k:
                keys.append(k)
        self._keys = keys

    @property
    def available(self) -> bool:
        return len(self._keys) > 0

    def get_key(self) -> str:
        if not self._keys:
            return ""
        return self._keys[self._idx % len(self._keys)]

    def rotate(self) -> str:
        if len(self._keys) > 1:
            self._idx = (self._idx + 1) % len(self._keys)
        return self.get_key()

    def reset(self) -> str:
        self._idx = 0
        return self.get_key()


_rotator = KeyRotator()

BASE_URL = "https://api.groq.com/openai/v1"
MODEL = "qwen/qwen3.6-27b"
_cache = {}


def _hash_image(b64):
    return hashlib.sha256(b64.encode()[:100000]).hexdigest()[:16]


def _score_match(description, traits):
    """Score how well a visual description matches plant/crop traits."""
    desc_lower = description.lower()
    score = 0
    for trait_list in traits.values():
        for trait in trait_list:
            if trait.lower() in desc_lower:
                score += 1
    return score


def _score_disease(description, disease_data):
    """Score how well symptoms match a disease."""
    desc_lower = description.lower()
    score = 0
    for symptom in disease_data["symptoms"]:
        if any(word in desc_lower for word in symptom.lower().split()):
            score += 1
    return score


def _match_plant(description):
    """Match visual description against verified plant database."""
    best_plant = None
    best_score = -1

    all_plants = dict(PLANTS)
    all_plants.update(GENERAL_PLANTS)

    for pid, plant in all_plants.items():
        traits = {
            "leaf_shape": plant.get("leaf_shape", []),
            "leaf_color": plant.get("leaf_color", []),
            "leaf_veins": plant.get("leaf_veins", []),
            "leaf_margin": plant.get("leaf_margin", []),
            "leaf_texture": plant.get("leaf_texture", []),
        }
        score = _score_match(description, traits)
        if score > best_score:
            best_score = score
            best_plant = plant

    return best_plant, best_score


def _match_disease(description, plant):
    """Match symptoms against verified disease database."""
    best_disease = "Healthy"
    best_score = -1

    for disease_name, disease_data in plant["diseases"].items():
        score = _score_disease(description, disease_data)
        if score > best_score:
            best_score = score
            best_disease = disease_name

    return plant["diseases"][best_disease], best_disease, best_score


def diagnose(image_base64, api_key=None, plant_hint="Auto-Detect Any Plant Species"):
    if not HAS_HTTPX:
        return _fallback_open(image_base64, plant_hint)

    clean_b64 = re.sub(r"^data:image/\w+;base64,", "", image_base64)

    h = _hash_image(clean_b64)
    if h in _cache:
        return _cache[h]

    if api_key:
        pool = [api_key]
    else:
        pool = list(_rotator._keys) if _rotator.available else [""]

    if not pool or not pool[0]:
        return _fallback_open(image_base64, plant_hint)

    start = _rotator._idx if not api_key else 0
    system_msg = "You are a botanist. Describe the leaf visually only. Do NOT identify the plant or disease."
    prompt = (
        "Describe this leaf in detail: shape, color, texture, veins, margins, "
        "and any spots, lesions, discoloration, or growth patterns visible. "
        "Use plain text, no JSON."
    )

    for attempt in range(len(pool)):
        key = pool[(start + attempt) % len(pool)]
        if not key:
            continue

        for retry in range(3):
            try:
                body = {
                    "model": MODEL,
                    "messages": [
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{clean_b64}"}}]},
                    ],
                    "max_tokens": 1000,
                }
                resp = httpx.post(f"{BASE_URL}/chat/completions", json=body,
                    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, timeout=30)

                if resp.status_code == 429:
                    time.sleep(2 ** retry)
                    continue
                if resp.status_code in (502, 503):
                    break
                resp.raise_for_status()
                data = resp.json()
                description = data["choices"][0]["message"]["content"]
                break
            except Exception as e:
                print(f"[groq] {type(e).__name__}: {e}", file=sys.stderr)
                if retry < 2:
                    time.sleep(2 ** retry)
                    continue
                return _fallback_open(image_base64, plant_hint)
        else:
            return _fallback_open(image_base64, plant_hint)

        # Match against verified knowledge base
        plant, plant_score = _match_plant(description)
        if plant:
            disease_data, disease_name, symptom_score = _match_disease(description, plant)
            confidence = min(95, 50 + plant_score * 5 + symptom_score * 5)
        else:
            plant = {"name": plant_hint, "scientific_name": "", "family": "", "diseases": {"Unknown": {"symptoms": [], "treatment": []}}}
            disease_name = "Unknown"
            disease_data = {"symptoms": [], "treatment": []}
            confidence = 50

        result = {
            "plant_name": plant["name"],
            "common_name": plant.get("zambian_name", plant["name"]),
            "scientific_name": plant.get("scientific_name", ""),
            "family": plant.get("family", ""),
            "health_percentage": 100 if disease_name == "Healthy" else max(20, 100 - symptom_score * 10),
            "condition": disease_name,
            "symptoms": ", ".join(disease_data["symptoms"]) if disease_data["symptoms"] else description[:300],
            "diagnosis_text": description[:500],
            "confidence": confidence,
            "treatment_recommendations": disease_data["treatment"],
            "method": "knowledge_base",
        }
        _cache[h] = result
        return result

    return _fallback_open(image_base64, plant_hint)


def _fallback_open(image_base64, plant_hint):
    """Local OPEN processor as fallback."""
    if not HAS_OPEN:
        return None
    try:
        clean_b64 = re.sub(r"^data:image/\w+;base64,", "", image_base64)
        raw = base64.b64decode(clean_b64)
        nparr = np.frombuffer(raw, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return None
        open_res = open_analyze(image_array=img)
        return {
            "plant_name": plant_hint,
            "common_name": "",
            "scientific_name": "",
            "family": "",
            "health_percentage": round(100 - open_res["diseased_pct"], 1),
            "condition": open_res["condition"],
            "symptoms": open_res["diagnosis_text"],
            "diagnosis_text": open_res["diagnosis_text"],
            "confidence": open_res["confidence"],
            "treatment_recommendations": [],
            "method": "open",
        }
    except Exception as e:
        print(f"[fallback] Error: {e}", file=sys.stderr)
        return None
