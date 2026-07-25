Markdown
# 🛡️ JobScamScore AI - Fake Job Posting Detection System

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_Framework-red.svg)
![NLTK](https://img.shields.io/badge/NLTK-NLP-green.svg)

An end-to-end Machine Learning and Natural Language Processing (NLP) pipeline designed to identify fraudulent job postings. This project features a robust classification model and a production-ready, dark-themed SaaS web interface.

---

## 🎯 Project Objective
With the rapid increase in online employment scams, this project aims to protect job seekers by developing a machine learning-based system capable of identifying fraudulent job postings. The system analyzes textual data (Job Descriptions, Requirements, Company Profiles) to classify postings as either **Legitimate** or **Fraudulent**. 

## ✨ Key Features
* **Advanced NLP Preprocessing:** Custom text cleaning pipeline handling HTML tags, URLs, Stopwords, and Lemmatization.
* **Feature Engineering:** Unstructured text transformed into numerical arrays using **TF-IDF Vectorization**.
* **Model Comparison:** Comprehensive evaluation across Logistic Regression, Naive Bayes, Linear SVM, and Random Forest.
* **Premium SaaS UI:** A custom-styled, dark-themed Streamlit web interface mimicking modern cybersecurity tools.

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

```text
Fake-Job-Detection/
│
├── dataset/
│   └── fake_job_postings.csv         # Original raw dataset
│
├── models/
│   ├── best_model.pkl                # Serialized ML model
│   └── tfidf_vectorizer.pkl          # Serialized TF-IDF Vectorizer
│
├── notebooks/
│   └── notebook.ipynb                # EDA, Data Cleaning, Model Training & Evaluation
│
├── app.py                            # Streamlit Web Application (Dark SaaS UI)
├── predict.py                        # Backend Inference & Preprocessing Script
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
⚙️ Installation & Usage
1. Clone the repository

Bash
git clone [https://github.com/yourusername/Fake-Job-Detection.git](https://github.com/yourusername/Fake-Job-Detection.git)
cd Fake-Job-Detection
2. Install Python Dependencies

Bash
pip install -r requirements.txt
3. Run the Web Application

Bash
streamlit run app.py
🔍 Model Interpretability & Limitations
How the Model Makes Decisions
The classification engine operates on the mathematical weights assigned by the TF-IDF Vectorizer. Words that are globally rare but frequent in specific documents are penalized or rewarded. The model associates high-risk weights with semantic patterns commonly used by scammers, such as "urgent hiring," "cash deposit," "no experience required," and unusual financial phrasing.

Real-World Limitations
False Positives on Enthusiastic Postings: The model may occasionally flag legitimate startup job postings as fraudulent if they use aggressive marketing language (e.g., "Urgent," "Hustle," "Unlimited earning").

Lack of Contextual Understanding: Since TF-IDF relies on word frequencies rather than the sequence of words, it might miss the deeper context that advanced deep learning models (like BERT) would catch.

Evolving Scam Patterns: Scammers continuously adapt their language. A static model will experience conceptual drift over time. To maintain accuracy, the model requires periodic retraining with newly identified fraudulent postings.

Developed as a capstone internship project focusing on Applied Machine Learning, NLP, and Software Deployment.