import random
import re

class Deck():
  '''The deck helps us play the game'''
  def __init__(self):
    '''Makes a new deck and shuffles it, sets the location index to 0'''
    self.cards = range(52)
    self.drawn = 0
    random.shuffle(self.cards)

  def draw(self,n=1):
    '''Draws n cards from the deck. Default is one'''
    drew = self.cards[self.drawn:self.drawn+n]
    self.drawn += n
    return drew

  def shuffle(self):
    random.shuffle(self.cards)
    self.drawn = 0

class Hand():
  def __init__(self,hole):
    '''This is PLO so we draw 4 cards to begin with'''
    self.hole = hole
    self.community = []

  def add_community(self,new):
    '''Adds one or more newly dealt community cards'''
    self.community += new

  def _card_rk_st(self,card):
    '''Returns the rank and suit of the card (rank,suit) as a tuple of numbers (A is 13)'''
    return (card/4 if card/4 != 0 else 13,card%4)

  # The following methods are to determine the rank of a hand.
  # They should not be called.
  def _is_straight(self,cards):
    '''Returns if the hand is a straight'''
    card_ranks = map(lambda c: self._card_rk_st(c)[0],cards)
    card_ranks.sort(reverse=True)
    if card_ranks[0] == 13 and card_ranks[-1] == 1:
      # Straight to Ace
      card_ranks[0] = 0
      card_ranks.sort(reverse=True)
    for i in xrange(4):
      if card_ranks[i] - 1 != card_ranks[i+1]:
        return False
    return card_ranks

  def _is_flush(self,cards):
    '''Returns if the hand is a flush'''
    card_suits = map(lambda c: self._card_rk_st(c)[1],cards)
    for i in xrange(4):
      if card_suits[0] != card_suits[i+1]:
        return False
    card_ranks = map(lambda c: self._card_rk_st(c)[0],cards)
    card_ranks.sort(reverse=True)
    return card_ranks

  def _is_straight_flush(self,cards):
    '''Returns if the hand is a straight flush'''
    s = self._is_straight(cards)
    if s and self._is_flush(cards):
      return s

  def _is_quad(self,cards):
    '''Returns if the hand is a 4 of a kind'''
    card_ranks = map(lambda c: self._card_rk_st(c)[0],cards)
    card_ranks.sort(reverse=True)
    for i in xrange(2):
      if card_ranks[i] == card_ranks[i+1] and card_ranks[i] == card_ranks[i+2] and card_ranks[i] == card_ranks[i+3]:
        # There is a quad
        if i == 0:
          return card_ranks
        return card_ranks[1:] + card_ranks[:1]
    return False

  def _is_trip(self,cards):
    '''Returns if the hand is a 3 of a kind'''
    card_ranks = map(lambda c: self._card_rk_st(c)[0],cards)
    card_ranks.sort(reverse=True)
    for i in xrange(3):
      if card_ranks[i] == card_ranks[i+1] and card_ranks[i] == card_ranks[i+2]:
        # There is a trip
        if i == 0:
          return card_ranks
        if i == 1:
          return card_ranks[i:i+3] + card_ranks[:1] + card_ranks[-1:]
        return card_ranks[i:] + card_ranks[:2]
    return False

  def _is_two_pair(self,cards):
    '''Returns if the hand is a 2 pair'''
    card_ranks = map(lambda c: self._card_rk_st(c)[0],cards)
    card_ranks.sort(reverse=True)
    # only 3 configurations of two pairs
    if card_ranks[0] == card_ranks[1] and card_ranks[2] == card_ranks[3]:
      return card_ranks
    if card_ranks[0] == card_ranks[1] and card_ranks[3] == card_ranks[4]:
      return card_ranks[:2] + card_ranks[3:] + card_ranks[2:3]
    if card_ranks[1] == card_ranks[2] and card_ranks[3] == card_ranks[4]:
      return card_ranks[1:] + card_ranks[:1]
    return False

  def _is_pair(self,cards):
    '''Returns if the hand is a pair'''
    card_ranks = map(lambda c: self._card_rk_st(c)[0],cards)
    card_ranks.sort(reverse=True)
    for i in xrange(4):
      if card_ranks[i] == card_ranks[i+1]:
        return card_ranks[i:i+2] + card_ranks[0:i] + card_ranks[i+2:]
    return False
  
  def _is_full_house(self,cards):
    '''Returns if the hand is a full house'''
    trip = self._is_trip(cards)
    if not trip:
      return False
    if trip[-1] == trip[-2]:
      return trip
    return False

  def _rank_hand(self,cards):
    '''Returns a tuple of the rank of the hand and the list of cards for ordered comparisons'''
    sf = self._is_straight_flush(cards)
    if sf:
      return (8,sf)

    q = self._is_quad(cards)
    if q:
      return (7,q)

    fh = self._is_full_house(cards)
    if fh:
      return (6,fh)

    f = self._is_flush(cards)
    if f:
      return (5,f)

    s = self._is_straight(cards)
    if s:
      return (4,s)

    t = self._is_trip(cards)
    if t:
      return (3,t)

    tp = self._is_two_pair(cards)
    if tp:
      return (2,tp)

    p = self._is_pair(cards)
    if p:
      return (1,p)

    card_ranks = map(lambda c: self._card_rk_st(c)[0],cards)
    card_ranks.sort(reverse=True)
    return (0,card_ranks)


  def rank_holding(self):
    '''Ranks your hand as a tuple'''
    best_type = -1
    best_rank = None
    best_cards = None

    # 3 cards from community and 2 cards from your hand
    clength = len(self.community)
    for i in xrange(0,clength-2):
      for j in xrange(i+1,clength-1):
        for k in xrange(j+1,clength):
          for l in xrange(0,3):
            for m in xrange(l+1,4):
              curr = [self.community[i],self.community[j],self.community[k],self.hole[l],self.hole[m]]
              rk = self._rank_hand(curr)
              if rk[0] > best_type:
                best_type = rk[0]
                best_rank = rk[1]
                best_cards = curr
              elif rk[0] == best_type:
                best = True
                for p in xrange(5):
                  if rk[1][p] < best_rank[p]:
                    best = False
                    break
                  if best:
                    best_type = rk[0]
                    best_rank = rk[1]
                    best_cards = curr

    return best_type,best_rank,best_cards

  def print_card(self,card):
    rk,st = self._card_rk_st(card)
    s = ''
    if st == 0:
      s += '\033[32m'
    if st == 1:
      s += '\033[36m'
    if st == 2:
      s += '\033[31m'
    if st == 3:
      s += '\033[35m'

    if rk == 13:
      s += 'A'
    if rk == 12:
      s += 'K'
    if rk == 11:
      s += 'Q'
    if rk == 10:
      s += 'J'
    if rk == 9:
      s += 'T'
    if rk == 8:
      s += '9'
    if rk == 7:
      s += '8'
    if rk == 6:
      s += '7'
    if rk == 5:
      s += '6'
    if rk == 4:
      s += '5'
    if rk == 3:
      s += '4'
    if rk == 2:
      s += '3'
    if rk == 1:
      s += '2'
    if rk == 0:
      s += 'A'

    if st == 0:
      s += 'c'
    if st == 1:
      s += 'd'
    if st == 2:
      s += 'h'
    if st == 3:
      s += 's'

    s += '\033[37m '
    return s
    
  def print_cards(self,cards):
    if cards == []:
      return ''
    return reduce(lambda a,b: a+b,map(self.print_card,cards))

  def __str__(self):
    s =  'Community:   '
    s += self.print_cards(self.community)
    s += '\n'
    s += 'Hole:        '
    s += self.print_cards(self.hole)
    return s
    
  def __cmp__(self,h2):
    my_rank = self.rank_holding()
    h2_rank = h2.rank_holding()

    if my_rank[0] > h2_rank[0]:
      return 1
    elif my_rank[0] < h2_rank[0]:
      return -1

    for i in xrange(len(my_rank[1])):
      if my_rank[1][i] > h2_rank[1][i]:
        return 1
      elif my_rank[1][i] < h2_rank[1][i]:
        return -1

    return 0

  # End of class

