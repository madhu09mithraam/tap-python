import csv

def read_csv(path: str) -> list[dict]:
    """
    Read a CSV file and return its contents as a list of dictionaries.
    """
    with open(path, "r", newline="", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)

    return data