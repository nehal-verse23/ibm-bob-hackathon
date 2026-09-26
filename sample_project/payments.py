from sample_project.database import Database


class Payment:
    def __init__(self):
        self.db = Database()

    def process_payment(self, user_id, amount):
        if amount <= 0:
            return "Invalid payment amount"

        self.db.save_payment(user_id, amount)
        return "Payment successful"
    # Payment processing updated