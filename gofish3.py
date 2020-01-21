import random
import deck

class Player():
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.sets = []
        self.asked_cards = []

    def numsets(self):
        return len(self.sets)

    def cardsInHand(self):
        return len(self.hand)

def createPlayers():
    #initialize players, deal starting hand
    p1 = Player("Player 1")
    p2 = Player("Player 2")
    p3 = Player("Player 3")
    p4 = Player("Player 4")

    for i in range(0, 5):
        p1.hand.append(deck.pop())
        p2.hand.append(deck.pop())
        p3.hand.append(deck.pop())
        p4.hand.append(deck.pop())

    return p1, p2, p3, p4


#GLOBALS###
deck = deck.buildDeck()
p1, p2, p3, p4 = createPlayers()
players = [p1, p2, p3, p4]
###########

def addSets(p):
    global players
    dupeidx = getDupes(p)
    for idx in dupeidx:
        getBooks(p, idx)
    p.hand = [x for x in p.hand if x]
    
def get_all_indices(values, card):
    #return indices of duplicate cars in hand
    return [i for i in range(len(values)) if values[i] == card]

def print_board():
    global players
    #print out number of cards in each player's hand and in deck
    for p in players:
        if p.numsets() == 1:
            word = 'set'
        else:
            word = 'sets'
        print(f'{p.name} - {p.cardsInHand()} cards in hand.')
        print(f'           {p.numsets()} {word}.')

    print(f'\n{len(deck)} cards in deck.\n')

def getDupes(player):
    global players
    hand = player.hand
    sets = []
    values = [card[0] for card in hand]
    
    dupeidx = [get_all_indices(values, value) for value in values]
    dupeidx = [i for i in dupeidx if len(i) == 4]
    
    if len(dupeidx) > 0: #if there are any sets of 4
        temp = []
        for i in dupeidx:
            if i not in temp:
                temp.append(i)
        dupeidx = [x for x in temp]
    return dupeidx

def getBooks(p, idxs):
    global players
    tempsets = []
    for i in idxs:
        tempsets.append(p.hand[i])
        p.hand[i] = []
    p.sets.append(tempsets)


def goFish(p):
    global players
    #adds top card of deck to player's hand, if any cards are in the deck
    if deck:
        p.hand.append(deck.pop(0))

def PlayerCanGo(player):
    global players
    #makes sure that player has cards or can go fish to get a card.
    #otherwise, player is out.
    if player.cardsInHand() == 0:
        goFish(player)
    if player.cardsInHand() == 0:
        return False
    else:
        return True

def pick_card(p):
    global players
    #returns the face value of the card the player has the most copies of
    random.shuffle(p.hand)
    values = [card[0] for card in p.hand]
    max_idx = 0
    for i in range(len(values)):
        if values.count(values[i]) > max_idx:
            max_idx = i
    if p.hand[max_idx][0] not in p.asked_cards:
        p.asked_cards.append(p.hand[max_idx][0])
    return p.hand[max_idx][0]

def WhoToAsk(card, p):
    global players
    playerlist = [x for x in players if x.name != p.name]
    playerlist = [x for x in playerlist if x.cardsInHand() > 0]
    #playerlist is a list of players that aren't the current player
    for player in playerlist:
        if card in player.asked_cards:
            return player
    return random.choice(playerlist)

def removeFromAsked(asked_player, card):
    global players
    for i in range(len(asked_player.asked_cards)):
        if asked_player.asked_cards[i] == card:
            asked_player.asked_cards[i] = []
    asked_player.asked_cards = [x for x in asked_player.asked_cards if x]
        
def ask(asked_card, asked_player, p):
    global players
    #Requests a card from another player.
    card = asked_card
    numcards = 0
    tempcards = []
    values = [x[0] for x in asked_player.hand]
    match_idx = [i for i in range(len(values)) if values[i] == card]
    print(f'{p.name}: \"Hey {asked_player.name}, Got any {card}s?\"')
    if len(match_idx) > 0: #there is a match
        for i in match_idx:
            numcards += 1
            p.hand.append(asked_player.hand[i])
            asked_player.hand[i] = []
        asked_player.hand = [x for x in asked_player.hand if x]
        if numcards > 1:
            end = 's'
        else:
            end = ''
        print(f'{asked_player.name} hands over {numcards} {card}{end}')
        removeFromAsked(asked_player, card)
    else:
        print(f'{asked_player.name}: \"Go fish!\"')
        goFish(p)
            
def printWinners():
    global players
    print('Game over!\n')
    print('Final scores:\n')
    for p in players:
        print(f'{p.name} - {p.numsets()} sets.')
            

##MAIN GAME LOOP##
def game():
    global players
    numsets = 0
    for p in players:
        addSets(p)
        
    while numsets < 13:
        print_board()
        for p in players:
            if PlayerCanGo(p):
                asked_card = pick_card(p)
                asked_player = WhoToAsk(asked_card, p)
                ask(asked_card, asked_player, p)
                addSets(p)
        numsets = 0
        for p in players:
            numsets += p.numsets()

    printWinners()

game()

