import tkinter as tk

ENGLISH = "en"
BEMBA = "be"

_current_lang = ENGLISH

BEMBA_TRANSLATIONS = {
    # ─── Tab & Sidebar ───
    "Agri-Eye": "Iciso ca Bulimi",
    "Live Diagnosis": "Ukupima kwa Cine",
    "Offline Analysis": "Ukupima Pa Offline",
    "Crop Advisory": "Upaila wa Filimwa",
    "Market Advisory": "Upaila wa Cilandanya",
    "Crop Simulator": "Iceshanya ca Filimwa",
    "Model Trainer": "Iceshanya ca Model",

    # ─── Camera Controls ───
    "Start Camera": "Iputula Kamera",
    "Stop Camera": "Imina Kamera",
    "Capture & Diagnose": "Kufula no Kupima",
    "CAM: OFFLINE": "KAMERA: TAYALA",
    "CAM: REAL WEBCAM ACTIVE": "KAMERA: IKALA BULANGA",
    "CAM: FALLBACK (OFFLINE)": "KAMERA: IBYA NI TAYALA",
    "CAM: STOPPED": "KAMERA: IMINWE",
    "[C] to capture": "Pani [C] pa kufula",
    "Camera connected": "Kamera iyikata",
    "No webcam found — using fallback preview": "Tapata kamera — twabombela ne fallback",

    # ─── Diagnosis ───
    "Diagnosis Report": "Lipoti lya Kupima",
    "Memory Bank": "Ibukoshi lya Bukumbusho",
    "captures": "ifula",
    "Start the camera to begin live diagnosis.": "Iputula kamera pa kendai ukupima.",
    "Position a leaf within the target zone brackets and press [C] or click 'Capture & Diagnose'.": "Ika ifuwa mu cibangwa ca target, pani [C] nelyo suna pa 'Capture & Diagnose'.",
    "The AI model will analyze the leaf and provide a full pathology report.": "AI model ikapima ifuwa no kupeela lipoti lyonse.",
    "Saved": "Ifulilwe",
    "Save failed": "Ifulila kufilwa",
    "No frame captured yet": "Tapali icifulwe",
    "Diagnosing...": "Ukupima...",
    "Analyzing with AI Vision...": "Ukupima ne AI Vision...",
    "AI diagnosis is not available.": "Ukupima kwa AI takukabele.",
    "Check your internet connection and ensure GROQ_API_KEY is set in the .env file.": "Lole ifyakuba intaneti no kushinikila GROQ_API_KEY file .env.",
    "All API keys have been exhausted or no keys are configured.": "API keys conse zilekana nelyo tapali izebelwe.",
    "AI PLANTATION PATHOLOGY REPORT": "LIPOTI LYA KUPIMA IFILIMWA",
    "Scientific Name": "Ishina lya Sayansi",
    "Common Name": "Ishina Lya Cibemba",
    "Family": "Ishiwi",
    "Condition": "Ishuko",
    "Confidence": "Ukushinikila",
    "Health": "Ubumi",
    "Method": "Inzila",
    "Symptoms": "Ibilwele",
    "TREATMENT RECOMMENDATIONS": "IFYAKUPAYA IFILWELE",
    "LOW CONFIDENCE: Consider lab confirmation": "UKUSHINIKILA FWASA: Lole ne lab",
    "Error": "Ibukwata",
    "AI unavailable": "AI tayalipo",
    "AI is not available.": "AI tayalipo.",
    "Check .env and internet connection.": "Lole .env ne intaneti.",
    "Action Plan": "Icapangwa.ca kucita",
    "No target detected": "Tapafiswike",
    "Healthy Leaf Foliage": "Ifuwa lilumbwe",
    "Position leaf within frame...": "Ika ifuwa mu frame...",
    "TARGET ZONE": "CIBANGWA CA TARGET",
    "NO CAMERA - SIMULATED FEED": "KAMERA TAYALIPO - ICESHANYO",
    "Click 'Capture & Diagnose' to test": "Suna pa 'Capture & Diagnose' pa kukesha",

    # ─── Offline Analysis ───
    "Upload Image": "Twala Ifikope",
    "Analyze": "Pima",
    "Analysis Results": "Ifyakupima",
    "Upload an image or use the synthetic test image, then click Analyze.": "Twala ifikope nelya ubombele ne synthetic, elyo suna Analyze.",
    "Cannot read image file": "Tapali ifikope ili nakubelenga",
    "Running {method} analysis...": "Ukupima {method}...",
    "Method:": "Inzila:",
    "Upload Image": "Twala Ifikope",
    "OPEN processor report": "Lipoti lya OPEN processor",
    "AI VISION DIAGNOSIS": "UKUPIMA KWA AI VISION",
    "ANN ML INFERENCE": "Iceshanya ca ANN ML",
    "Upload an image": "Twala ifikope",
    "Loaded": "Ubombelwe",
    "synthetic test image": "iceshanyo ifikope",

    # ─── Crop Advisory ───
    "Crop Advisory": "Upaila wa Filimwa",
    "Crop Recommendations": "Ifilimwa Ifyasankwa",
    "Category": "Mushango",
    "Answer a few questions about your farm to get crop recommendations.": "Asuka imishobo ipepe palwa ifimwa lyenu pa kusanga upaila.",
    "What climate type does your farm have?": "Ilyo mushango wa nkolele wamunonshi wakwe ifimwa cakuti?",
    "What soil type does your farm have?": "Ilo mushango wa ilo wamunonshi wakwe ifimwa cakuti?",
    "What is your soil pH range?": "Ilo pH palwa ilo lyenu cayaya?",
    "What is your average annual rainfall (mm)?": "Ilo fula lyamulundu mwaka?",
    "What is your temperature range (°C)?": "Ilyo lyamunonshi (°C)?",
    "Search for a specific crop (optional):": "Kwaya ifimwa (te puliki):",
    "Get Recommendations": "Pandeni Upaila",
    "Refresh": "Pya",
    "Rank": "Pele",
    "Crop": "Filimwa",
    "Zambian Name": "Ishina lya Zambia",
    "Score": "Manambala",
    "Climate": "Ilyo",
    "Temp": "Ilyo",
    "Rainfall": "Fula",
    "Growth Stages": "Inshita sha Kukula",
    "CROP MATURED - READY FOR HARVEST": "FILIMWA YA KULA - YAKU KONKOLA",
    "Simulating": "Iceshanya",
    "Crop Growth Cycle": "Iceshanya ca kukula kwa Filimwa",
    "Current": "Ico cali",
    "Day": "Ubushiku",
    "of": "pa",
    "days": "nshiku",

    # ─── Market Advisory ───
    "Market Advisory": "Upaila wa Cilandanya",
    "Market Rankings": "Ipepala lya Cilandanya",
    "Zambian Local Market": "Cilandanya ca Zambia",
    "International Market (Export)": "Cilandanya ca Calo (Export)",
    "Zambian Local Market Prices": "Mitengo ya Cilandanya ca Zambia",
    "International Market Prices (Export)": "Mitengo ya Cilandanya ca Calo (Export)",
    "Source": "Ishuko",
    "ZMW equivalent": "Ishibano ca ZMW",
    "Search:": "Fwaya:",
    "Min Demand:": "Icipimo ca Demand:",
    "Max Price:": "Mutengo Wakunonshi:",
    "Min Margin:": "Margin Wakunonshi:",
    "Category:": "Mushango:",
    "Sort By:": "Pandeni pa:",
    "Export Only": "Export Fye",
    "Price (ZMW/kg)": "Mutengo (ZMW/kg)",
    "Demand": "Icipimo",
    "Margin%": "Margin%",
    "Stability": "Ukutula",
    "Export": "Export",
    "Score": "Manambala",
    "Price": "Mutengo",
    "All": "Yonse",
    "Grains & Cereals": "Ifilimwa Ifyakukamanya",
    "Roots & Tubers": "Ifilimwa Ifyakumilila",
    "Legumes & Pulses": "Ifilimwa Ifyakulya",
    "Cash / Industrial": "Ifilimwa Ifyakucita",
    "Fruits": "Ifilimwa Ifyamatungulu",
    "Vegetables": "Ifilimwa Ifyamasamba",

    # ─── Simulator ───
    "Growth Simulator": "Iceshanya ca Kukula",
    "Play": "Tampa",
    "Pause": "Ima",
    "Reset": "Pilibula",
    "Day:": "Ubushiku:",

    # ─── Model Trainer ───
    "ANN Trainer": "Iceshanya ca ANN",
    "Epochs:": "Epochs:",
    "Learning Rate:": "Learning Rate:",
    "Hidden Dim:": "Hidden Dim:",
    "Start Training": "Tampa Iceshanya",
    "Ready": "Bekele",
    "Training Log": "Ibukoshi lya Iceshanya",
    "Training complete": "Iceshanya ca mana",
    "No training session active.": "Tapali iceshanya ilya kubele.",
    "Configure parameters and execute.": "Beka ifyakubelekafye elyo cishe.",
    "Training in progress...": "Iceshanya cilakubeleka...",
    "Training started...": "Iceshanya ca tampa...",
    "Training...": "Iceshanya...",
    "=== TRAINING COMPLETE ===": "=== ICESHANYA CA MANA ===",
    "Model saved": "Model yabulokwe",
    "Samples": "Iceshanya",
    "Classes": "Ishiwi",
    "Training Log": "Ibukoshi lya Iceshanya",

    # ─── Generic ───
    "Error:": "Ibukwata:",
    "Unknown": "Cisakamane",
    "N/A": "Tepo",
    "No": "Awe",
    "Yes": "Ee",
}

