import joblib
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# NLTK Setup
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    cleaned_words = [lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words]
    return ' '.join(cleaned_words)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'best_model.pkl')
TFIDF_PATH = os.path.join(BASE_DIR, 'models', 'tfidf_vectorizer.pkl')

model = None
vectorizer = None

if os.path.exists(MODEL_PATH) and os.path.exists(TFIDF_PATH):
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(TFIDF_PATH)
    print("✅ Models loaded successfully!")
else:
    print(f"❌ Error: Models not found at {MODEL_PATH} or {TFIDF_PATH}")

def predict_job_posting(raw_text):
    if model is None or vectorizer is None:
        return {"is_fake": False, "probability_fake": None, "error": "Model files missing!"}
        
    text_lower = raw_text.lower()
    matched_reasons = []

    # 1. Off-Platform Contact & Messaging Apps
    if re.search(r"\b(telegram|whatsapp|signal)\b", text_lower):
        matched_reasons.append("Off-platform messaging requested (Telegram / WhatsApp / Signal)")

    if re.search(r'(?:dm|contact|telegram|whatsapp|reach|message)\s*(?:me|us|at)?\s*@\w+', text_lower) or re.search(r'@(?:telegram|t\.me|wa\.me|whatsapp|crypto_admin|hr_telegram)', text_lower):
        matched_reasons.append("Direct social or messaging handle requested (@)")

    if re.search(r"@gmail\.com|@yahoo\.com|@hotmail\.com", text_lower):
        matched_reasons.append("Generic personal email domain used instead of official corporate domain")

    # 2. Crypto & Financial Wire Triggers
    if re.search(r"\b(crypto|bitcoin|usdt)\b", text_lower):
        matched_reasons.append("Cryptocurrency payment or investment mentioned")

    # 3. Fake Check & Upfront Fee / Equipment Scam Signals
    if re.search(r"company check|check deposit|onboarding fee|equipment fee|equipment purchase|free laptop|home office setup|cashier check|wire money|send cash", text_lower):
        matched_reasons.append("Upfront equipment, check deposit, or registration fee requested")

    # 4. Unrealistic Salary for Zero Experience
    if re.search(r"\$\d{2,}\s*-\s*\$\d{2,}\s*per hour|\$\d{2,}/hr|\$\d{4,}\s*(per|a)\s*week", text_lower) and re.search(r"no experience|no prior experience|will train|flexible hours|data entry", text_lower):
        matched_reasons.append("Unrealistically high payout for entry-level or zero-experience role")

    # 5. Non-Standard / Text-Based Interview Process
    if re.search(r"text-based|text interview|instant interview|15 minutes interview", text_lower):
        matched_reasons.append("Non-standard hiring process (Text-based / Instant approval interview)")

    # 6. High Pressure Urgency Language
    if re.search(r"urgent hiring|start immediately|limited spots|immediate joining", text_lower):
        matched_reasons.append("High-pressure urgency language used to skip standard verification")

    # If any rule-based triggers hit, collect all reasons and return immediately!
    if len(matched_reasons) > 0:
        return {
            "is_fake": True,
            "probability_fake": 99.4,
            "reasons": matched_reasons
        }

    # Fallback to ML Model (Linear SVM / Model + TF-IDF)
    cleaned_input = clean_text(raw_text)
    vectorized_input = vectorizer.transform([cleaned_input])
    prediction = model.predict(vectorized_input)[0]
    
    probability = None
    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(vectorized_input)[0][1] * 100
    elif hasattr(model, "decision_function"):
        decision = model.decision_function(vectorized_input)[0]
        # Softmax approximation for decision boundary
        probability = round(100 / (1 + (2.718 ** -decision)), 2)
    else:
        probability = 95.0 if prediction == 1 else 5.0
        
    return {
        "is_fake": bool(prediction == 1),
        "probability_fake": round(probability, 2) if probability is not None else None,
        "reasons": ["Language patterns match high-risk fraudulent dataset entries"] if prediction == 1 else []
    }

if __name__ == "__main__":
    test_job = "URGENT HIRING! Work from home and earn $10000 per week. Send cash to register."
    result = predict_job_posting(test_job)
    print(f"\nPrediction Result: {result}")