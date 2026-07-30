# Agri-Eye Mobile

Android version of the Agri-Eye crop diagnostic system for Zambian farmers.

## Features

- **Live Diagnosis** – Capture a photo of a crop and get AI-powered disease/diagnosis
- **Offline Analysis** – Analyze stored images using an offline VLM model
- **Crop Advisory** – Get crop recommendations based on soil, climate, and weather inputs
- **Market Advisory** – View market prices and demand for Zambian crops
- **Crop Simulator** – Watch realistic plant growth animations with stage-by-stage tracking
- **Model Trainer** – Train a neural network on your own crop data

## Build for Android

### Using GitHub Actions (recommended)

1. Push this repo to GitHub
2. Go to Actions → Build Android APK → Run workflow
3. Download the APK from the artifacts

### Using Buildozer locally (Linux only)

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf automake cmake libtool pkg-config libncurses5 libncursesw5 libtinfo5 ccache curl lld llvm libffi-dev libssl-dev
pip install --upgrade pip cython buildozer
buildozer android debug
```

The APK will be in `bin/AgriEye-1.0.0-debug.apk`.

## Project Structure

```
agri-eye/
├── main.py                  # Kivy app (UI + logic)
├── buildozer.spec           # Android build config
├── requirements.txt         # Python dependencies
├── core/                    # Business logic from desktop version
│   ├── crop_advisory_engine.py
│   ├── market_advisory_engine.py
│   ├── plant_db.py
│   ├── ann_model.py
│   ├── gemini_client.py
│   ├── offline_vlm.py
│   ├── localization.py
│   └── eye_module.py
├── .github/workflows/       # CI/CD for APK builds
└── data/                    # Static data files
```
