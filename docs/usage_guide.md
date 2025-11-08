# Flow Compiler — Usage Guide (v1.2.3)

A lightweight data-pipeline compiler that turns `.flow` scripts into runnable Python (Pandas) pipelines.

---

## 1) Installation

### A. Local install (recommended during development)

```bash
# from the project root
pip install .
```

### B. Editable install (auto-picks up code changes)

```bash
pip install -e .
```

> After install, the `flowc` command becomes available globally.

---

## 2) Quick Start

### Create a Flow script

`examples/monthly_revenue.flow`

```text
load "datasets/sales.csv" as sales

pipeline monthly_revenue:
  sales |> filter region == "APAC"
       |> group_by month
       |> sum amount as revenue
       |> emit to "datasets/output_filter_sum.csv"
```

### Compile & Run

```bash
flowc examples/monthly_revenue.flow
```

Expected:

- A `generated_pipeline.py` file is created/overwritten.
- Output CSV written to the path declared in `emit`.

---

## 3) CLI Reference

```bash
flowc <file.flow> [--verbose] [--no-run]
```

- `--verbose` — prints internal compiler stages and extra diagnostics.
- `--no-run` — generates `generated_pipeline.py` but skips executing it.

Examples:

```bash
flowc examples/join_pipeline.flow --verbose
flowc examples/monthly_revenue.flow --no-run
```

---

## 4) Language Cheatsheet

```
load "<csv_path>" as <alias>

pipeline <name>:
  <alias> |> filter <expr>
          |> group_by <column>
          |> sum <column> [as <alias>]
          |> average <column> [as <alias>]
          |> dropduplicates [<column>]
          |> sortby <column> [desc]
          |> rename <old> to <new>
          |> select col1, col2, ...
          |> join <other_alias> on <column>
          |> ensure <condition>
          |> emit to "<csv_output_path>"
```

Notes:

- Expressions in `filter` use Pandas query syntax (e.g., `amount > 1000 and region == "APAC"`).
- `group_by` followed by `sum/average` will aggregate and reset index automatically.
- `select` accepts comma-separated column names.

---

## 5) Example: Join

`examples/join_pipeline.flow`

```text
load "datasets/employees.csv" as employees
load "datasets/customers.csv"  as customers

pipeline join_pipeline:
  employees |> join customers on id
            |> select id, name, city
            |> emit to "datasets/output_join.csv"
```

---

## 6) Typical Output Files

- `generated_pipeline.py` — auto-generated Python.
- Output CSVs at paths defined by `emit`.

---

## 7) Troubleshooting

**“Column 'X' not found”**

- The semantic checker validates columns before running. Check the CSV header.
- The error may include a suggestion (closest match).

**“Skipped execution due to incomplete or circular dependencies.”**

- One pipeline depends on the output of another that wasn’t generated.
- Fix pipeline order or remove circular references.

**Windows paths in `load`/`emit`**

- Prefer forward slashes or raw strings in CSV paths: `datasets/sales.csv`.

**Nothing happens on run**

- Ensure your script contains an `emit` step.
- Run with `--verbose` to see internal steps.

---

## 8) Versioning

- Compiler version: **v1.2.3 (Final Build)**
- See `docs/CHANGELOG.md` and `docs/test_results.md` for history and coverage.

---