BEMBA_MONTHS = {
    "January": "Januali",
    "February": "Februali",
    "March": "Machi",
    "April": "Apule",
    "May": "Mei",
    "June": "Juni",
    "July": "Julai",
    "August": "Ogasiti",
    "September": "Seputemba",
    "October": "Oktoba",
    "November": "Novemba",
    "December": "Disemba",
}

BEMBA_DAYS = {
    "Monday": "Palichimo",
    "Tuesday": "Palichibili",
    "Wednesday": "Palichitatu",
    "Thursday": "Palichine",
    "Friday": "Palichisano",
    "Saturday": "Pachibelushi",
    "Sunday": "Pa Mulungu",
}


def set_language(lang: str):
    global _current_lang
    _current_lang = lang


def get_language() -> str:
    return _current_lang


def tr(text: str) -> str:
    if _current_lang == BEMBA:
        return BEMBA_TRANSLATIONS.get(text, text)
    return text


def toggle_language() -> str:
    global _current_lang
    _current_lang = BEMBA if _current_lang == ENGLISH else ENGLISH
    return _current_lang


class LanguageSwitchButton(tk.Frame):
    def __init__(self, parent, on_switch, **kw):
        super().__init__(parent, bg="#16213e", cursor="hand2", **kw)
        self._on_switch = on_switch
        self.config(border=0, highlightthickness=1, highlightbackground="#2a2a3e")
        self._lbl = tk.Label(self, text="  \U0001F1FF\U0001F1F2  EN/BE", anchor="w",
                             bg="#16213e", fg="#e8e8e8", font=("Segoe UI", 10), padx=14, pady=8)
        self._lbl.pack(fill="both", expand=True)
        self._lbl.bind("<Button-1>", self._click)
        self.bind("<Button-1>", self._click)
        self.bind("<Enter>", lambda e: self.config(bg="#0f3460") or self._lbl.config(bg="#0f3460"))
        self.bind("<Leave>", lambda e: self.config(bg="#16213e") or self._lbl.config(bg="#16213e"))

    def _click(self, e):
        lang = toggle_language()
        self._lbl.config(text=f"  \U0001F1FF\U0001F1F2  {'BE' if lang == BEMBA else 'EN'}")
        self._on_switch()

    def update_label(self):
        lang = get_language()
        self._lbl.config(text=f"  \U0001F1FF\U0001F1F2  {'BE' if lang == BEMBA else 'EN'}")
