#import statements
import tkinter as tk
from tkinter import *
from tkinter import font as tkFont
import time
from PIL import Image, ImageTk
from Game import bj
from Deck import deck
import os

#Create tkinter window
my_w=tk.Tk()
my_w.geometry("1024x600")
my_w.title("BlackJack")
my_w.maxsize(1024,600)
my_w.minsize(1024,600)

icon = Image.open(str(os.getcwd()) + '\\Images\\BlackJack.jpg')
photo = ImageTk.PhotoImage(icon)
my_w.iconphoto(True, photo)


#Global Variables
pictures = []
fullDeck=Image.open(str(os.getcwd()) + '\\Images\\deck_of_cards.png')
backOfCard = Image.open(str(os.getcwd()) +  '\\Images\\back_of_card.png')
allChips=Image.open(str(os.getcwd()) + '\\Images\\chips.png')
back=ImageTk.PhotoImage(backOfCard.resize((100,150)))
canvasWidgets = []
canvasValues = []
buttons = []
chipsImage = []
chips = []
extraChips = []
moneyVals = []
numDecks = 4
numShuffles = 3
numPlayers = 4
gameDeck = bj(numDecks, numShuffles, numPlayers)

#card values: 0-12 = spades
#             13-25 = hearts
#             26-38 = diamonds
#             39-52 = clubs

#global functions

"""MOVE FUNCTIONS"""

#Purpose: Shows animation of card moving
#Parameter(s): img = the object to move
#              moveX = move on X axis
#              moveY = move on Y axis
def move(img, moveX, moveY):
    #moveY positive is down
    #moveY negative is up
    #moveX positive is right
    #moveX negative is left
    for x in range(0,60):
        canvas.move(img, moveX, moveY)
        my_w.update()
        #.006
        time.sleep(0.009)

#Purpose: Shows animation of chip moving
#Parameter(s): img = the object to move
#              moveX = move on X axis
#              moveY = move on Y axis
def moveFast(img, moveX, moveY):
    #moveY positive is down
    #moveY negative is up
    #moveX positive is right
    #moveX negative is left
    for x in range(0,60):
        canvas.move(img, moveX, moveY)
        my_w.update()
        #.006
        time.sleep(0.001)


"""IMAGE FUNCTIONS"""

#Purpose: Create images for each card and add them to pictures array to be used
#Parameter(s): None
def addCards():
    startXclose = 30
    startXfar = 390  
    startYclose = 30
    startYfar = 570

    moveX = 390
    moveY = 570

    for i in range(4):
        startXclose = 30
        startXfar = 390
        for j in range(13):
            card=fullDeck.resize((100,150),box=(startXclose,startYclose,startXfar,startYfar))
            startXclose += moveX
            startXfar += moveX

            card_img=ImageTk.PhotoImage(card)
            pictures.append(card_img)

        startYclose += moveY
        startYfar += moveY

#Purpose: Create images for each chip and add them to chipsImage array to be used
#Parameter(s): None
def addChips():
    startXclose = 228
    startXfar = 884  
    startYclose = 206
    startYfar = 863

    moveX = 806
    moveY = 805

    for i in range(2):
        startXclose = 228
        startXfar = 884
        for j in range(2):
            chip=allChips.resize((35,35),box=(startXclose,startYclose,startXfar,startYfar))
            startXclose += moveX
            startXfar += moveX

            chip_img=ImageTk.PhotoImage(chip)
            chipsImage.append(chip_img)

        startYclose += moveY
        startYfar += moveY


"""HELPER FUNCTIONS"""
#Purpose: Returns the index of a card's image in the pictures array
#Parameter(s): card = card object
def parseCard(card):
    result = -1
    val = card.val
    suit = card.suit
    if suit == "Spades":
        result = val - 1
    elif suit == "Hearts":
        result = val + 12
    elif suit == "Diamonds":
        result = val + 25
    elif suit == "Clubs":
        result = val + 38
    return result

"""RESET GAME FUNCTIONS"""

#Purpose: Reveals the dealer's card and score and gives cards to dealer until 17 or over
#Parameter(s): None
def reveal():
    dealerPos = len(gameDeck.players) - 1
    hiddenCard = parseCard(gameDeck.players[dealerPos].hand[1])
    cardBack = canvas.create_image(0,0, anchor=NW, image=pictures[hiddenCard])
    canvas.move(cardBack, 434, 66)
    canvasWidgets.append(cardBack)

    dealerScore()

    my_w.update()
    while sum(gameDeck.players[dealerPos].values) < 17:
        cardHit(dealerPos)
        updateDealerScore()

    giveMoney()
    reset()
    
