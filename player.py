import random

class Player():
    def __init__(self, pid, others_cards, num_ranks):
        self.pid = pid
        self.num_ranks = num_ranks
        self.num_players = len(others_cards)
        self.ranges = self.create_ranges(others_cards)
        self.num_ranks = num_ranks
        # transform from cards to numbers
        cards_iter = iter(others_cards)
        self.others_cards_map = {}
        for i in xrange(self.num_players):
            if i != pid:
                self.others_cards_map[i] = next(cards_iter)
                
        self.others_cards = [i.top().rank for i in others_cards]
        self.others_cards.sort(reverse=True)
        self.others_ranges = self.initialize_others_ranges()

    def create_ranges(self, others_cards):
        ranges = [i for i in xrange(1, 14)]
        for i in others_cards:
            if i.top().rank in ranges:
                ranges.remove(i.top().rank)
        return ranges

    def initialize_others_ranges(self):
        for i in xrange(self.num_players):
            if i != self.pid:
                ah

    def get_id(self):
        return self.pid

    def update(self, player, rank, value):
        if player == self.pid:
            return
        # first pass
        # TODO: split up into two functions
        if not value:
            invalid = []
            if player in self.others_ranges:
                other_range = self.others_ranges.get(player)
            else:
                # TODO: initialize this in __init__
                self.others_ranges[player] = [i for i in xrange(1, 14)]
                for i in self.others_cards_map:
                    if i != player:
                        if self.others_cards_map[i] in self.others_ranges[player]:
                            self.others_ranges[player].remove(self.others_cards_map[i])

            for i in xrange(1, 14):
                hypo_ranks = self.infer_ranks(self.others_ranges[player], i)
                if rank not in hypo_ranks:
                    invalid.append(i)
            for i in invalid:
                if i in self.ranges: 
                    self.ranges.remove(i) 
        #TODO: add logic for matching vs. getting distinct (thus you can eliminate others or only match others)
        else:
            total_num = len(self.others_cards)+1
            above = rank-1
            below = total_num-rank
            num_above = 0
            for i in self.others_cards:
                if i > value:
                    num_above+=1
            # case: my card is below
            if num_above == above:
                for i in xrange(value, 14):
                    if i in self.ranges:
                        self.ranges.remove(i)
            # case: my card is above
            else:
                for i in xrange(1, value+1):
                    if i in self.ranges:
                        self.ranges.remove(i)
            
    def infer_ranks(self, input_range, val):
        ranges = list(input_range)
        if val in ranges:
            ranges.remove(val)
        max_length = 0
        max_ranges = []
        curr_length = 0
        prev = 0
        for i in ranges:
            if prev == i-1:
                curr_length+=1
            else:
                if curr_length > max_length:
                    max_ranges = [(prev-curr_length+1, prev)]
                    max_length = curr_length
                elif curr_length == max_length:
                    max_ranges.append((prev-curr_length+1, prev))
                curr_length = 1
            prev = i

        if curr_length > max_length:
            max_ranges = [(ranges[-1]-curr_length+1, ranges[-1])]
            max_length = curr_length
        elif curr_length == max_length:
            max_ranges.append((prev-curr_length+1, prev))

        ranks = []
        # print("Max ranges {}".format(max_ranges))
        for max_range in max_ranges:
            # print("Max range {}".format(max_range))
            num = max_range[1]
            rank = 1
            # need to  take into account val and others' cards minus the guy who updated
            # for i in self.others_cards-pid+val
            #     if num > i.top().rank:
            #         continue
            #     else:
            #         rank+=1
            if num <= val:
                rank+=1
            ranks.append(rank)
        return ranks

    # TODO: where to consider 7 (should be in both, which it might be already rn)
    def guess_rank(self):
        max_length = 0
        max_range = None
        sorted(self.ranges)
        curr_length = 0
        prev = 0
        for i in self.ranges:
            if prev == i-1:
                curr_length+=1
            else:
                if curr_length > max_length:
                    max_range = (prev-curr_length+1, prev)
                    max_length = curr_length
                curr_length = 1
            prev = i

        if curr_length > max_length:
            max_range = (self.ranges[-1]-curr_length+1, self.ranges[-1])
            max_length = curr_length

        num = max_range[1]
        return self.get_rank(num, self.others_cards)

    # input must be a list of numbers for 'others'
    def get_rank(self, card, others):
        others.sort(reverse=True)

        rank = 1
        for i in others:
            if card > i:
                return rank
            else:
                rank+=1
        return rank

    def guess_card(self):
        print("self.ranges when guessing card {}".format(self.ranges))
        card = random.choice(self.ranges)
        rank = self.get_rank(card, self.others_cards) 
        return card, rank
