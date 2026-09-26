from unittest.mock import MagicMock

from sample_project.payments import Payment


def test_successful_payment():
    payment = Payment()

    result = payment.process_payment(101, 500)

    assert result == "Payment successful"


def test_invalid_payment():
    payment = Payment()

    result = payment.process_payment(101, 0)

    assert result == "Invalid payment amount"


def test_negative_payment_amount():
    payment = Payment()

    result = payment.process_payment(101, -50)

    assert result == "Invalid payment amount"


def test_save_payment_called_with_correct_args():
    payment = Payment()
    payment.db = MagicMock()

    payment.process_payment(101, 500)

    payment.db.save_payment.assert_called_once_with(101, 500)