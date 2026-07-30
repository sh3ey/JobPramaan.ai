# 🛡️ JobPramaan.ai - Fake Job Posting Detection System

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_Framework-red.svg)
![NLTK](https://img.shields.io/badge/NLTK-NLP-green.svg)

An end-to-end Machine Learning and Natural Language Processing (NLP) pipeline designed to verify the authenticity of online job postings. **JobPramaan.ai** features a robust classification model paired with a Hybrid Rule Engine and a production-ready, dark-themed SaaS web interface.

---

## 🎯 Project Objective

With the rapid increase in online employment scams, **JobPramaan.ai** aims to protect job seekers by developing a machine learning-based system capable of identifying fraudulent job postings. The system analyzes textual data (*Job Descriptions, Requirements, Company Profiles*) to classify postings as either **Legitimate (Pramaan Verified)** or **Fraudulent**.

---

## ✨ Key Features

* **Advanced NLP Preprocessing:** Custom text cleaning pipeline handling HTML tags, URLs, Stopwords, and Lemmatization.
* **Feature Engineering:** Unstructured text transformed into numerical arrays using **TF-IDF Vectorization**.
* **Hybrid Rule & ML Engine:** Combines Machine Learning predictions with real-time heuristic keyword and regex detectors (catching Telegram handles, USDT/Crypto, and Check scams instantly).
* **Model Comparison:** Comprehensive evaluation across Logistic Regression, Naive Bayes, Linear SVM, and Random Forest.
* **Premium SaaS UI:** A custom-styled, dark-themed Streamlit web interface mimicking modern cybersecurity and verification tools.

---

## 📊 Dataset & Preprocessing

* **Dataset:** EMSCAD (Employment Scam Aegean Dataset) containing 17,880 real-world job postings.
* **Class Distribution:** Highly imbalanced (~95% Legitimate, ~5% Fraudulent).
* **Data Cleaning:**
  * Addressed missing values by imputing empty strings to preserve textual integrity.
  * Merged multiple textual attributes (`title`, `description`, `requirements`, `company_profile`) into a single consolidated feature.
  * Applied RegEx for noise reduction (removing punctuation, web links) and NLTK for tokenization and lemmatization.

---

## 🧠 Machine Learning & Evaluation

Due to the highly imbalanced nature of the dataset, **Accuracy is a misleading metric**. Therefore, the models were evaluated focusing on **F1-Score, Precision, and Recall**.

1. **Logistic Regression:** Great baseline, balanced weights handled the imbalanced classes well.
2. **Multinomial Naive Bayes:** Traditionally strong for text classification but struggled slightly with minority class recall.
3. **Linear SVM:** Achieved the best balance of Precision and Recall for the TF-IDF feature space.
4. **Random Forest:** Strong ensemble performance, though computationally heavier.

*Note: The best performing model (Linear SVM) and the fitted TF-IDF Vectorizer were serialized (`.pkl`) for production deployment.*

---

## 📂 Project Structure

    JobPramaan.ai/
    │
    ├── dataset/
    │   └── fake_job_postings.csv         # Original raw dataset
    │
    ├── models/
    │   ├── best_model.pkl                # Serialized ML model (Linear SVM)
    │   └── tfidf_vectorizer.pkl          # Serialized TF-IDF Vectorizer
    │
    ├── tests/                            
    │   ├── debug_single.py               # Debug script for individual text inputs
    │   ├── find_error.py                 # Error checking & edge-case diagnostic script
    │   └── test_batch.py                 # Batch testing script for model inference
    │
    ├── .gitattributes                    # Git configuration for path/text handling
    ├── .gitignore                        # Files and folders ignored by Git
    ├── app.py                            # Streamlit Web Application (Dark SaaS UI)
    ├── logo.png                          # Brand Logo & Favicon Asset
    ├── notebook.ipynb                    # EDA, Data Cleaning, Model Training & Evaluation
    ├── predict.py                        # Backend Inference, Preprocessing & Heuristic Script
    ├── README.md                         # Project documentation
    └── requirements.txt                  # Python dependencies

---

## ⚙️ Installation & Usage

1. **Clone the repository**
    ```bash
    git clone https://github.com/sh3ey/JobPramaan.ai.git
    
    cd JobPramaan.ai
    ```

2. **Install Python Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Web Application**
    ```bash
    streamlit run app.py
    ```

---

## 🔍 Model Interpretability & Limitations

### How the Model Makes Decisions
The classification engine operates on a hybrid approach:
* **Hybrid Triggers:** Scans for high-risk flags like off-platform handles, crypto payment requests, or fake equipment checks.
* **TF-IDF & Linear SVM:** Assigns mathematical weights to text patterns. Words globally rare but frequent in scam postings (e.g., *"urgent hiring"*, *"cash deposit"*, *"no experience required"*) boost the fraud probability score.

### Real-World Limitations
* **False Positives on Aggressive Postings:** Postings with heavy marketing jargon (*"Urgent"*, *"Unlimited earning"*) might occasionally raise flags.
* **Lack of Deep Sequence Context:** TF-IDF measures word frequency rather than sentence context (which transformers like BERT capture).
* **Evolving Scam Patterns:** Scammers adjust vocabulary over time, requiring periodic model retraining.

---

<p align="center">
  <i>Developed as part of an Internship Project, focusing on Applied Machine Learning, NLP Pipeline Engineering, and Interactive Software Deployment.</i>
</p>