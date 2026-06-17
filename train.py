import boto3
import pandas as pd
import pickle
import json

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

bucket = "jjtech-ai-bucket"

s3 = boto3.client("s3")

print("Downloading dataset...")

s3.download_file(
    bucket,
    "customer_data.csv",
    "customer_data.csv"
)

df = pd.read_csv("customer_data.csv")

X = df[["age", "salary"]]
y = df["bought"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LogisticRegression()

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(f"Accuracy = {accuracy}")

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("metrics.json", "w") as f:
    json.dump(
        {"accuracy": float(accuracy)},
        f
    )

print("Uploading model...")

s3.upload_file(
    "model.pkl",
    bucket,
    "models/model.pkl"
)

print("Uploading metrics...")

s3.upload_file(
    "metrics.json",
    bucket,
    "metrics/metrics.json"
)

print("Training completed")