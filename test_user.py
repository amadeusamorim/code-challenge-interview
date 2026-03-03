import unittest
from user import User
from exceptions import PaymentException
from payment import Payment, FriendshipEvent

class TestPayments(unittest.TestCase):
    def setUp(self):
        self.bobby = User("Bobby")
        self.bobby.add_to_balance(5.00)
        self.bobby.add_credit_card("4111111111111111")
        self.carol = User("Carol")
        self.carol.add_to_balance(10.00)
        self.carol.add_credit_card("4242424242424242")

    def test_pay_with_balance(self):
        self.bobby.pay(self.carol, 5.00, "Coffee")
        self.assertEqual(self.bobby.balance, 0.00)
        self.assertEqual(self.carol.balance, 15.00)
    
    def test_pay_with_card(self):
        self.bobby.pay(self.carol, 10.00, "Lunch")
        self.assertEqual(self.bobby.balance, 5.00)
        self.assertEqual(self.carol.balance, 20.00)

    def test_returns_payment(self):
        payment = self.bobby.pay(self.carol, 5.00, "Coffee")
        self.assertIsInstance(payment, Payment)
        self.assertEqual(payment.amount, 5.00)

    def test_self_pay_raises(self):
        with self.assertRaises(PaymentException):
            self.bobby.pay(self.bobby, 5.00, "Nope")
    
    def test_negative_raises(self):
        with self.assertRaises(PaymentException):
            self.bobby.pay(self.carol, -1.00, "Nope")

    def test_zero_raises(self):
        with self.assertRaises(PaymentException):
            self.bobby.pay(self.carol, 0, "Nope")


class TestFriends(unittest.TestCase):
    def setUp(self):
        self.bobby = User("Bobby")
        self.carol = User("Carol")
    
    def test_bidirectional(self):
        self.bobby.add_friend(self.carol)
        self.assertIn(self.carol, self.bobby.friends)
        self.assertIn(self.bobby, self.carol.friends)

    def test_no_duplicate(self):
        self.bobby.add_friend(self.carol)
        self.bobby.add_friend(self.carol)
        self.assertEqual(len(self.bobby.friends), 1)

    def test_self_friend(self):
        self.bobby.add_friend(self.bobby)
        self.assertEqual(len(self.bobby.friends), 0)


class TestFeed(unittest.TestCase):
    def setUp(self):
        self.bobby = User("Bobby")
        self.bobby.add_to_balance(5.00)
        self.bobby.add_credit_card("4111111111111111")
        self.carol = User("Carol")
        self.carol.add_to_balance(10.00)
        self.carol.add_credit_card("4242424242424242")
    
    def test_payment_in_feed(self):
        self.bobby.pay(self.carol, 5.00, "Coffee")
        self.assertEqual(len(self.bobby.retrieve_feed()), 1)

    def test_payment_in_both_feeds(self):
        self.bobby.pay(self.carol, 5.00, "Coffee")
        self.assertEqual(len(self.carol.retrieve_feed()), 1)

    def test_friendshipp_in_feed(self):
        self.bobby.add_friend(self.carol)
        events = list(self.bobby.retrieve_feed())
        self.assertIsInstance(events[0], FriendshipEvent)
    
    def test_full_scenario(self):
        self.bobby.pay(self.carol, 5.00, "Coffee")
        self.carol.pay(self.bobby, 15.00, "Lunch")
        self.bobby.add_friend(self.carol)
        events = list(self.bobby.retrieve_feed())
        self.assertEqual(len(events), 3)
        self.assertIsInstance(events[0], Payment)
        self.assertIsInstance(events[1], Payment)
        self.assertIsInstance(events[2], FriendshipEvent)