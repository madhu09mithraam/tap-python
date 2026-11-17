#task 8:
from transformer import (
    to_snake_case,
    convert_to_float,
    calculate_order_totals
)

#to test snake_case function:
def test_to_snake_case():
    assert to_snake_case("Order ID") == "order_id"
    assert to_snake_case("CustomerName") == "customer_name"
    assert to_snake_case("Freight Value") == "freight_value"

#to test convert_to_float function:
def test_convert_to_float():
    data = [
        {
            "price": "250.50",
            "freight_value": "30.25"
        }
    ]

    result = convert_to_float(data)

    assert result[0]["price"] == 250.50
    assert result[0]["freight_value"] == 30.25

#to test calculate_order_totals function:
def test_calculate_order_totals():
    data = [
        {
            "order_id": "O101",
            "price": 100.0,
            "freight_value": 10.0
        },
        {
            "order_id": "O101",
            "price": 200.0,
            "freight_value": 20.0
        },
        {
            "order_id": "O102",
            "price": 300.0,
            "freight_value": 30.0
        }
    ]

    result = calculate_order_totals(data)

    assert result["O101"] == 330.0
    assert result["O102"] == 330.0