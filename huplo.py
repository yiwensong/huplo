import montecarlo
import huplo_game as game

class HUPLO_game():
  '''This is the class that will hook up the MCTS code with the game code'''

  def __init__(self,g,arg=None):
    self.g = game.Game(p0type=0,p1type=0,copy=g)
  
  def __str__(self):
    s = ''
    return s 

  def active(self):
    return self.g.action

  def copy(self):
    return HUPLO(self)

  def moves(self):
    return ['f','xc','br0','br1','br2','br3']

  def move(self,mv):
    act = self.g.action
    if mv == 'f':
      pass
    elif mv == 'xc':
      pass
    elif mv == 'br0':
      pass
    elif mv == 'br1':
      pass
    elif mv == 'br2':
      pass
    elif mv == 'br3':
      pass
    else:
      return

  def payoff(self):
    return [0,0]
