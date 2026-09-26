from unittest.mock import patch

from sample_project.orders import Order


def test_order_placement():
    order = Order(101, 500)

    result = order.place_order()

    assert result == "Order placed successfully"


def test_order_fails_on_invalid_payment():
    order = Order(101, 0)

    result = order.place_order()

    assert result == "Order failed"


def test_notification_sent_on_payment_success():
    order = Order(101, 500)

    with patch.object(order.notification, "send_payment_notification") as mock_notify:
        order.place_order()

    mock_notify.assert_called_once_with(101, "Payment successful")


def test_notification_not_sent_on_payment_failure():
    order = Order(101, 0)

    with patch.object(order.notification, "send_payment_notification") as mock_notify:
        order.place_order()

    mock_notify.assert_not_called()