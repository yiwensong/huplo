import random
import math

from montecarlo import *

class TicTacToe():
  def __init__(self,arg=None):
    if arg is not None:
      self.board = map(lambda i:i, arg.board)
      self.turn = arg.turn
      return
    self.board = [0] * 9
    self.turn = 0

  def active(self):
    return self.turn

  def moves(self):
    mv = []
    for i in xrange(9):
      if self.board[i] == 0:
        mv.append(i)
    return mv

  def copy(self):
    return TicTacToe(arg=self)

  def move(self,move):
    if move not in self.moves():
      return -1
    self.board[move] = int((self.turn - .5) * 2)
    self.turn = (self.turn + 1) % 2

  def payoff(self):
    b = self.board
    winner = 0
    for i in xrange(3):
      if b[3*i] == b[3*i+1] == b[3*i+2] and b[3*i] != 0:
        winner = b[3*i]
        break
      if b[i] == b[i+3] == b[i+6] and b[i] != 0:
        winner = b[i]
        break
    if b[0] == b[4] == b[8] and winner == 0:
      winner = b[0]
    if b[2] == b[4] == b[6] and winner == 0:
      winner = b[2]

    if winner is 0:
      return (0,0)
    
    winner = (winner + 1) / 2
    outcomes = [0,0]
    outcomes[winner] = 1
    outcomes[(winner + 1) % 2] = -1
    return tuple(outcomes)

  def __str__(self):
    s = ''
    for i in xrange(9):
      if self.board[i] == -1:
        s += 'x '
      elif self.board[i] == 1:
        s += 'o '
      else:
        s += '- '
      if i % 3 == 2:
        s += '\n'
    return s


t = TicTacToe()
order = range(9)
random.shuffle(order)
for i in order:
  t.move(i)
  print t
  print t.payoff()

t = TicTacToe()
while t.payoff()[0] == 0 and len(t.moves()) > 0:
  if t.active() == 0:
    # Player turn
    valid = -1
    while valid == -1:
      player_mv = input('Which square?\n-> ')
      valid = t.move(player_mv)
  else:
    # AI turn
    ai_mv = mcts(t)
    t.move(ai_mv)
  print t
print t.payoff()



t = TicTacToe()
while t.payoff()[0] == 0 and len(t.moves()) > 0:
  if t.active() == 1:
    # Player turn
    valid = -1
    while valid == -1:
      player_mv = input('Which square?\n-> ')
      valid = t.move(player_mv)
  else:
    # AI turn
    ai_mv = mcts(t)
    t.move(ai_mv)
  print t
print t.payoff()