#Purpose: Resets player turns for next round with delay
#Parameter(s): None
def reset():
    var = IntVar()
    my_w.after(3000, var.set, 1)
    my_w.wait_variable(var)

    for i in canvasWidgets:
        canvas.delete(i)
    for i in canvasValues:
        canvas.delete(i)
    for i in moneyVals:
        canvas.delete(i)
    for i in extraChips:
        canvas.delete(i)    
    for i in range(len(gameDeck.players)):
        gameDeck.players[i].resetHand()
    canvasWidgets.clear()
    canvasValues.clear()
    extraChips.clear()
    moneyVals.clear()

    money()
    my_w.update()
    
    #if all players have no money
    toEnd = [0, 0, 0, 0]
    for i in range(numPlayers):
        if gameDeck.players[i].money == 0:
            toEnd[i] = 1
    if sum(toEnd) == 4:
        endGame()

    #if deck has less than half the cards left from start, reshuffle the deck
    if len(gameDeck.d.cards) < (52*numDecks) // 2:
        gameDeck.d.cards.clear()
        gameDeck.d = deck(numDecks)
        gameDeck.d.shuffle(numShuffles)
 
    if sum(toEnd) != 4:
        betTurn(0)

#Purpose: Resets whole game for new setup without delay
#Parameter(s): None
def reset2():
    for i in canvasWidgets:
        canvas.delete(i)
    for i in canvasValues:
        canvas.delete(i)
    for i in moneyVals:
        canvas.delete(i)
    for i in extraChips:
        canvas.delete(i)    
    for i in range(len(gameDeck.players)):
        gameDeck.players[i].resetHand()
    canvasWidgets.clear()
    canvasValues.clear()
    extraChips.clear()
    moneyVals.clear()

    money()
    my_w.update()
    betTurn(0)

#Purpose: Asks player if they want to play again or quit game
#Parameter(s): None
def endGame():
    font = tkFont.Font(family='Helvetica', size=10, weight='bold')
    pOrQ = canvas.create_text(512, 200, anchor = CENTER, text="Play Again or Quit Game?", fill="white", font=('Helvetica 15 bold'))
    playAgain = Button(my_w, text='Play Again', width=10, height=1, anchor = CENTER, background='red', foreground='white', activebackground='dark red', activeforeground= 'white', command=lambda: [playAgain.destroy(), quit.destroy(), playGameAgain()])
    quit = Button(my_w, text='Quit', width=5, height=1, anchor = CENTER, background='red', foreground='white', activebackground='dark red', activeforeground= 'white', command=lambda: [my_w.quit()])
    playAgain.place(x=430,y=220)
    quit.place(x=530,y=220)

    playAgain['font'] = font
    quit['font'] = font

    canvasWidgets.append(pOrQ)

#Purpose: Sets game up to play again
#Parameter(s): None
def playGameAgain():
    global gameDeck
    gameDeck = bj(numDecks, numShuffles, numPlayers)
    reset2()


"""MONEY FUNCTIONS"""

#Purpose: Gives player money if they beat the dealer(6:5 for blackjack)
#Parameter(s): None
def giveMoney():
    #blackjack is defined as people with only 2 cards that add up to 21
    for i in range(numPlayers):
        #if player and dealer have blackjack give money back
        if sum(gameDeck.players[i].values) == 21 and len(gameDeck.players[i].values) == 2 and sum(gameDeck.players[len(gameDeck.players) - 1].values) == 21 and len(gameDeck.players[len(gameDeck.players) - 1].values) == 2:
            gameDeck.players[i].givePush()
        #if player has blackjack give 6:5 payout
        elif sum(gameDeck.players[i].values) == 21 and len(gameDeck.players[i].values) == 2:
            gameDeck.players[i].giveBlackJack()
        #if dealer busts
        elif sum(gameDeck.players[len(gameDeck.players) - 1].values) > 21:
            #if player has less than or equal to 21
            if sum(gameDeck.players[i].values) <= 21:
                gameDeck.players[i].giveWin()
        #if dealer is less than or equal to 21
        elif sum(gameDeck.players[len(gameDeck.players) - 1].values) <= 21:
            #if player is less than 21 and is greater than dealer give win
            if sum(gameDeck.players[i].values) <= 21 and sum(gameDeck.players[i].values) > sum(gameDeck.players[len(gameDeck.players) - 1].values):
                gameDeck.players[i].giveWin()
            #if player is less than 21 and is equal to dealer give push
            if sum(gameDeck.players[i].values) <= 21 and sum(gameDeck.players[i].values) == sum(gameDeck.players[len(gameDeck.players) - 1].values):
                gameDeck.players[i].givePush()

        gameDeck.players[i].bet = 0
        updateMoney(i)   
        
