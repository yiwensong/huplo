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
    return []

  def move(self,mv):
    pass

  def payoff(self):
    return [0,0]
