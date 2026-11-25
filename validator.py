import pandas as pd
import logging
import yaml
import os
from datetime import datetime
from exceptions import (
    InputFileError,
    ConfigFileError,
    MissingColumnError,
    EmptyDataError
)
from manifest_manager import (
    load_manifest,
    save_manifest,
    is_file_already_processed,
    update_manifest
)
def setup_logging():

    # Create logs folder if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create log filename
    log_file = f"logs/pipeline_{timestamp}.log"

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ],
        force=True
    )

    logging.info("Pipeline logging started")

def load_config(config_path="config.yaml"):
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        if not config:
            raise ConfigFileError("Configuration file is empty.")

        logging.info("Configuration loaded successfully")
        return config

    except FileNotFoundError:
        raise ConfigFileError(
            f"Configuration file not found: {config_path}"
        )

    except yaml.YAMLError:
        raise ConfigFileError("Invalid YAML configuration.")


def read_orders_file(file_path):

    if not os.path.exists(file_path):
        raise InputFileError(
            f"Orders file not found: {file_path}"
        )

    try:
        df = pd.read_csv(file_path)

    except pd.errors.EmptyDataError:
        raise EmptyDataError("Orders CSV file is empty.")

    required_columns = ["order_id", "customer_id", "order_status"]
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise MissingColumnError(
            f"Missing required columns: {missing_columns}"
        )

    if df.empty:
        raise EmptyDataError("Orders dataset contains no records.")

    logging.info(f"Orders file loaded successfully: {len(df)} records")

    return df


def validate_orders(df):

    logging.info("Starting order validation")

    valid_statuses = [
        "delivered", "shipped", "canceled", "unavailable",
        "invoiced", "processing", "approved", "created"
    ]

    missing_order_id = df["order_id"].isnull()
    missing_customer_id = df["customer_id"].isnull()
    invalid_status = ~df["status"].isin(valid_statuses)

    invalid_condition = (
        missing_order_id |
        missing_customer_id |
        invalid_status
    )

    valid_records = df.loc[~invalid_condition].copy()
    bad_records = df.loc[invalid_condition].copy()

    logging.info(
        f"Validation completed | "
        f"Valid records: {len(valid_records)} | "
        f"Invalid records: {len(bad_records)}"
    )

    return valid_records, bad_records


def save_validation_results(valid_records, bad_records, config):

    clean_file = config["paths"]["clean_csv"]
    bad_file = "bad_records.csv"

    valid_records.to_csv(clean_file, index=False)
    logging.info(f"Valid records saved to {clean_file}")

    bad_records.to_csv(bad_file, index=False)
    logging.info(f"Invalid records saved to {bad_file}")


if __name__ == "__main__":

    setup_logging()

    try:
        config = load_config()

        orders_file = config["paths"]["orders"]
        manifest_file = config["paths"]["manifest"]

        # Load existing manifest
        manifest = load_manifest(manifest_file)

        # Check whether the file was already processed
        if is_file_already_processed(orders_file, manifest):

            print("\nFile already processed. Skipping pipeline execution.")

        else:
            # Read orders
            df = read_orders_file(orders_file)

            # Apply column mapping
            mapping = config.get("column_mapping", {}).get("orders", {})
            df = df.rename(columns=mapping)

            # Validate records
            valid_records, bad_records = validate_orders(df)

            # Save validation results
            save_validation_results(
                valid_records,
                bad_records,
                config
            )

            # Update manifest after successful processing
            update_manifest(
                orders_file,
                len(valid_records),
                manifest
            )

            print("\n========== VALIDATION SUMMARY ==========")
            print("Total records:", len(df))
            print("Valid records:", len(valid_records))
            print("Invalid records:", len(bad_records))
            print("\nValidation completed successfully!")

    except (InputFileError, ConfigFileError,
            MissingColumnError, EmptyDataError) as error:

        logging.error(f"Pipeline stopped safely: {error}")
        print("\nPipeline stopped safely.")
        print("Reason:", error)

    except Exception:
        logging.exception("Unexpected pipeline error occurred.")
        print("\nAn unexpected error occurred. Check the log file.")

    except (InputFileError, ConfigFileError,
            MissingColumnError, EmptyDataError) as error:

        logging.error(f"Pipeline stopped safely: {error}")
        print("\nPipeline stopped safely.")
        print("Reason:", error)

    except Exception:
        logging.exception("Unexpected pipeline error occurred.")
        print("\nAn unexpected error occurred. Check the log file.")