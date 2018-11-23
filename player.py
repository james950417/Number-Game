import random

class Player():
    def __init__(self, pid, others_cards):
        self.pid = pid
        # self.num_ranks = num_ranks
        self.num_players = len(others_cards)+1
        self.ranges = self.create_ranges(others_cards)
        # transform from cards to numbers
        cards_iter = iter(others_cards)
        self.others_cards_map = {}
        for i in xrange(self.num_players):
            if i != pid:
                self.others_cards_map[i] = next(cards_iter).top().rank
                
        self.others_cards = [i.top().rank for i in others_cards]
        self.others_cards.sort(reverse=True)
        self.others_ranges = self.initialize_others_ranges()

    def create_ranges(self, others_cards):
        ranges = [i for i in xrange(1, 14)]
        for i in others_cards:
            if i.top().rank in ranges:
                ranges.remove(i.top().rank)
        return ranges

    # ranges are different depending on what they are trying to get (match or distinct)
    def initialize_others_ranges(self):
        others_ranges = {}
        for player in xrange(self.num_players):
            if player != self.pid:
                others_ranges[player] = [i for i in xrange(1, 14)]
                for other in self.others_cards_map:
                    if other != player:
                        if self.others_cards_map[other] in others_ranges[player]:
                            others_ranges[player].remove(self.others_cards_map[other])
        return others_ranges

    def get_id(self):
        return self.pid

    def update(self, player, rank, value):
        if player == self.pid:
            return
        # first pass
        # TODO: split up into two functions
        if not value:
            invalid = []
            other_range = self.others_ranges.get(player)

            # print("MY ID IS {}".format(self.pid))
            # print(other_range)
            # print(self.ranges)
            # for all my values
            # for i in xrange(1, 14):
            for i in self.ranges:
                # what would be his inferred rank
                hypo_ranks = self.infer_ranks(player, other_range, i)
                # print("rank {}".format(rank))
                # print("hypo_ranks {}".format(hypo_ranks))
                if rank not in hypo_ranks:
                    invalid.append(i)
            # print("invalid {}".format(invalid))
            # TODO: logic case -- they might saw a rank which is valid based on their logic but which results in my inferred rank not being correct. I need to trust their judgment. There needs to be accounting for this, but for now, I will ignore when this happens.
            if set(invalid) != set(self.ranges):
                for i in invalid:
                    if i in self.ranges: 
                        self.ranges.remove(i) 
            # print("MY ID IS {}".format(self.pid))
            # print(self.ranges)
            # print("\n\n\n\n")
        #TODO: add logic for matching vs. getting distinct (thus you can eliminate others or only match others)
        else:
            # all cards but his own
            total_num = len(self.others_cards)
            above = rank-1
            below = total_num-rank
            num_above = 0
            tmp_others_cards = list(self.others_cards)
            tmp_others_cards.remove(self.others_cards_map[player])
            tmp_others_cards.sort(reverse=True)
            for i in tmp_others_cards:
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
            
    def infer_ranks(self, player, input_range, val):
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
        temp_others_cards = list(self.others_cards)
        temp_others_cards.remove(self.others_cards_map[player])
        temp_others_cards.append(val)
        temp_others_cards.sort(reverse=True)
        # print("temp other cards {}".format(temp_others_cards))
        for max_range in max_ranges:
            num = max_range[1]
            rank = 1
            for i in temp_others_cards:
                if num > i:
                    continue
                else:
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
        # print("self.ranges when guessing card {}".format(self.ranges))
        card = random.choice(self.ranges)
        rank = self.get_rank(card, self.others_cards) 
        return card, rank
