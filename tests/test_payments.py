from sample_project.payments import Payment


def test_successful_payment():
    payment = Payment()

    result = payment.process_payment(101, 500)

    assert result == "Payment successful"


def test_invalid_payment():
    payment = Payment()

    result = payment.process_payment(101, 0)

    assert result == "Invalid payment amount"