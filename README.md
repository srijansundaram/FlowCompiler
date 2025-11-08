<p align="center">
  <img src="docs/assets/flow-icon.svg" width="120" alt="Flow Compiler Logo"/>
</p>

<h1 align="center">Flow Compiler</h1>

<p align="center">
  <a href="https://github.com/srijansundaram/FlowCompiler/releases">
    <img src="https://img.shields.io/github/v/release/srijansundaram/FlowCompiler?color=brightgreen&label=Latest%20Release&logo=github" alt="Release Badge">
  </a>
  <a href="https://github.com/srijansundaram/FlowCompiler/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License Badge">
  </a>
  <a href="https://github.com/srijansundaram/FlowCompiler/actions">
    <img src="https://img.shields.io/badge/Build-Passing-brightgreen.svg" alt="Build Status Badge">
  </a>
</p>

---

## 💡 Overview

**Flow Compiler** is a lightweight **data pipeline compiler** that converts simple, human-readable `.flow` scripts into optimized **Python (Pandas)** code.

It supports:

- ✅ Dynamic syntax parsing
- 🧠 AI typo correction & suggestions
- ⚙️ Semantic validation
- 💬 Rich CLI feedback
- 🧾 CSV I/O and parallel pipelines

---

## 🚀 Features

| Category                 | Description                                                           |
| ------------------------ | --------------------------------------------------------------------- |
| 🧱 **Parser**            | Converts Flow syntax into AST structures                              |
| ⚙️ **Code Generator**    | Produces executable Pandas-based pipelines                            |
| 🧩 **Semantic Analyzer** | Detects undefined aliases, circular dependencies, and missing columns |
| 💡 **AI Hooks**          | Suggests corrections for typos and near-match commands                |
| 🧮 **CLI Integration**   | One-command compilation and execution with colored logs               |
| 🧾 **Emit System**       | Saves output CSVs with clear flow of data                             |
| 🔗 **Pipeline Chaining** | Supports one pipeline feeding into another (v1.2.2+)                  |
| 📦 **Final Build Ready** | Install globally via pip — no manual setup needed                     |

---

## 📦 Installation

### Option 1: Local (Development)

```bash
pip install .
```

### Option 2: Editable Install

```bash
pip install -e .
```

After installation, run:

```bash
flowc <path-to-your>.flow
```

---

## 🧰 Basic Usage

### Example: `examples/monthly_revenue.flow`

```text
load "datasets/sales.csv" as sales

pipeline monthly_revenue:
  sales |> filter region == "APAC"
        |> group_by month
        |> sum amount as revenue
        |> emit to "datasets/output_filter_sum.csv"
```

Run it:

```bash
flowc examples/monthly_revenue.flow
```

It automatically:

1. Generates a Python file `generated_pipeline.py`
2. Executes it
3. Outputs `datasets/output_filter_sum.csv`

---

## 🧠 Example Outputs

| Example File                    | Description                  | Output                           |
| ------------------------------- | ---------------------------- | -------------------------------- |
| `examples/join_pipeline.flow`   | Joins two datasets by `id`   | `datasets/output_join.csv`       |
| `examples/monthly_revenue.flow` | Sums revenue by region/month | `datasets/output_filter_sum.csv` |
| `examples/sales_summary.flow`   | Simple aggregation and sort  | `datasets/output_summary.csv`    |

---

## 📘 Documentation

| Resource                                       | Description               |
| ---------------------------------------------- | ------------------------- |
| [`docs/usage_guide.md`](docs/usage_guide.md)   | Full CLI and syntax guide |
| [`docs/CHANGELOG.md`](docs/CHANGELOG.md)       | Version history           |
| [`docs/test_results.md`](docs/test_results.md) | Test coverage and results |
| [`LICENSE`](LICENSE)                           | License details           |

---

## 🧪 Developer Notes

- Language: **Python 3.8+**
- Dependencies: `pandas`, `rich`
- Entry Command: `flowc`
- Tested OS: Windows 11, macOS, Ubuntu 22.04

---

## 🧭 Version History

| Version    | Date          | Highlights                                                |
| ---------- | ------------- | --------------------------------------------------------- |
| **v0.1**   | Nov 2, 2025   | Initial project setup and structure                       |
| **v0.2**   | Nov 3, 2025   | Parser & AST implementation — basic syntax understanding  |
| **v0.3**   | Nov 4, 2025   | Code Generator + CLI execution integrated                 |
| **v0.6**   | Nov 5, 2025   | AI Syntax Assistance & Auto-Correction (Hooks v1 & v2)    |
| **v0.9**   | Nov 6, 2025   | Semantic Validation — data-aware compiler intelligence    |
| **v1.2.2** | Nov 6–8, 2025 | Pipeline Chaining, Dependency Safety & CLI Enhancements   |
| **v1.2.3** | Nov 8, 2025   | Final Build — packaged, documented, stable public release |

---

## 👨‍💻 Author

**Srijan Sundaram**
📍 India
💼 [GitHub](https://github.com/srijansundaram)
📜 [VS Code Extension: Flow Language Support](https://marketplace.visualstudio.com/items?itemName=SrijanSundaram.flow-language-support)

---

## 🧾 License

Licensed under the **MIT License**.
See [`LICENSE`](LICENSE) for details.

---

## ⭐ Contributing & Feedback

Contributions are welcome!
You can:

- Submit issues and suggestions on [GitHub Issues](https://github.com/srijansundaram/FlowCompiler/issues)
- Fork and improve Flow Compiler
- Tag your stars ⭐ if you liked this project!

---

<p align="center">
  Made with ❤️ by <b>Srijan Sundaram</b>
</p>
