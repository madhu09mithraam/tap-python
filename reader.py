import pandas as pd
import glob
import os
import logging
import yaml


# --------------------------------
# STEP 1: LOAD CONFIGURATION
# --------------------------------

def load_config(config_path="config.yaml"):

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    logging.info("Configuration loaded successfully")

    return config


# --------------------------------
# STEP 2: READ ALL CSV FILES
# --------------------------------

def read_all_csv_files(directory=".", config_path="config.yaml"):

    dataframes = {}

    # Load configuration
    config = load_config(config_path)

    # Get column mappings
    column_mappings = config.get("column_mapping", {})

    # Find CSV files
    csv_files = glob.glob(os.path.join(directory, "*.csv"))

    if not csv_files:
        logging.warning("No CSV files found")
        return dataframes

    # Read each CSV file
    for file_path in csv_files:

        try:
            file_name = os.path.splitext(
                os.path.basename(file_path)
            )[0]

            logging.info(f"Reading file: {file_name}")

            # Read CSV
            df = pd.read_csv(file_path)

            # --------------------------------
            # STEP 3: APPLY COLUMN MAPPING
            # --------------------------------

            if file_name in column_mappings:

                mapping = column_mappings[file_name]

                df = df.rename(columns=mapping)

                logging.info(
                    f"Column mapping applied to {file_name}: {mapping}"
                )

            # Store DataFrame
            dataframes[file_name] = df

            logging.info(
                f"Successfully read {file_name} | "
                f"Rows: {len(df)} | Columns: {len(df.columns)}"
            )

        except Exception as e:

            logging.error(
                f"Failed to read {file_path}: {e}"
            )

    return dataframes


# --------------------------------
# STEP 4: EXECUTE THE PIPELINE
# --------------------------------

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Read all datasets
    datasets = read_all_csv_files()

    print("\n========== CSV READING SUMMARY ==========")

    for name, df in datasets.items():

        print(f"\nDataset: {name}")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

    print(
        "\nTotal CSV files successfully read:",
        len(datasets)
    )

    # --------------------------------
    # STEP 5: VERIFY COLUMN MAPPING
    # --------------------------------

    if "orders" in datasets:

        print("\n========== COLUMN MAPPING CHECK ==========")

        print("Orders dataset columns:")

        print(datasets["orders"].columns.tolist())