from Player import Player
from Deck import Deck


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
	for card in dealt_cards:
		print card.top().suit
		print card.top().rank
	all_players = [Player(i, dealt_cards[:i] + dealt_cards[(i+1):]) for i in range(0, num_players)]
	# TODO: check quad / triple / double

	for player in all_players:
		guess = player.guess_rank()
		print("Player {} guessed their rank is {}.".format(player.get_id(), guess))
		update_player(all_players, player.get_id(), guess, None)

	for player in all_players:
		rank, value = player.guess_card()
        print ("Player {} guessed {} with a rank {}.".format(player.get_id(), value, rank))
        update_player(all_players, player.get_id(), rank, value)






def update_player(all_players, pid, rank, value):
	for player in all_players:
		player.update(pid, rank, value)


if __name__ == '__main__':
    main()