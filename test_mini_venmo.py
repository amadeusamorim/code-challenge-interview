import unittest
from mini_venmo import MiniVenmo
from user import User
from exceptions import CreditCardException

class TestCreateUser(unittest.TestCase):
    def setUp(self):
        self.venmo = MiniVenmo()

    def test_returns_user(self):
        user = self.venmo.create_user("Bobby", 5.00, "4111111111111111")
        self.assertIsInstance(user, User)

    def test_sets_balance(self):
        user = self.venmo.create_user("Bobby", 5.00, "4111111111111111")
        self.assertEqual(user.balance, 5.00)

    def test_sets_card(self):
        user = self.venmo.create_user("Bobby", 5.00, "4111111111111111")
        self.assertEqual(user.credit_card_number, "4111111111111111")

    def test_invalid_card_raises(self):
        with self.assertRaises(CreditCardException):
            self.venmo.create_user("Bobby", 5.00, "0000000000000000")