class player:
    #need to add chip amounts
    def __init__(self):
        self.hand = []
        self.values = [0,0]
        self.money = 1000
        self.bet = 0
        self.dealer = False

    #if first two are aces make one 11 and one 1
    #if there are two aces with another card that is a 10 or higher make both 1
    #if two aces with another card that is a 9 or lower make one 11 and one 1
    def addInitVals(self):
        if self.bet != 0 or self.dealer == True:
            #if two aces
            if self.hand[0].val == 1 and self.hand[1].val == 1:
                self.values[0] = 1
                self.values[1] = 11
                return sum(self.values)
            #if one ace and 10
            elif (self.hand[0].val == 1 and self.hand[1].val >= 10) or (self.hand[0].val >= 10 and self.hand[1].val == 1):
                self.values[0] = 11
                self.values[1] = 10
                return sum(self.values)
            #if one ace and number less than 10
            elif (self.hand[0].val == 1 and self.hand[1].val < 10) or (self.hand[0].val < 10 and self.hand[1].val == 1):
                value = self.hand[0].val
                if value == 1:
                    self.values[0] = 11
                    self.values[1] = self.hand[1].val
                else:
                    self.values[0] = self.hand[0].val
                    self.values[1] = 11
                return sum(self.values)
            #if 10 and other number
            elif (self.hand[0].val >= 10 and self.hand[1].val <= 9) or (self.hand[0].val <= 9 and self.hand[1].val >= 10) :
                value = self.hand[0].val
                if value >= 10:
                    self.values[0] = 10
                    self.values[1] = self.hand[1].val
                else:
                    self.values[0] = self.hand[0].val
                    self.values[1] = 10
                return sum(self.values)
            #if two 10s
            elif self.hand[0].val >= 10 and self.hand[1].val >= 10:
                self.values[0] = 10
                self.values[1] = 10
                return sum(self.values)
            else:
                self.values[0] = self.hand[0].val
                self.values[1] = self.hand[1].val
                return sum(self.values)
    
    #else is there are more than two aces check what values are with one ace that is 11 and the others as 1, if sum is greater than 21 than make all aces 1 and checksum again
    def addNextCard(self):
        Aces = self.values.count(1)
        Aces += self.values.count(11)
        if self.hand[len(self.hand) - 1].val == 1:
            Aces += 1
            if sum(self.values) <= 10:
                self.values.append(11)
            else:
                self.values.append(1)
            if sum(self.values) > 21 and Aces >= 2:
                self.replaceAces()
        elif self.hand[len(self.hand) - 1].val >= 10:
            self.values.append(10)
            if sum(self.values) > 21 and Aces >= 1:
                self.replaceAces()
        else:
            self.values.append(self.hand[len(self.hand) - 1].val)
            if sum(self.values) > 21 and Aces >= 1:
                self.replaceAces()
        return sum(self.values)
    
    def replaceAces(self):
        for i in range(len(self.values)):
            if self.values[i] == 11:
                self.values[i] = 1
     
    def sub(self, num):
        if self.bet - num >= 0:
            self.bet -= num
    
    def add(self, num):
        if self.bet + num <= self.money:
            self.bet += num
    
    def placeBet(self):
        self.money -= self.bet
    
    def giveWin(self):
        self.money += self.bet*2
    
    def givePush(self):
        self.money += self.bet

    def giveBlackJack(self):
        self.money += (self.bet + int(self.bet*(6/5)))

    def resetHand(self):
        self.bet = 0
        self.hand.clear()
        self.values = [0,0]