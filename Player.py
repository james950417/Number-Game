class Player():
    def __init__(self, pid, others_cards):
        self.pid = pid
        self.num_players = len(others_cards)
        self.ranges = self.create_ranges(others_cards)
        print self.ranges
        self.others_cards = others_cards
        print self.others_cards[0].top().rank
        sorted(self.others_cards, reverse=True)
        self.others_ranges =[[]]

    def create_ranges(self, others_cards):
        ranges = [i for i in xrange(1, 14)]
        for i in others_cards:
            if i.top().rank in ranges:
                ranges.remove(i.top().rank)
        return ranges


    def get_id(self):
        return self.pid

    def update(self, player, rank, value):
        pass

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
                    max_range = (i-curr_length+1, i)
                    max_length = curr_length
                curr_length = 1
                prev = i

        if curr_length > max_length:
            max_range = (i-curr_length+1, i)
            max_length = curr_length

        num = max_range[1]
        rank = 1
        for i in self.others_cards:
            if num < i:
                return rank
            else:
                rank+=1
        return rank

    def guess_card(self):
        return None, None