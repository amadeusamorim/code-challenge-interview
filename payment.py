import uuid
from datetime import datetime

class Payment:

    def __init__(self, amount, actor, target, note):
        self.id = str(uuid.uuid4())
        self.amount = float(amount)
        self.actor = actor
        self.target = target
        self.note = note
        self.created_at = datetime.now()

    
    def __repr__(self):
        return (
            f"Payment (id={self.id[:8]}, "
            f"{self.actor.username} -> {self.target.username}, "
            f"${self.amount:.2f}, '{self.note}')"
        )
