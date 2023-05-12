from Cards import card
import random

class deck:
    cards = []
    
    def __init__(self, decks):
        #decks = number of decks used
        suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        for i in range(decks):
            for j in suits:
                for k in range(1,14):
                    self.cards.append(card(j,k))
        
    def shuffle(self, num):
        #num = number of shuffles
        for i in range(num):
            for j in range(len(self.cards)):
                rnd = random.randint(0,j)
                self.cards[j], self.cards[rnd] = self.cards[rnd], self.cards[j]

    def printDeck(self):
        for i in self.cards:
            i.printCard()
            print(", ", end = "")
        print("")