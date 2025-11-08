import pandas as pd

employees = pd.read_csv(r"datasets/employees.csv")
customers = pd.read_csv(r"datasets/customers.csv")

# ----- Pipeline: join_pipeline -----
join_pipeline = employees.copy()
join_pipeline = join_pipeline.merge(customers, on="id", how="inner")
join_pipeline = join_pipeline[["id", "name", "city"]]
join_pipeline.to_csv(r"datasets/output_join.csv", index=False)
print("📂 Output written to datasets/output_join.csv")