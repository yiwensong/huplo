import random
import math

class MCT():
  def __init__(self, parent, game,active_player=0):
    self.parent = parent
    if parent is None:
      self.player = active_player
    else:
      self.player = (self.parent.player + 1) % 2
    self.game = game
    self.total_value = [0.,0.]
    self.trials = 1
    self.children = []

  def add_child(self, child):
    self.children.append(child)

  def expand(self):
    val = self.game.payoff()
    if val[0] != 0 or val[1] != 0:
      return
    moves = self.game.moves()
    for m in moves:
      g = self.game.copy()
      g.move(m)
      child = MCT(self,g)
      self.children.append(child)

  def get_score(self, t, c):
    val = self.game.payoff()
    win_rate = self.total_value[self.player] / self.trials
    exploration = math.sqrt(math.log(t) / self.trials)
    score = win_rate + c * exploration
    if val[0] != 0 or val[1] != 0:
      return val[self.player] * 100 + c * exploration
    return score

  def random_traverse(self,t,c=None):
    if len(self.children) == 0:
      return self
    
    if c is None:
      c = math.sqrt(2)

    scores = map(lambda child: child.get_score(t,c), self.children)
    
    # total_score = sum(scores)
    # r = random.random() * total_score

    # for i in xrange(len(self.children)):
    #   r -= scores[i]
    #   if r <= 0:
    #     break

    # return self.children[i].random_traverse(t,c)

    m = scores.index(max(scores))
    # if self.parent is None:
    #   print m
    #   print scores
    
    # if self.parent is None:
    #   print ''
    # print self.player,':',self.game.moves()[m],'(',max(scores),')'
    return self.children[m].random_traverse(t,c)

  def simulate(self):
    '''Plays the game until the end. Returns a tuple of results (p0 net, p1 net).'''
    g = self.game.copy()
    moves = g.moves()
    val = g.payoff()
    while len(moves) > 0 and val[0] == 0 and val[1] == 0:
      g.move(moves[random.randint(0,len(moves)-1)])
      moves = g.moves()
      val = g.payoff()
    return g.payoff()
  
  def prop_up(self,sim_value):
    '''Propagates a simulation all the way to the root of the search tree'''
    self.total_value = map(lambda a,b: a + b, self.total_value, sim_value)
    self.trials += 1
    if self.parent is not None:
      self.parent.prop_up(sim_value)

    # if self.parent is None:
    #   pass
    # elif self.parent.parent is None:
    #   print 'sim_value:',sim_value
    #   print 'self.total_value:',self.total_value

def mcts(game,max_sim=1000,c=None):
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
  ap = g.active()
  mct_root = MCT(None,g,(ap + 1) % 2)
  
  for t in xrange(1,max_sim):
    curr = mct_root
    curr = mct_root.random_traverse(t,c)
    outcomes = curr.simulate()
    curr.prop_up(outcomes)
    curr.expand()

  if len(mct_root.children) == 0:
    return 0

  # points = map(lambda arr: arr.total_value[ap]/arr.trials, mct_root.children)
  # max_points = max(points)
  # best = points.index(max_points)
  points = map(lambda arr: arr.trials, mct_root.children)
  players = map(lambda arr: arr.player, mct_root.children)
  scores = map(lambda arr: arr.total_value[ap]/arr.trials, mct_root.children)
  max_points = max(points)
  best = points.index(max_points)

  # print points, max_points, best
  # print players
  # print scores
  # print game.moves()

  return game.moves()[best]



