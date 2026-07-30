import pandas as pd
from predict import predict_job_posting

# Load a random batch of 100 samples
df = pd.read_csv("dataset/fake_job_postings.csv").sample(100, random_state=42)

correct = 0
total = len(df)

for idx, (_, row) in enumerate(df.iterrows()):
    # Clean text concatenation
    text = " ".join([
        str(row['title']) if pd.notna(row['title']) else "",
        str(row['company_profile']) if pd.notna(row['company_profile']) else "",
        str(row['description']) if pd.notna(row['description']) else "",
        str(row['requirements']) if pd.notna(row['requirements']) else ""
    ])
    
    # Run prediction
    result = predict_job_posting(text)
    
    # Extract prediction boolean
    predicted_is_fake = result.get('is_fake', False)
    
    # Actual value from dataset (1 = True, 0 = False)
    actual_is_fake = bool(row['fraudulent'] == 1)
    
    if predicted_is_fake == actual_is_fake:
        correct += 1

accuracy = (correct / total) * 100
print(f"\n✅ Batch Validation Complete!")
print(f"Correct Predictions: {correct} / {total}")
print(f"Batch Accuracy: {accuracy:.2f}%\n")