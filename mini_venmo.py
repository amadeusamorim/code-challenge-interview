from exceptions import PaymentException
from user import User
from payment import Payment

class MiniVenmo:
    def create_user(self, username: str, balance: float, credit_card_number: str) -> User:
        user = User(username)
        user.add_to_balance(balance)
        user.add_credit_card(credit_card_number)

        return user

    def render_feed(self, feed):
        for event in feed:
            if isinstance(event, Payment):
                print(
                    f"{event.actor.username} paid {event.target.username} "
                    f"${event.amount:.2f} for {event.note}"
                )
            elif isinstance(event, FriendshipEvent):
                print(
                    f"{event.user.username} and "
                    f"{event.new_friend.username} are now friends"
                )

    def add_friend(self, new_friend):
        if new_friend == self:
            return
        if new_friend not in self.friends:
            self.friends.append(new_friend)
            new_friend.friends.append(self)

    @classmethod
    def run(cls):
        venmo = cls()

        bobby = venmo.create_user("Bobby", 5.00, "4111111111111111")
        carol = venmo.create_user("Carol", 10.00, "4242424242424242")

        try:
            # should complete using balance
            bobby.pay(carol, 5.00, "Coffee")
 
            # should complete using card
            carol.pay(bobby, 15.00, "Lunch")
        except PaymentException as e:
            print(e)

        feed = bobby.retrieve_feed()
        venmo.render_feed(feed)

        bobby.add_friend(carol)