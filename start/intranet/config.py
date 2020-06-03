
class PlatesSet:
    front = ""
    rear = ""
    def __init__(self, front="", rear=""):
        self.front = front
        self.rear = rear
        self.full = f"{{front}}/{{rear}}"