#Purpose: Display money and bet values of player
#Parameter(s): None
def money():
    x = 860
    for i in range(numPlayers):
        money = canvas.create_text(x, 550, anchor = CENTER, text="$" + str(gameDeck.players[i].money), fill="white", font=('Helvetica 15 bold'))
        bet = canvas.create_text(x-51, 304, anchor = CENTER, text="$" + str(gameDeck.players[i].bet), fill="white", font=('Helvetica 12 bold'))
        moneyVals.append(money)
        moneyVals.append(bet)
        x -= 240

#Purpose: Updates the money and bet values after a chip is added or removed
#Parameter(s): numPlayer = which player game is on
def updateMoney(numPlayer):
    canvas.itemconfig(moneyVals[numPlayer*2], text = "$" + str(gameDeck.players[numPlayer].money - gameDeck.players[numPlayer].bet))
    canvas.itemconfig(moneyVals[numPlayer*2+1], text = "$" + str(gameDeck.players[numPlayer].bet))

"""CARD TURN FUNCTIONS"""

#Purpose: Adds a card to player's hand
#Parameter(s): numPlayer = which player for card hit
def cardHit(numPlayer):
    gameDeck.hit(numPlayer)
    handLength = len(gameDeck.players[numPlayer].hand)

    Xcord = -1.5
    Ycord = 6
    #if dealer
    if numPlayer == len(gameDeck.players) - 1:
        Xcord = -8.5
        Ycord = .85
        for i in range(handLength - 1):
            Xcord += .75
    else:
        #place next card on stack
        for i in range(handLength - 1):
            Ycord -= .3
            Xcord += .25
        #place next card on player
        for i in range(numPlayer):
            Xcord -= 4

    nextCard = parseCard(gameDeck.players[numPlayer].hand[handLength-1])
    next = canvas.create_image(0,0, anchor=NW, image=pictures[nextCard])
    canvas.move(next, 900, 15)
    canvasWidgets.append(next)

    gameDeck.players[numPlayer].addNextCard()


    cardBack = canvas.create_image(0,0, anchor=NW, image=back)
    canvas.move(cardBack, 900, 15)
    move(next, Xcord, Ycord)

    if sum(gameDeck.players[numPlayer].values) == 21:
        nextTurn(numPlayer)

    if numPlayer != len(gameDeck.players) - 1:
        updateValues(numPlayer)
    my_w.update()

#Purpose: moves to next player's card turn
#Parameter(s): numPlayer = which player game is on
def nextTurn(numPlayer):
    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear()
    if numPlayer == len(gameDeck.players) - 2:
        reveal()
    else:
        cardTurn(numPlayer + 1)

#Purpose: Starts a players turn for hit or stand
#Parameter(s): numPlayer = which player game is on
def cardTurn(numPlayer):
    font = tkFont.Font(family='Helvetica', size=10, weight='bold')
    hit = Button(my_w, text='Hit', width=5, height=1, anchor = CENTER, background='red', foreground='white', activebackground='dark red', activeforeground= 'white', command=lambda: [hit.config(state="disabled"), cardHit(numPlayer), my_w.after(500, hit.config(state="active"))])
    stand = Button(my_w, text='Stand', width=5, height=1, anchor = CENTER, background='red', foreground='white', activebackground='dark red', activeforeground= 'white', command=lambda: [nextTurn(numPlayer)])
    buttons.append(hit)
    buttons.append(stand)
    
    #if dealer has blackjack then stop game and give pushes
    if sum(gameDeck.players[len(gameDeck.players) - 1].values) == 21:
        reveal()
    elif sum(gameDeck.players[numPlayer].values) == 21 or gameDeck.players[numPlayer].bet == 0:
        nextTurn(numPlayer)
    elif sum(gameDeck.players[numPlayer].values) != 21:
        hit['font'] = font
        stand['font'] = font
        if numPlayer == 0:
            hit.place(x=865, y=565)
            stand.place(x=805, y=565)
        elif numPlayer == 1:
            hit.place(x=628, y=565)
            stand.place(x=568, y=565)
        elif numPlayer == 2:
            hit.place(x=387, y=565)
            stand.place(x=327, y=565)
        elif numPlayer == 3:
            hit.place(x=147, y=565)
            stand.place(x=87, y=565)


