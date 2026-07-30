"""
Crop Diagnostic Camera Tool Module.
Provides threaded camera streaming (CropDiagnosticCamera)
and utility functions for leaf analysis.
"""

import os
import cv2
import logging
import threading
import numpy as np
from collections import deque
from datetime import datetime
from typing import Optional, Tuple, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default directory for diagnostic captures
CAPTURE_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "AgriEye", "crop_captures")


def ensure_capture_dir() -> str:
    os.makedirs(CAPTURE_DIR, exist_ok=True)
    return CAPTURE_DIR


# ============================================================================
# Core Camera Capture & UI Overlay Class
# ============================================================================

class CropDiagnosticCamera:
    """
    Background camera capture thread designed for continuous live preview,
    ROI framing overlay, and raw un-overlayed frame extraction for ML models.
    """

    def __init__(self, camera_id: int = 0, resolution: Tuple[int, int] = (1280, 720)):
        """
        Initialize the diagnostic camera.

        Args:
            camera_id: Camera device index. If -1, auto-detects the first working camera.
            resolution: (width, height) tuple
        """
        self.camera_id = camera_id
        self.resolution = resolution
        self.is_running = False
        self._thread = None
        self._camera_idx = camera_id
        self.latest_frame: Optional[np.ndarray] = None
        self.latest_raw_frame: Optional[np.ndarray] = None
        self.frame_lock = threading.Lock()
        self.frame_buffer = deque(maxlen=30)

    def _find_camera(self) -> int:
        """Find the first camera index that returns non-black frames."""
        found = [0]

        def _try_idx(idx):
            try:
                cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
                if not cap.isOpened():
                    cap.release()
                    return
                ret, frame = cap.read()
                cap.release()
                if ret and frame is not None and np.mean(frame) > 10:
                    found[0] = idx
            except Exception:
                pass

        for idx in range(4):
            t = threading.Thread(target=_try_idx, args=(idx,), daemon=True)
            t.start()
            t.join(timeout=2.0)
            if found[0] == idx and idx > 0:
                logger.info(f"Auto-detected camera at index {idx}")
                return idx

        logger.info(f"No real camera found, using index {found[0]}")
        return found[0]

    def start(self) -> bool:
        """Start camera capture in a background thread."""
        idx = self.camera_id
        if idx < 0:
            idx = self._find_camera()

        self._camera_idx = idx
        self.is_running = True
        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()
        return True

    def _capture_loop(self):
        """Camera capture loop — runs entirely in a single background thread."""
        import time as _time
        try:
            cap = cv2.VideoCapture(self._camera_idx, cv2.CAP_DSHOW)
            if not cap.isOpened():
                logger.error(f"Cannot open camera device {self._camera_idx}")
                self.is_running = False
                return

            while self.is_running:
                ret, frame = cap.read()
                if ret and frame is not None:
                    raw_frame = frame.copy()
                    processed_frame = create_diagnostic_frame(frame)

                    with self.frame_lock:
                        self.latest_raw_frame = raw_frame
                        self.latest_frame = processed_frame
                        self.frame_buffer.append(raw_frame)
                else:
                    _time.sleep(0.03)

            cap.release()
        except Exception as e:
            logger.error(f"Camera capture error: {e}")
            self.is_running = False

    def get_frame(self, raw: bool = False) -> Optional[np.ndarray]:
        """
        Get the most recent camera frame.

        Args:
            raw: If True, returns clean frame without UI overlays (ideal for ML/vision models).
        """
        with self.frame_lock:
            if raw:
                return self.latest_raw_frame.copy() if self.latest_raw_frame is not None else None
            return self.latest_frame.copy() if self.latest_frame is not None else None

    def stop(self):
        """Stop background capture thread and release hardware resources."""
        self.is_running = False
        if hasattr(self, '_thread') and self._thread is not None:
            self._thread.join(timeout=2.0)
        logger.info("Diagnostic camera stopped")

    def __del__(self):
        self.stop()


# ============================================================================
# Processing & Segmentation Utilities
# ============================================================================

