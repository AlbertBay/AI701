import pandas as pd
from utils import decompile
import re as re
from collections import Counter
from sklearn.model_selection import train_test_split


df = pd.read_parquet("data/opcodes.parquet")

df["malicious"] = df["malicious"].astype(int)
df.drop(columns=["creation_bytecode"], inplace=True)
df = df[df.opcode.duplicated() == False]

print("Class balance", Counter(df.malicious))

X = df[["opcode"]]
y = df.malicious

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.40, random_state=42, stratify=y
)
X_test, X_val, y_test, y_val = train_test_split(
    X_test, y_test, test_size=0.30, random_state=42, stratify=y_test
)

print(f"Test - {Counter(y_test)}")
print(f"Val - {Counter(y_val)}")
print(f"Train - {Counter(y_train)}")


X_train["malicious"] = y_train
X_val["malicious"] = y_val
X_test["malicious"] = y_test

X_train.reset_index(drop=True).to_parquet("data/train.parquet")
X_val.reset_index(drop=True).to_parquet("data/val.parquet")
X_test.reset_index(drop=True).to_parquet("data/test.parquet")