"""CHIP FUNCTIONS"""

#Purpose: Places all chips for all players
#Parameter(s): None
def placeChips():
    chips.clear()
    x = 780
    for i in range(numPlayers):
        chip5Img = chipsImage[0]
        chip5 = canvas.create_image(x, 395, image=chip5Img)
        canvas.tag_bind(chip5, "<Button-1>", lambda event, i=i: moveChip(5, i), add='+')
        canvas.tag_bind(chip5, "<Button-1>", lambda event, i=i: updateMoney(i), add='+')
        chips.append(chip5)

        chip10Img = chipsImage[1]
        chip10 = canvas.create_image(x, 435, image=chip10Img)
        canvas.tag_bind(chip10, "<Button-1>", lambda event, i=i: moveChip(10, i), add='+')
        canvas.tag_bind(chip10, "<Button-1>", lambda event, i=i: updateMoney(i), add='+')
        chips.append(chip10)

        chip25Img = chipsImage[2]
        chip25 = canvas.create_image(x, 475, image=chip25Img)
        canvas.tag_bind(chip25, "<Button-1>", lambda event, i=i: moveChip(25, i), add='+')
        canvas.tag_bind(chip25, "<Button-1>", lambda event, i=i: updateMoney(i), add='+')
        chips.append(chip25)

        chip100Img = chipsImage[3]
        chip100 = canvas.create_image(x, 515, image=chip100Img)
        canvas.tag_bind(chip100, "<Button-1>", lambda event, i=i: moveChip(100, i), add='+')
        canvas.tag_bind(chip100, "<Button-1>", lambda event, i=i: updateMoney(i), add='+')
        chips.append(chip100)
        x -= 240

#Purpose: Moves chips to be bet or to be taken away from bet
#Parameter(s): chipVal = value of the chip to be moved
#              numPlayer = which player to add chips to
def moveChip(chipVal, numPlayer):
    x = 780
    for i in range(numPlayer):
        x -= 240

    if chipVal == 5:
        chipImg = chipsImage[0]
        moveY = -1
        y = 395
    elif chipVal == 10:
        chipImg = chipsImage[1]
        moveY = -1.659
        y = 435
    elif chipVal == 25:
        chipImg = chipsImage[2]
        moveY = -2.33
        y = 475
    elif chipVal == 100:
        chipImg = chipsImage[3]
        moveY = -2.9999
        y = 515

    if not(gameDeck.players[numPlayer].bet + chipVal > gameDeck.players[numPlayer].money):
        gameDeck.players[numPlayer].add(chipVal)
        chip = canvas.create_image(x, y, image=chipImg)
        canvas.tag_bind(chip, "<Button-1>", lambda event: moveFast(chip, -.5, moveY*-1))
        canvas.tag_bind(chip, "<Button-1>", lambda event, numPlayer=numPlayer: gameDeck.players[numPlayer].sub(chipVal), add='+')
        canvas.tag_bind(chip, "<Button-1>", lambda event, numPlayer=numPlayer: updateMoney(numPlayer), add='+')
        canvas.tag_bind(chip, "<Button-1>", lambda event: canvas.delete(chip), add='+')
        extraChips.append(chip)
        canvas.tag_bind(chip, "<Button-1>", lambda event: extraChips.remove(chip), add='+')
        moveFast(chip, .5, moveY)


#Purpose: Unbinds chip functions so they can't be moved after placing a bet
#Parameter(s): None
def setChips():
    for i in range(len(extraChips)):
        canvas.tag_unbind(extraChips[i], "<ButtonPress-1>")

"""BET FUNCTIONS"""

#Purpose: moves to next player's bet turn
#Parameter(s): numPlayer = which player to add chips to
def nextBet(numPlayer):
    for i in range(len(buttons)):
        buttons[i].destroy()
    buttons.clear() 
    if numPlayer == len(gameDeck.players) - 2:
        canvas.tag_unbind(chips[len(chips) - 4], "<ButtonPress-1>") #unbind action
        canvas.tag_unbind(chips[len(chips) - 3], "<ButtonPress-1>") #unbind action
        canvas.tag_unbind(chips[len(chips) - 2], "<ButtonPress-1>") #unbind action
        canvas.tag_unbind(chips[len(chips) - 1], "<ButtonPress-1>") #unbind action
        playGame()
    else:
        betTurn(numPlayer + 1)

