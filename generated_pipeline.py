import pandas as pd

sales = pd.read_csv(r"datasets/sales.csv")

# ----- Pipeline: monthly_revenue -----
monthly_revenue = sales.copy()
monthly_revenue = monthly_revenue.query("region == "id",")
monthly_revenue = monthly_revenue.groupby("month").sum().reset_index()
monthly_revenue = pd.DataFrame([monthly_revenue["amount"].sum()], columns=["revenue"])
monthly_revenue.to_csv(r"datasets/output_filter_sum.csv", index=False)
print("📂 Output written to datasets/output_filter_sum.csv")