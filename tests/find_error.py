import pandas as pd
from predict import predict_job_posting

df = pd.read_csv("dataset/fake_job_postings.csv").sample(100, random_state=42)

for idx, (_, row) in enumerate(df.iterrows()):
    text = " ".join([
        str(row['title']) if pd.notna(row['title']) else "",
        str(row['company_profile']) if pd.notna(row['company_profile']) else "",
        str(row['description']) if pd.notna(row['description']) else "",
        str(row['requirements']) if pd.notna(row['requirements']) else ""
    ])
    
    result = predict_job_posting(text)
    predicted_is_fake = result.get('is_fake', False)
    actual_is_fake = bool(row['fraudulent'] == 1)
    
    # Print the misclassified post
    if predicted_is_fake != actual_is_fake:
        print("\n❌ MISCLASSIFIED SAMPLE FOUND:")
        print(f"Title: {row['title']}")
        print(f"Predicted Is Fake: {predicted_is_fake}")
        print(f"Actual Is Fake:    {actual_is_fake}")
        print(f"Confidence/Probability: {result.get('probability_fake')}%")
        print(f"Reasons: {result.get('reasons')}")
        print("-" * 50)
        print(f"Description snippet: {str(row['description'])[:300]}...\n")