#Purpose: Starts a players turn for betting
#Parameter(s): numPlayer = which player to add chips to
def betTurn(numPlayer):
    placeChips()
    font = tkFont.Font(size=12, weight='bold')
    check = Button(my_w, text='Place Bet', width=8, height=1, anchor = CENTER, background='red', foreground='white', activebackground='dark red', activeforeground= 'white', command=lambda: [setChips(), gameDeck.players[numPlayer].placeBet(), nextBet(numPlayer)])
    check['font'] = font
    buttons.append(check)

    index = 0
    for i in range(numPlayers):
        if numPlayer == 0:
            check.place(x=860, y=580, anchor = CENTER)
        elif numPlayer == 1:
            check.place(x=620, y=580, anchor = CENTER)
        elif numPlayer == 2:
            check.place(x=380, y=580, anchor = CENTER)
        elif numPlayer == 3:
            check.place(x=140, y=580, anchor = CENTER)
        
        if i != numPlayer:
            canvas.tag_unbind(chips[index], "<ButtonPress-1>") #unbind action
            canvas.tag_unbind(chips[index + 1], "<ButtonPress-1>") #unbind action
            canvas.tag_unbind(chips[index + 2], "<ButtonPress-1>") #unbind action
            canvas.tag_unbind(chips[index + 3], "<ButtonPress-1>") #unbind action
        index += 4

    if gameDeck.players[numPlayer].money == 0:
        nextBet(numPlayer)

"""PLAYER OUTCOME FUNCTIONS"""

#Purpose: Print "BlackJack!" if a player has blackjack
#Parameter(s): None
def printWins():
    for i in range(len(gameDeck.players) - 1):
        if sum(gameDeck.players[i].values) == 21:
            if i == 0:
                text = canvas.create_text(860, 580, anchor = CENTER, text="BlackJack!", fill="white", font=('Helvetica 15 bold'))
                canvasWidgets.append(text)
            elif i == 1:
                text = canvas.create_text(620, 580, anchor = CENTER, text="BlackJack!", fill="white", font=('Helvetica 15 bold'))
                canvasWidgets.append(text)
            elif i == 2:
                text = canvas.create_text(380, 580, anchor = CENTER, text="BlackJack!", fill="white", font=('Helvetica 15 bold'))
                canvasWidgets.append(text)
            elif i == 3:
                text = canvas.create_text(140, 580, anchor = CENTER, text="BlackJack!", fill="white", font=('Helvetica 15 bold'))
                canvasWidgets.append(text)

#Purpose: Print "Bust!" if a player busts
#Parameter(s): numPlayer = which player to print "Bust!" for
def printBust(numPlayer):
    if numPlayer == 0:
        text = canvas.create_text(860, 580, anchor = CENTER, text="Bust!", fill="white", font=('Helvetica 15 bold'))
        canvasWidgets.append(text)
    elif numPlayer == 1:
        text = canvas.create_text(620, 580, anchor = CENTER, text="Bust!", fill="white", font=('Helvetica 15 bold'))
        canvasWidgets.append(text)
    elif numPlayer == 2:
        text = canvas.create_text(380, 580, anchor = CENTER, text="Bust!", fill="white", font=('Helvetica 15 bold'))
        canvasWidgets.append(text)
    elif numPlayer == 3:
        text = canvas.create_text(140, 580, anchor = CENTER, text="Bust!", fill="white", font=('Helvetica 15 bold'))
        canvasWidgets.append(text)

#Purpose: Print player hand values
#Parameter(s): None
def printPlayerValues():
    for i in range(len(gameDeck.players) - 1):
            if sum(gameDeck.players[i].values) != 21:
                if i == 0:
                    text = canvas.create_text(940, 510, text = sum(gameDeck.players[i].values), fill="white", font=('Helvetica 15 bold'))
                    canvasValues.append(text)
                elif i == 1:
                    text = canvas.create_text(700, 510, text = sum(gameDeck.players[i].values), fill="white", font=('Helvetica 15 bold'))
                    canvasValues.append(text)
                elif i == 2:
                    text = canvas.create_text(460, 510, text = sum(gameDeck.players[i].values), fill="white", font=('Helvetica 15 bold'))
                    canvasValues.append(text)
                elif i == 3:
                    text = canvas.create_text(220, 510, text = sum(gameDeck.players[i].values), fill="white", font=('Helvetica 15 bold'))
                    canvasValues.append(text)
            else:
                canvasValues.append("")

