import pandas as pd

sales = pd.read_csv(r"datasets/sales.csv")

sales = pd.DataFrame([sales["amount"].sum()], columns=["amount"])
sales.to_csv(r"datasets/output_valid.csv", index=False)