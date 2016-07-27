import montecarlo
import huplo_game as game

class HUPLO_game():
  '''This is the class that will hook up the MCTS code with the game code'''

  def __init__(self,g,arg=None):
    self.g = game.Game(p0type=0,p1type=0,copy=g)
    self.pays = [0,0]
  
  def __str__(self):
    s = ''
    s += 'hand 0:\n'
    s += str(self.g.p0.hand)
    s += '\n'
    s += 'hand 1:\n'
    s += str(self.g.p1.hand)
    s += '\n'
    s += 'bet 0: '
    s += str(self.g.p0.bet)
    s += '\n'
    s += 'bet 1: '
    s += str(self.g.p1.bet)
    s += '\n'
    s += 'pot: '
    s += str(self.g.pot)
    s += '\n\n\n'
    return s 

  def active(self):
    return self.g.action

  def copy(self):
    return HUPLO(self.g)

  def moves(self):
    if self.pays[0] != 0 or self.pays[1] != 0:
      return []
    return ['f','xc','br0','br1','br2','br3']

  def preaction(self):
    '''Deals the hand and makes players pay blinds if not already done'''
    if self.g.p0.hand is None:
      self.g.blinds()
      self.g.deal_hole()
      self.g.action = self.g.btn
      self.g.last_action = (self.g.action + 1) % 2
      return

  def pg_cleanup(self):
    self.g.pot = 0.
    self.g.p0.bet = 0.
    self.g.p1.bet = 0.
    return

  def betting_cleanup(self):
    self.g.pot += self.g.p0.bet 
    self.g.pot += self.g.p1.bet 
    self.g.p0.bet = 0.
    self.g.p1.bet = 0.
    return

  def postaction(self,last_act):
    '''Deals the next cards and determines winners (if necessary)'''
    print self.g.action, self.g.last_action
    if self.g.action == self.g.last_action and last_act == 'xc':
      self.g.last_action = self.g.btn
      self.g.action = (self.g.btn + 1) % 2
      if len(self.g.community) == 0:
        self.g.deal_community(3)
      elif len(self.g.community) == 3 or len(self.g.community) == 4:
        self.g.deal_community(1)
      else:
        raked_pot = max(self.g.pot * (1. - self.g.rake), self.g.pot - self.g.max_rake)
        pot = self.g.pot
        winner = self.g.find_winner()
        if winner == 0:
          self.g.p0.stack += raked_pot
          self.pays[0] = raked_pot - pot/2.
          self.pays[1] = -pot/2.
        if winner == 1:
          self.g.p1.stack += raked_pot
          self.pays[1] = raked_pot - pot/2.
          self.pays[0] = -pot/2.
        if winner == 2:
          self.g.p0.stack += raked_pot/2.
          self.g.p1.stack += raked_pot/2.
          self.pays[0] = raked_pot/2. - pot/2.
          self.pays[1] = raked_pot/2. - pot/2.
        self.pg_cleanup()
      self.betting_cleanup()
    else:
      self.g.action = (self.g.action + 1) % 2
    if last_act == 'f':
      # Player who didn't fold wins
      winner = self.g.action
      if len(self.g.community) > 0:
        raked_pot = max(self.g.pot * (1. - self.g.rake), self.g.pot - self.g.max_rake)
      else:
        raked_pot = self.g.pot
      self.g.players[winner].stack += raked_pot
      self.pays[winner] = raked_pot - self.g.pot/2.
      self.pays[(winner + 1) % 2] = -self.g.pot/2.
      self.pg_cleanup()

  def move(self,mv):
    print self.g.action,'plays',mv,'(btn is',self.g.btn,')'
    self.preaction()
    act = self.g.action
    pot = self.g.maxbet(act)
    bet = self.g.players[act].bet
    max_amt = pot - bet
    if mv == 'f':
      last_act = self.g.f(act,fold_cleanup=False)
    elif mv == 'xc':
      last_act = self.g.xc(act)
    elif mv == 'br0':
      last_act = self.g.br(act,bet + .350 * max_amt )
    elif mv == 'br1':
      last_act = self.g.br(act,bet + .500 * max_amt )
    elif mv == 'br2':
      last_act = self.g.br(act,bet + .650 * max_amt )
    elif mv == 'br3':
      last_act = self.g.br(act,pot)
    else:
      # Don't let it get here pls
      return
    if last_act == 'br':
      self.g.last_action = (act + 1) % 2
    self.postaction(last_act)


  def payoff(self):
    return self.pays


def main():
  global g,h
  h = game.Game()
  g = HUPLO_game(h)
  print g.moves()
  g.move('br0')
  print g
  g.move('br0')
  print g
  g.move('br0')
  print g
  g.move('xc')
  print g
  g.move('xc')
  print g

if __name__=='__main__':
  main()


