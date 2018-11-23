# -*- coding: utf-8 -*-

from player import Player
from deck import Deck 
from deck import Set
from deck import Card

class NumberGame(object):
	"""docstring for NumberGame"""
	def __init__(self, arg):
		self.num_players = num_players

		
def main():
	print("Welcome to the Number Game! :D")
	num_players = input("Please enter the number of players for the game (including yourself): ")
	print("This will be a {}-player Number Game.".format(num_players))
	deck = Deck()
	deck.shuffle()
	dealt_cards = [deck.deal(1) for i in range(0, num_players)]
	dealt_cards_value_only = [card.top().rank for card in dealt_cards]

	# change this to randomize when I go
	myid = 0
	# for card in dealt_cards:
	# 	print("Dealt [ {}{}  ]".format(card.top().rank, card.top().suit))
	# dealt_cards = [Set(Card("❤️", 5)), Set(Card("❤️", 7)), Set(Card("❤️", 1))]
	all_players = [Player(i, dealt_cards[:i] + dealt_cards[(i+1):]) for i in range(0, num_players)]
	# TODO: check quad / triple / double
	total_ranks = count_uniq_ranks(dealt_cards_value_only)
	print "There is {} unique ranks in total.".format(total_ranks)
	all_players = [Player(i, dealt_cards[:i] + dealt_cards[(i+1):], total_ranks) for i in range(0, num_players)]

	for player in all_players:
		if player.get_id() == myid:
			print("You see {}".format([i.top().rank for i in dealt_cards[1:]]))
			guess = input("Enter your rank guess: ")
		else:
			guess = player.guess_rank()
		print("Player {} guessed their rank is {}.".format(player.get_id(), guess))
		update_player(all_players, player.get_id(), guess, None)

	for player in all_players:
		if player.get_id() == myid:
			value = input("Guess your value: ")
			rank = input("Guess your rank: ")
                # fix confusing rank terminology
		else:
			value, rank = player.guess_card()
		print ("Player {} guessed {} with a rank of {}.".format(player.get_id(), value, rank))
                print ("Player {} actually had {}".format(player.get_id(), dealt_cards[player.get_id()].top().rank))
		update_player(all_players, player.get_id(), rank, value)

def update_player(all_players, pid, rank, value):
	for player in all_players:
		player.update(pid, rank, value)

def count_uniq_ranks(dealt_cards_value_only):
	return len(list(set(dealt_cards_value_only)))


if __name__ == '__main__':
    main()
