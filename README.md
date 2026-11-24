# Olist Data Pipeline

## 1. Project Overview

The Olist Data Pipeline is a Python-based data processing project that focuses on reading, cleaning, transforming, and validating Olist datasets.

The project aims to improve data quality and ensure reliable data processing through configuration-driven operations, error handling, logging, and automated testing.

## 2. Project Objectives

- Read multiple Olist CSV datasets.
- Perform data cleaning and transformation.
- Validate data types and column values.
- Identify and handle invalid records.
- Support configuration-driven column mapping.
- Handle errors using custom exceptions.
- Maintain execution logs.
- Prevent duplicate processing using a manifest.
- Verify functionality through unit testing.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data manipulation and processing |
| NumPy | Numerical operations |
| PyYAML | Reading YAML configuration |
| Jupyter Notebook | Development and execution |
| Pytest | Unit testing |
| Git & GitHub | Version control |

## 4. Project Structure

The project follows a flat folder structure. All datasets, Python modules, configuration files, and notebooks are maintained in the main project directory.

```text
tap-python/
│
├── cleaned_orders.csv
├── customers.csv
├── customers_semicolon.csv
├── geolocation.csv
├── order_items.csv
├── order_payments.csv
├── order_reviews.csv
├── orders.csv
├── product_category_name_translation.csv
├── products.csv
├── sellers.csv
│
├── day11.ipynb
├── day12.ipynb
├── day13.ipynb
├── day14.ipynb
│
├── reader.py
├── transformer.py
├── validator.py
├── test_transformer.py
│
├── config.yaml
├── column_mapping.json
├── manifest.json
├── run_summary.json
├── schema.sql
│
├── README.md
└── requirements.txt
```

## 5. Prerequisites

Before running the project, make sure the following are installed:

- Python 3.11 or later
- Visual Studio Code
- Git
- Jupyter Notebook

## 6. Environment Setup

### Step 1: Clone the Repository

```bash
git clone <your-github-repository-url>
```

### Step 2: Navigate to the Project Directory

```bash
cd tap-python
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

For Command Prompt:

```cmd
venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

## 7. Dataset Information

The project uses the Brazilian Olist e-commerce dataset.

The datasets include:

| Dataset | Description |
|---|---|
| customers.csv | Customer information |
| orders.csv | Order details |
| order_items.csv | Individual order items |
| order_payments.csv | Payment information |
| order_reviews.csv | Customer reviews |
| products.csv | Product information |
| sellers.csv | Seller information |
| geolocation.csv | Geographic information |
| product_category_name_translation.csv | Product category translations |

Additional files:

- customers_semicolon.csv: Customer dataset with semicolon-separated values.
- cleaned_orders.csv: Cleaned order dataset.

All input CSV files are maintained in the project root directory.

## 8. Configuration Management

The project uses configuration files to manage processing requirements.

### config.yaml

Stores configurable pipeline settings such as:

- File paths.
- Validation thresholds.
- Processing settings.
- Logging settings.

### column_mapping.json

Maintains mappings between incoming dataset column names and standardized column names.

This helps adapt the pipeline when incoming column names change.

## 9. Running the Notebooks

### Step 1: Activate the Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 