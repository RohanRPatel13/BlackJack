class card:
    def __init__(self,suit,val):
        self.suit = suit
        self.val = val

    def printCard(self):
        print(str(self.val) + " " + self.suit, end = "")