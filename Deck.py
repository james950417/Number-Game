# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 11:39:30 2018

@author: kopur
"""
import random

suits = ["hearts", "spades", "clubs", "diamonds"]
names = {'1':'ace', '11':'jack', '12':'queen', '13':'king', '14':'joker'}

""" Groundwork for a card class"""
class Card:
    def __init__(self, suit, rank):
        if rank not in range(0,14):
            raise TypeError("Rank must be an integer from 1 to 14. Rank was " + rank)
        if suit not in suits and suit != 'joker':
            raise TypeError("Suit must be hearts, spades, clubs or diamonds. Suit was " + suit)
        self.rank = rank
        self.suit = suit
        
    def name(self):
        if self.suit == 'joker':
            print("Joker")
        elif str(self.rank) in names:
            print(names[str(self.rank)] + " of " + self.suit)
        else:
            print(str(self.rank) + " of " + self.suit)
            

""" Groundwork for a deck class"""        
class Deck:
    def __init__(self, jokers = False):
        if jokers:
            self.cards = [Card(suit, rank) for rank in range(1,14) for suit in suits]
            self.cards.append(Card('joker', 0))
            self.cards.append(Card('joker', 0))
        else:
            self.cards = [Card(suit, rank) for rank in range(1,14) for suit in suits]
            
    def __getitem__(self, key):
        return self.cards[key]
    
    def flip(self):
        return self.cards.pop()
            
    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal(self, number):
        cards = self.cards[:number]
        self.cards = self.cards[number:]
        return Set(cards)
    
    def size(self):
        return len(self.cards)
    
""" Groundwork for a set class"""
class Set:
    def __init__(self, cards):
        if isinstance(cards, list):
            for x in cards:
                if not isinstance(x, Card):
                    raise TypeError("Contents of cards are not all Cards.")
            self.cards = cards
        else:
            if isinstance(cards, Card):
                self.cards = [cards]
            else:
                raise TypeError("Card is not a type Card")
    def __getitem__(self, key):
        return self.cards[key]
        
    def top(self):
        return self.cards[-1]
    
    def play(self, index):
        ret = Set([self.cards[i] for i in index])
        for x in ret:
            self.cards.remove(x)
        return ret
    
    def show(self):
        for x in self.cards:
            x.name()
    
    def sort(self):
        self.cards.sort(key=lambda x: (x.rank, x.suit))
        
    # merges two different Sets
    def append(self, a_set):
        for x in a_set.cards:
            self.cards.append(x)
        
    #Sums card in hand value
    def value(self):
        total = 0
        for x in self.cards:
            if x.rank <= 10:
                total = total + x.rank
            else:
                total = total + 10
        return total