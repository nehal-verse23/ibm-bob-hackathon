from sample_project.payments import Payment
from sample_project.users import User
from sample_project.notifications import Notification


class Order:
    def __init__(self, user_id, amount):
        self.user = User(user_id, "Test User")
        self.payment = Payment()
        self.notification = Notification()
        self.amount = amount

    def place_order(self):
        result = self.payment.process_payment(
            self.user.user_id,
            self.amount
        )

        if result == "Payment successful":
            self.notification.send_payment_notification(
                self.user.user_id,
                "Payment successful"
            )
            return "Order placed successfully"

        return "Order failed"