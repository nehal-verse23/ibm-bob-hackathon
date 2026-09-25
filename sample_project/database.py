class Database:
    def save_payment(self, user_id, amount):
        print(f"Payment of ₹{amount} saved for user {user_id}")

    def get_payment(self, user_id):
        return f"Payment history for user {user_id}"