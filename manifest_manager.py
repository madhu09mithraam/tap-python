import json
import os
import hashlib
import logging
from datetime import datetime


def calculate_file_hash(file_path):
    """Generate SHA-256 hash for a file."""

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def load_manifest(manifest_path="manifest.json"):
    """Load existing manifest."""

    if not os.path.exists(manifest_path):
        return {}

    with open(manifest_path, "r") as file:
        manifest = json.load(file)

    return manifest


def save_manifest(manifest, manifest_path="manifest.json"):
    """Save manifest information."""

    with open(manifest_path, "w") as file:
        json.dump(manifest, file, indent=4)

    logging.info("Manifest updated successfully")


def is_file_already_processed(file_path, manifest):
    """Check whether the file was already processed without changes."""

    file_name = os.path.basename(file_path)

    current_hash = calculate_file_hash(file_path)

    previous_details = manifest.get(file_name)

    if previous_details:
        previous_hash = previous_details.get("file_hash")

        if current_hash == previous_hash:
            logging.info(f"{file_name} is already processed. Skipping.")
            return True

    return False


def update_manifest(file_path, record_count, manifest):
    """Update manifest after successful processing."""

    file_name = os.path.basename(file_path)

    file_hash = calculate_file_hash(file_path)

    manifest[file_name] = {
        "file_hash": file_hash,
        "status": "completed",
        "records_processed": record_count,
        "last_processed": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    save_manifest(manifest)