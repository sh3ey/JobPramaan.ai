import pandas as pd
from predict import predict_job_posting

# Load just the first row from the dataset
df = pd.read_csv("dataset/fake_job_postings.csv", nrows=1)
row = df.iloc[0]

text = f"{row['title']} {row['company_profile']} {row['description']} {row['requirements']}"

# Run prediction
result = predict_job_posting(text)

print("\n================ RAW OUTPUT DEBUG ================")
print("Return Value:", repr(result))
print("Return Type: ", type(result))
print("Actual Column Value in CSV:", repr(row['fraudulent']))
print("Actual Column Type:        ", type(row['fraudulent']))
print("==================================================\n")