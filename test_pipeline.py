import pandas as pd
import json

from validator import validate_orders
from manifest_manager import (
    calculate_file_hash,
    save_manifest,
    load_manifest,
    is_file_already_processed
)


# TEST 1: Check valid records
def test_valid_records():

    df = pd.DataFrame({
        "order_id": ["A101"],
        "customer_id": ["C101"],
        "status": ["delivered"]
    })

    valid, bad = validate_orders(df)

    assert len(valid) == 1
    assert len(bad) == 0


# TEST 2: Check invalid records
def test_invalid_records():

    df = pd.DataFrame({
        "order_id": [None],
        "customer_id": ["C101"],
        "status": ["delivered"]
    })

    valid, bad = validate_orders(df)

    assert len(valid) == 0
    assert len(bad) == 1


# TEST 3: Check file hash generation
def test_file_hash(tmp_path):

    file = tmp_path / "sample.csv"
    file.write_text("order_id,status\nA101,delivered")

    file_hash = calculate_file_hash(str(file))

    assert len(file_hash) == 64


# TEST 4: Check manifest saving and loading
def test_manifest_save_load(tmp_path):

    manifest_file = str(tmp_path / "manifest.json")

    sample_manifest = {
        "orders.csv": {
            "status": "completed",
            "records_processed": 500
        }
    }

    save_manifest(sample_manifest, manifest_file)

    loaded_manifest = load_manifest(manifest_file)

    assert loaded_manifest == sample_manifest


# TEST 5: Check already processed file
def test_already_processed(tmp_path):

    file = tmp_path / "orders.csv"
    file.write_text("order_id,status\nA101,delivered")

    file_hash = calculate_file_hash(str(file))

    manifest = {
        "orders.csv": {
            "file_hash": file_hash,
            "status": "completed"
        }
    }

    result = is_file_already_processed(str(file), manifest)

    assert result is True