class CallStation():
  '''Literal calling station AI'''
  def __init__(self):
    pass

  def play(self,game):
    return game.xc

class Player():
  def __init__(self,stack,player_type,ai=None):
    self.player_type = player_type
    self.stack = stack
    if ai is None:
      ai = CallStation()
    self.ai = ai

    # Set by game
    self.hand = None
    self.bet = 0.

class Game():
  '''This is the game class. Every time you play a game, you will initialize this class'''
  def __init__(self,p0=100.,p1=100.,bb=1.,rake=.05,max_rake=.625,p0type=0,p1type=1,p0ai=None,p1ai=None):
    '''Initializes a game with an AI and a player. Human player is p1 and AI is p0'''
    self.p0 = Player(p0,p0type,ai=p0ai)
    self.p1 = Player(p1,p1type,ai=p1ai)
    self.players = [self.p0,self.p1]
    self.bb = bb

    self.deck = Deck()
    self.community = []

    self.rake = rake
    self.max_rake = max_rake

    self.btn = random.randint(0,1)
    self.action = self.btn
    self.last_action = None
    self.pot = 0.

  def xc(self,pl):
    opp = self.players[(pl + 1) % 2]
    pl = self.players[pl]
    amt2call = opp.bet - pl.bet

    if amt2call > pl.stack:
      # opp.bet = pl.stack + pl.bet
      diff = opp.bet - pl.stack - pl.bet
      opp.bet -= diff
      opp.stack += diff
    
    pl.stack -= opp.bet - pl.bet
    pl.bet = opp.bet
    return 'xc'


  def br(self,pl,amt='pot'):
    # self.last_action = pl
    opp = self.players[(pl + 1) % 2]
    pl = self.players[pl]
    amt2call = opp.bet - pl.bet
    pot = 2 * opp.bet + self.pot
    if amt == 'pot':
      amt = pot
    if amt > pl.stack:
      amt = pl.stack
    if amt > pot:
      amt = pot
    pl.stack -= amt
    pl.bet += amt
    return 'br'

  def f(self,pl):
    opp = self.players[(pl + 1) % 2]
    pl = self.players[pl]
    prerake_pot = opp.bet + self.pot + pl.bet
    if opp.bet <= pl.bet:
      # Check if no bet
      return 'xc'
    if len(pl.hand.community) > 0:
      raked_pot = max(prerake_pot * (1. - self.rake), prerake_pot - self.max_rake)
    else:
      raked_pot = prerake_pot
    opp.stack += raked_pot
    opp.bet = 0.
    self.pot = 0.
    self.bet = 0.
    return 'f'

  def blinds(self):
    if self.btn == 0:
      self.p0.stack -= .5 * self.bb
      self.p1.stack -= 1. * self.bb
      self.p0.bet = .5 * self.bb
      self.p1.bet = 1. * self.bb
    else:
      self.p1.stack -= .5 * self.bb
      self.p0.stack -= 1. * self.bb
      self.p1.bet = .5 * self.bb
      self.p0.bet = 1. * self.bb
    return

  def deal_hole(self):
    self.p0.hand = Hand(self.deck.draw(4))
    self.p1.hand = Hand(self.deck.draw(4))

  def deal_community(self,n=1):
    new_comm_card = self.deck.draw(n)
    self.p0.hand.add_community(new_comm_card)
    self.p1.hand.add_community(new_comm_card)
    self.community += new_comm_card
    return new_comm_card

  def player_action_prompt(self,pl):
    '''Makes a prompt on what the player does'''
    player = self.players[pl]
    opp = self.players[(pl + 1) % 2]
    if player.stack <= 0.:
      print 'Player',pl,'is all in.'
    if player.stack <= 0. or opp.stack <= 0.:
      return self.xc(pl)
    pltype = player.player_type
    if pltype == 0:
      # Human player
      print '\nPlayer',pl,'your turn to act'
      action_str = raw_input('')
      split_str = re.split(' ',action_str)
      if split_str[0] == 'x' or split_str[0] == 'c':
        return self.xc(pl)
      if split_str[0] == 'f':
        return self.f(pl)
      if split_str[0] == 'b' or split_str[0] == 'r':
        try:
          amt = int(split_str[1])
        except:
          return self.player_action_prompt(pl)
        return self.br(pl,amt)
      else:
        return self.player_action_prompt(pl)
    else:
      # AI player 
      print '\nAI Player',pl,'is acting...'
      try:
        ai_action = player.ai.play(self)(pl)
        return ai_action
      except:
        pass
    return self.f(pl)

  def betting_round(self,pf=False):
    print 'button:',self.btn
    if pf:
      self.action = self.btn
    else:
      self.action = (self.btn + 1) % 2
    self.last_action = (self.action + 1) % 2

    while True:
      # It is self.action player's turn to act
      act = self.player_action_prompt(self.action)
      print 'Player',self.action,'did',act,'\n'
      if act == 'f':
        # Folded
        return True
      if act == 'br':
        self.last_action = (self.action + 1) % 2
      if self.action == self.last_action:
        break
      self.action = (self.action + 1) % 2

    self.pot += self.p0.bet 
    self.pot += self.p1.bet 
    self.p0.bet = 0
    self.p1.bet = 0
    return False

  def find_winner(self):
    if self.p0.hand > self.p1.hand:
      return 0
    elif self.p0.hand < self.p1.hand:
      return 1
    return 2 # chop the pot

  def show_hands(self):
    print 'Player 1\'s Hand:'
    print self.p0.hand
    print 'Player 2\'s Hand:'
    print self.p1.hand
    print 'Player 1: ',self.p0.stack
    print 'Player 2: ',self.p1.stack
    print '=====================\n\n'

  def start(self):
    self.pot = 0.
    self.last_action = None
    self.deck.shuffle()

    self.blinds()

    self.deal_hole()
    print '***PREFLOP***'
    print 'Pot: ',self.pot + self.p0.bet + self.p1.bet
    print self.p0.hand,'\n'
    if self.betting_round(pf=True):
      self.show_hands()
      return

    self.deal_community(3)
    print '***FLOP***'
    print 'Pot: ',self.pot + self.p0.bet + self.p1.bet
    print self.p0.hand,'\n'
    if self.betting_round():
      self.show_hands()
      return

    self.deal_community(1)
    print '***TURN***'
    print 'Pot: ',self.pot + self.p0.bet + self.p1.bet
    print self.p0.hand,'\n'
    if self.betting_round():
      self.show_hands()
      return

    self.deal_community(1)
    print '***RIVER***'
    print 'Pot: ',self.pot + self.p0.bet + self.p1.bet
    print self.p0.hand,'\n'
    if self.betting_round():
      self.show_hands()
      return

    raked_pot = max(self.pot * (1. - self.rake), self.pot - self.max_rake)

    winner = self.find_winner()
    print 'winner',winner
    print 'pot with rake:',raked_pot
    if winner == 0:
      print 'winner is 0', self.p0.stack
      self.p0.stack += raked_pot
      print 'winner is 0', self.p0.stack
    if winner == 1:
      print 'winner is 1', self.p1.stack
      self.p1.stack += raked_pot
      print 'winner is 1', self.p1.stack
    if winner == 2:
      self.p0.stack += raked_pot/2.
      self.p1.stack += raked_pot/2.
      print 'winner is 0', self.p0.stack
      print 'winner is 1', self.p1.stack
    self.show_hands()

    return

  def play(self):
    while self.p0.stack > 0. and self.p1.stack > 0.:
      self.start()
      self.btn = (self.btn + 1) % 2
    
  def __str__(self):
    return ''


