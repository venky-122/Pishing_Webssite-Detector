# detector/views.py
from django.shortcuts import render
from django.conf import settings
import joblib
import pandas as pd
import os

# import same feature extraction utilities
from detector.feature_extraction import extract_features_from_url, FEATURE_COLUMNS

# load model bundle once at startup
MODEL_PATH = os.path.join(settings.BASE_DIR, "phishing_model_bundle.pkl")
bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
feature_columns = bundle["feature_columns"]

def home(request):
    return render(request, "home.html")

def check_url(request):
    result = None
    details = None
    if request.method == "POST":
        url = request.POST.get("url", "").strip()
        if url:
            feat_dict = extract_features_from_url(url)
            # create DataFrame in same column order
            df = pd.DataFrame([feat_dict])[feature_columns]
            pred = model.predict(df)[0]          # 1 => phishing, 0 => legitimate
            proba = model.predict_proba(df)[0]   # [prob_legit, prob_phish]

            if pred == 1:
                result = "⚠️ Phishing Website"
            else:
                result = "✅ Legitimate Website"

            details = {
                "features": feat_dict,
                "prediction": int(pred),
                "prob_legit": float(proba[0]),
                "prob_phish": float(proba[1])
            }

    return render(request, "home.html", {"result": result, "details": details})
