import re
import json
from pathlib import Path
# Task 4: Convert column names into snake_case

def to_snake_case(column_name: str) -> str:
    """
    Convert a column name into snake_case format.
    """
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', column_name)
    name = re.sub(r'[^a-zA-Z0-9]+', '_', name)

    return name.strip('_').lower()


# Task 5: Column mapping dictionary

def load_column_mapping() -> dict[str, str]:
    """
    Load column mapping from a JSON configuration file.
    """
    config_path = Path(__file__).with_name("column_mapping.json")

    with open(config_path, "r", encoding="utf-8") as file:
        mapping = json.load(file)

    return mapping


column_mapping = load_column_mapping()

#task 6:

def convert_to_float(data: list[dict]) -> list[dict]:
    """
    Convert price and freight_value columns into float.
    """
    for row in data:
        row["price"] = float(row["price"])
        row["freight_value"] = float(row["freight_value"])

    return data

#task 7:

def calculate_order_totals(data: list[dict]) -> dict[str, float]:
    """
    Calculate the total amount for each order.
    """
    order_totals = {}

    for row in data:
        order_id = row["order_id"]

        total = row["price"] + row["freight_value"]

        if order_id in order_totals:
            order_totals[order_id] += total
        else:
            order_totals[order_id] = total

    return order_totals