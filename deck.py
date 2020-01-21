import random

def buildDeck():
    deck = []
    suits = ['Clubs', 'Spades', 'Hearts', 'Diamonds']
    numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    for i in suits:
        for j in numbers:
            deck.append([j, i])
            
    random.shuffle(deck)
    return deck
