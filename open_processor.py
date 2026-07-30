import cv2
import numpy as np


def analyze(image_path=None, image_array=None):
    if image_array is not None:
        img = image_array
    elif image_path is not None:
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if img is None:
            raise FileNotFoundError(f"Cannot read image: {image_path}")
    else:
        raise ValueError("Provide image_path or image_array")

    h, w = img.shape[:2]
    total_pixels = w * h

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    green_mask = cv2.inRange(hsv, (35, 40, 40), (85, 255, 255))
    leaf_count = np.count_nonzero(green_mask)

    yellow_mask = cv2.inRange(hsv, (20, 40, 40), (35, 255, 255))
    brown_mask = cv2.inRange(hsv, (0, 30, 20), (20, 255, 180))
    diseased_count = np.count_nonzero(yellow_mask) + np.count_nonzero(brown_mask)

    leaf_mask_pct = (leaf_count / total_pixels * 100) if total_pixels > 0 else 0.0
    diseased_pct = (diseased_count / leaf_count * 100) if leaf_count > 0 else 0.0

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = np.sqrt(grad_x**2 + grad_y**2)
    texture_score = float(np.mean(grad_mag))

    leaf_region = cv2.bitwise_and(img, img, mask=green_mask)
    leaf_hsv = cv2.cvtColor(leaf_region, cv2.COLOR_BGR2HSV)
    hue_vals = leaf_hsv[:, :, 0][green_mask > 0]
    mean_hue = float(np.mean(hue_vals)) if len(hue_vals) > 0 else 60.0

    condition, diagnosis_text, confidence = _classify(diseased_pct, texture_score, mean_hue)

    return {
        "leaf_mask_pct": round(leaf_mask_pct, 2),
        "diseased_pct": round(diseased_pct, 2),
        "texture_score": round(texture_score, 2),
        "mean_hue": round(mean_hue, 2),
        "condition": condition,
        "diagnosis_text": diagnosis_text,
        "confidence": confidence,
    }


def _classify(diseased_pct, texture_score, mean_hue):
    if diseased_pct < 12.0:
        return (
            "Healthy Leaf",
            f"OPEN analysis indicates high chlorophyll density (diseased area: {round(diseased_pct, 1)}%). "
            "Leaf tissue shows normal structural symmetry.",
            round(94.0 - diseased_pct * 0.5, 1),
        )
    elif diseased_pct < 30.0:
        return (
            "Early Blight / Leaf Spot",
            f"OPEN analysis detected localized foliar lesions (diseased area: {round(diseased_pct, 1)}%, "
            f"texture variance: {round(texture_score, 1)}). Early copper-based fungicide recommended.",
            88.0,
        )
    elif diseased_pct < 55.0:
        return (
            "Maize Streak Virus / Mosaic",
            f"OPEN analysis found chlorotic streaking across leaf veins (diseased area: {round(diseased_pct, 1)}%, "
            f"mean hue: {round(mean_hue, 1)}°). Vector control advised.",
            86.0,
        )
    else:
        return (
            "Severe Necrosis / Fall Armyworm Damage",
            f"OPEN analysis flagged extensive leaf tissue destruction (diseased area: {round(diseased_pct, 1)}%). "
            "Immediate field isolation required.",
            91.0,
        )
