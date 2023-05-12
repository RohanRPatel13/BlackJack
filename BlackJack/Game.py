from Deck import deck
from Player import player

class bj:
    
    def __init__(self, numOfDecks, shuffles, numPlayers):
        self.d = deck(numOfDecks)
        self.d.shuffle(shuffles)
        dealer = player()
        self.players = []
        for i in range(numPlayers):
            newPlayer = player()
            self.players.append(newPlayer)
        self.players.append(dealer)
        self.players[len(self.players) - 1].dealer = True

    def deal(self):
        for i in range(2):
            for j in range(len(self.players)):
                if self.players[j].bet != 0 or self.players[j].dealer == True:
                    dealt = self.d.cards.pop(0)
                    self.players[j].hand.append(dealt)
        
    def hit(self, numPlayer):
        dealt = self.d.cards.pop(0)
        self.players[numPlayer].hand.append(dealt)
        return dealt
    
    def printHands(self):
        for i in range(len(self.players)):
            handLength = len(self.players[i].hand)
            if i == 0:
                print("Dealer: ", end = "")
            else:
                print("Player " + str(i) + ": ", end = "")
            for j in range(handLength):
                print(self.players[i].hand[j].val, end = ", ") 
            print("")
    