g = Game()
g.play()

'''
d = Deck()
h = Hand(d.draw(4))

h.add_community(d.draw(3))
print h.rank_holding()
print h
h.add_community(d.draw(1))
print h.rank_holding()
print h
h.add_community(d.draw(1))
print h.rank_holding()
print h

d = Deck()
h = Hand(d.draw(4))

h.add_community(d.draw(3))
print h.rank_holding()
print h
h.add_community(d.draw(1))
print h.rank_holding()
print h
h.add_community(d.draw(1))
print h.rank_holding()
print h

d = Deck()
h = Hand(d.draw(4))

h.add_community(d.draw(3))
print h.rank_holding()
print h
h.add_community(d.draw(1))
print h.rank_holding()
print h
h.add_community(d.draw(1))
print h.rank_holding()
print h

d = Deck()
h = Hand(d.draw(4))

h.add_community(d.draw(3))
print h.rank_holding()
print h
h.add_community(d.draw(1))
print h.rank_holding()
print h
h.add_community(d.draw(1))
print h.rank_holding()
print h




print h._is_straight([0,4,8,12,16])
print h._is_flush([0,4,8,12,16])
print h._is_straight_flush([0,4,8,12,16])

print h._is_quad([0,1,2,3,10])

print h._is_trip([0,20,12,13,14])
print h._is_trip([0,51,12,13,14])
print h._is_trip([1,10,12,13,14])
print h._is_trip([27,8,12,13,14])



print h._is_pair([0,20,12,13,14])
print h._is_pair([0,51,12,13,14])
print h._is_pair([1,10,12,13,14])
print h._is_pair([27,8,12,13,14])

print h._is_two_pair([0,1,12,13,41])
print h._is_two_pair([4,5,0,13,14])
print h._is_two_pair([4,8,9,51,50])
print h._is_two_pair([27,8,12,13,14])


print h._is_full_house([0,1,2,13,14])
print h._is_full_house([0,51,12,13,14])
print h._is_full_house([11,10,12,13,14])
print h._is_full_house([27,26,12,13,14])
'''
