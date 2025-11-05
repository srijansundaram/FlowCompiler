import pandas as pd

employees = pd.read_csv(r"datasets/employees.csv")
customers = pd.read_csv(r"datasets/customers.csv")

employees = employees.merge(customers, on="id", suffixes=("", "_right"))
employees.columns = [c.replace("_right", "") for c in employees.columns]
employees = employees[["id", "name", "city"]]
employees.to_csv(r"datasets/output_join.csv", index=False)