#Purpose: Update player hand values
#Parameter(s): numPlayer = which player to update value for
def updateValues(numPlayer):
    canvas.itemconfig(canvasValues[numPlayer], text = sum(gameDeck.players[numPlayer].values))
    if sum(gameDeck.players[numPlayer].values) > 21:
        for i in range(len(buttons)):
            buttons[i].destroy()
        buttons.clear()
        printBust(numPlayer)
        nextTurn(numPlayer)

"""DEALER OUTCOME FUNCTIONS"""

#Purpose: Display dealer hand values
#Parameter(s): None
def dealerScore():
    text = canvas.create_text(370, 80, text = sum(gameDeck.players[len(gameDeck.players) - 1].values), fill="white", font=('Helvetica 15 bold'))
    canvasValues.append(text)

#Purpose: Update dealer hand values
#Parameter(s): None
def updateDealerScore():
    canvas.itemconfig(canvasValues[len(gameDeck.players) - 1], text = sum(gameDeck.players[len(gameDeck.players) - 1].values))


"""SETUP FUNCTIONS"""

#Purpose: Deal first two cards to everyone(including dealer), dealers 2nd card is hidden
#Parameter(s): None
def dealCards():
    posX = 2.5
    posY = 6
    for i in range(2):
        for j in range(len(gameDeck.players)):
            posX -= 4
            if gameDeck.players[j].bet != 0 or gameDeck.players[j].dealer == True:
                nextCardInt = parseCard(gameDeck.players[j].hand[i])
                if j == len(gameDeck.players) - 1 and i == len(gameDeck.players[j].hand) - 1:
                    next = canvas.create_image(0,0, anchor=NW, image=back)
                    posX = -7.75
                    posY = .85
                    canvasWidgets.append(next)
                elif j == len(gameDeck.players) - 1:
                    next = canvas.create_image(0,0, anchor=NW, image=pictures[nextCardInt])
                    posX = -8.5
                    posY = .85
                    canvasWidgets.append(next)
                else:
                    next = canvas.create_image(0,0, anchor=NW, image=pictures[nextCardInt])
                    canvasWidgets.append(next)
                canvas.move(next, 900, 15)

                cardBack = canvas.create_image(0,0, anchor=NW, image=back)
                canvas.move(cardBack, 900, 15)
                canvasWidgets.append(cardBack)

                move(next, posX, posY)
        posX = 2.75
        posY = 5.7

#Purpose: Play the game
#Parameter(s): none
def playGame():
    gameDeck.deal()
    dealCards()
    for i in range(len(gameDeck.players)):
        gameDeck.players[i].addInitVals()
    printWins()
    printPlayerValues()
    cardTurn(0)


"""START MAIN"""
#initial setup
addCards()
addChips()
canvas = Canvas(my_w, width=1024, height=600)
canvas.grid(row = 0, column = 0)

#background setup
background=Image.open(str(os.getcwd()) + '\\Images\\background.jpg')
bground =ImageTk.PhotoImage(background.resize((1024,600))) 
bg = canvas.create_image(512,300, anchor=CENTER, image=bground)

cardBack = canvas.create_image(0,0, anchor=NW, image=back)
canvas.move(cardBack, 900, 15)

brdr = Image.open(str(os.getcwd()) + '\\Images\\border.png')
bord = ImageTk.PhotoImage(brdr.resize((110,160)))
#dealerBord = ImageTk.PhotoImage(brdr.resize((200,160)))

chipbrdr = Image.open(str(os.getcwd()) + '\\Images\\chipBorder.png')
chipBorder =ImageTk.PhotoImage(chipbrdr.resize((45,45)))

x = 860
for i in range(numPlayers):
    border = canvas.create_image(x,450, anchor=CENTER, image=bord)
    chipBord = canvas.create_image(x-50,335, anchor=CENTER, image=chipBorder)
    x -= 240

#dealerBorder = canvas.create_image(300,200, anchor=CENTER, image=dealerBord)

money()

#start game
betTurn(0)

my_w.mainloop()
