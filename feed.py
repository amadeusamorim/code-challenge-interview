class Feed:

    def __init__(self, user):
        self.user = user
        self.events = []

    def add_event(self, event):
        self.events.append(event)
    
    def __len__(self):
        return len(self.events)
    
    def __iter__(self):
        return iter(self.events)