import boto3
import pandas as pd

BUCKET_NAME = "wasimkabucket"

s3 = boto3.client('s3')

print("Downloading dataset...")

s3.download_file(
    BUCKET_NAME,
    "dataset.csv",
    "dataset.csv"
)

df = pd.read_csv("dataset.csv")

new_id = len(df) + 1

df.loc[len(df)] = [
    new_id,
    f"Student{new_id}",
    20 + new_id
]

df.to_csv("dataset.csv", index=False)

print("Uploading updated dataset...")

s3.upload_file(
    "dataset.csv",
    BUCKET_NAME,
    "dataset.csv"
)

print("Completed")