def create_diagnostic_frame(
    frame: np.ndarray, 
    add_target_roi: bool = True, 
    add_health_indicator: bool = True
) -> np.ndarray:
    """Overlay diagnostic alignment guides and live leaf color metrics onto frame."""
    if frame is None:
        return None

    frame = frame.copy()
    h, w = frame.shape[:2]

    box_w, box_h = int(w * 0.5), int(h * 0.6)
    x1, y1 = (w - box_w) // 2, (h - box_h) // 2
    x2, y2 = x1 + box_w, y1 + box_h

    if add_target_roi:
        line_len = 25
        color = (50, 205, 50)  # Lime green guide
        thickness = 2

        # Draw ROI corner brackets
        cv2.line(frame, (x1, y1), (x1 + line_len, y1), color, thickness)
        cv2.line(frame, (x1, y1), (x1, y1 + line_len), color, thickness)
        cv2.line(frame, (x2, y1), (x2 - line_len, y1), color, thickness)
        cv2.line(frame, (x2, y1), (x2, y1 + line_len), color, thickness)
        cv2.line(frame, (x1, y2), (x1 + line_len, y2), color, thickness)
        cv2.line(frame, (x1, y2), (x1, y2 - line_len), color, thickness)
        cv2.line(frame, (x2, y2), (x2 - line_len, y2), color, thickness)
        cv2.line(frame, (x2, y2), (x2, y2 - line_len), color, thickness)

        cv2.putText(
            frame, "ALIGN LEAF IN TARGET ZONE", (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA
        )

    if add_health_indicator:
        roi = frame[y1:y2, x1:x2]
        color_status, status_bgr, _ = analyze_leaf_color_quick(roi)

        cv2.rectangle(frame, (0, 0), (w, 32), (20, 20, 20), -1)
        cv2.putText(
            frame, f"Diagnostic Scanner: {color_status}", (12, 21),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_bgr, 1, cv2.LINE_AA
        )

    return frame


def analyze_leaf_color_quick(roi: np.ndarray) -> Tuple[str, Tuple[int, int, int], Dict[str, float]]:
    """
    Performs fast HSV color space analysis to evaluate vegetation vs symptoms.
    
    Returns:
        (Status String, BGR Color, Metrics Dictionary)
    """
    if roi is None or roi.size == 0:
        return "No Target Detected", (200, 200, 200), {}

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    total_pixels = roi.shape[0] * roi.shape[1]

    # HSV thresholds for leaf evaluation
    green_mask = cv2.inRange(hsv, (35, 40, 40), (85, 255, 255))
    yellow_mask = cv2.inRange(hsv, (20, 40, 40), (35, 255, 255))
    brown_mask = cv2.inRange(hsv, (0, 30, 20), (20, 255, 180))

    green_pct = round((np.count_nonzero(green_mask) / total_pixels) * 100, 1)
    yellow_pct = round((np.count_nonzero(yellow_mask) / total_pixels) * 100, 1)
    brown_pct = round((np.count_nonzero(brown_mask) / total_pixels) * 100, 1)

    metrics = {
        "healthy_green_pct": green_pct,
        "chlorosis_yellow_pct": yellow_pct,
        "necrosis_brown_pct": brown_pct
    }

    if green_pct > 40 and yellow_pct < 15 and brown_pct < 10:
        return "Healthy Leaf Foliage", (0, 255, 127), metrics
    elif yellow_pct >= 15:
        return "Chlorosis Detected (Yellowing/Deficiency)", (0, 215, 255), metrics
    elif brown_pct >= 10:
        return "Necrosis / Blight Spots Detected", (50, 100, 255), metrics
    else:
        return "Position leaf within frame...", (200, 200, 200), metrics


def extract_leaf_segment(frame: np.ndarray) -> np.ndarray:
    """Segments the main plant leaf using color masking and crops to bounding box."""
    if frame is None:
        return frame

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (10, 30, 30), (90, 255, 255))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        pad = 20
        h_f, w_f = frame.shape[:2]
        x1, y1 = max(0, x - pad), max(0, y - pad)
        x2, y2 = min(w_f, x + w + pad), min(h_f, y + h + pad)

        return frame[y1:y2, x1:x2]

    return frame


def frame_to_bytes(frame: np.ndarray, quality: int = 90) -> Optional[bytes]:
    """Convert OpenCV frame into JPEG binary payload for streaming/APIs."""
    if frame is None:
        return None
    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
    return buffer.tobytes()


# ============================================================================
# Standalone utility functions (no LiveKit dependency)
# ============================================================================