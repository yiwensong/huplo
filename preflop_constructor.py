import re
import random

import numpy as np
from sklearn import svm

'''This file is to create a preflop range constructor for the HUPLO AI.
The goals of this are:
  * Using learning, predict which hands are playable and which are not.
  * Create an adjustable model for which we can add or cut hands depending on desired
    opening range or observed villain opening range.
  * Aid the MCTS AI by eliminating hands which villains are unlikely to play.
  * Serve as a UI for people to add data points to the data set.
'''

DATA = 'data/hands.txt'
SAVE = 'data/pfc'
