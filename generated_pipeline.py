import pandas as pd

sales = pd.read_csv(r"datasets/sales.csv")

sales = pd.DataFrame([sales["revenue"].sum()], columns=["revenue"])
sales.to_csv(r"datasets/typo_output.csv", index=False)