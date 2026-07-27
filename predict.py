import joblib
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

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
    
    scam_triggers = [
        "telegram", "signal", "crypto", "bitcoin", "usdt", 
        "company check", "check deposit", "onboarding fee", "equipment fee", 
        "wire money", "whatsapp"
    ]
    
    matched_triggers = [word for word in scam_triggers if word in text_lower]
    
    if re.search(r'(?<!\w)@\w+', raw_text) and not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', raw_text):
        matched_triggers.append("username/handle (@)")
    
    if len(matched_triggers) >= 1:
        return {
            "is_fake": True,
            "probability_fake": 99.4,
            "reasons": matched_triggers
        }
        
    cleaned_input = clean_text(raw_text)
    vectorized_input = vectorizer.transform([cleaned_input])
    prediction = model.predict(vectorized_input)[0]
    
    probability = None
    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(vectorized_input)[0][1] * 100
    elif hasattr(model, "decision_function"):
        decision = model.decision_function(vectorized_input)[0]
        probability = 95.0 if decision > 0 else 5.0
    else:
        probability = 95.0 if prediction == 1 else 5.0
        
    return {
        "is_fake": bool(prediction == 1),
        "probability_fake": round(probability, 2) if probability is not None else None,
        "reasons": []
    }

if __name__ == "__main__":
    test_job = "URGENT HIRING! Work from home and earn $10000 per week. Send cash to register."
    result = predict_job_posting(test_job)
    print(f"\nPrediction Result: {result}")