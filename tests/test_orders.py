from sample_project.orders import Order


def test_order_placement():
    order = Order(101, 500)

    result = order.place_order()

    assert result == "Order placed successfully"