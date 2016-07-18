import montecarlo
import huplo_game

class HUPLO_game():
  '''This is the class that will hook up the MCTS code with the game code'''

  def __init__(self,arg=None):
    pass
  
  def __str__(self):
    s = ''
    return s 

  def active(self):
    return 0

  def copy(self):
    return HUPLO(self)

  def moves(self):
    return []

  def move(self,mv):
    pass

  def payoff(self):
    return [0,0]
