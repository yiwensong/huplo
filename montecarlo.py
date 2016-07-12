import random

class MCT():
  def __init__(self, parent, game):
    self.parent = parent
    self.game = game
    self.total_value = [0.,0.]
    self.trials = 0
    self.children = []

  def add_child(self, child):
    self.children.append(child)

  def expand(self):
    moves = self.game.moves()
    for m in moves:
      g = self.game.copy()
      g.move(m)
      child = MCT(self,g)
      self.children.append(child)

  def random_traverse(self):
    if len(self.children) == 0:
      return self

    r = random.randint(0,len(self.children)-1)
    return random_traverse(self.children(r))

  def simulate(self):
    '''Plays the game until the end. Returns a tuple of results (p0 net, p1 net).'''
    g = self.game.copy()
    moves = g.moves()
    while len(moves) > 0:
      g.move(moves[random.randint(0,len(moves)-1)])
      moves = g.moves()
    return g.payoff()
  
  def prop_up(self,sim_value):
    '''Propagates a simulation all the way to the root of the search tree'''
    self.total_value = map(lambda a,b: a + b, self.total_value, sim_value)
    self.trials += 1
    if self.parent is not None:
      self.parent.prop_up(sim_value)

def mcts(game,max_sim=1000):
  '''Assume game has the following:
  * game.active() returns which player is active.
  * game.moves() which returns a list of valid moves
  * game.copy() which lets you copy the game
  * game.move() which takes an element from the list returned by game.moves()
    and makes that move in the game.
  * game.payoff() returns a tuple that is the gain and loss of each player.
    When the game is not finished, this tuple will be all zeros.
  '''
  g = game.copy()
  mct_root = MCT(None,g)
  
  for _ in xrange(max_sim):
    curr = mct_root
    curr = mct_root.random_traverse()
    outcomes = curr.simulate()
    curr.prop_up(outcomes)
    curr.expand()

  ap = game.active()
  points = map(lambda arr: arr[ap], mct_root.children.total_value)
  max_points = max(points)
  best = points.index(max_points)

  return best
