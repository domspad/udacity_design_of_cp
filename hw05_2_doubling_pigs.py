# -----------------
# User Instructions
# 
# In this problem, we introduce doubling to the game of pig. 
# At any point in the game, a player (let's say player A) can
# offer to 'double' the game. Player B then has to decide to 
# 'accept', in which case the game is played through as normal,
# but it is now worth two points, or 'decline,' in which case
# player B immediately loses and player A wins one point. 
#
# Your job is to write two functions. The first, pig_actions_d,
# takes a state (p, me, you, pending, double), as input and 
# returns all of the legal actions.
# 
# The second, strategy_d, is a strategy function which takes a
# state as input and returns one of the possible actions. This
# strategy needs to beat hold_20_d in order for you to be
# marked correct. Happy pigging!

import random
from functools import update_wrapper


def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(*args)
    _f.cache = cache
    return _f

@decorator
def trace(f):
    indent = '   '
    def _f(*args):
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        print '%s--> %s' % (trace.level*indent, signature)
        trace.level += 1
        try:
            # your code here
            result = f(*args)
            print '%s<-- %s == %s' % ((trace.level-1)*indent, 
                                      signature, result)
        finally:
            # your code here
            trace.level-=1
        return result
    trace.level = 0
    return _f


def pig_actions_d(state):
    """The legal actions from a state. Usually, ["roll", "hold"].
    Exceptions: If double is "double", can only "accept" or "decline".
    Can't "hold" if pending is 0.
    If double is 1, can "double" (in addition to other moves).
    (If double > 1, cannot "double").
    """
    # state is like before, but with one more component, double,
    # which is 1 or 2 to denote the value of the game, or 'double'
    # for the moment at which one player has doubled and is waiting
    # for the other to accept or decline
    (p, me, you, pending, double) = state 
    if double == 'double' :
        return ['accept', 'decline']
    acts = ['roll']
    if pending != 0 :
        acts.append('hold')
    if double == 1 :
        acts.append('double')
    return acts

def strategy_d(state):
    """Doubles if looks like is going to win, else plays hold_20_d
        Wins > 60%  of points roughly 60%  of time agains hold_20_d
    """
    _, me, you, pending, double = state
    if me + pending > you + 15 and double == 1 :
        return 'double'
    return hold_20_d(state)

def Q_pig(state, action, Epoint) :
    "The expected value of choosing action in state."
    if action in ['hold','double', 'accept','decline'] :
        return -Epoint(do(action, state, dierolls))
    # elif action == 'accept' :
    #     return 2 * -Epoint(do(action, state, dierolls))
    # elif action == 'decline' :
    #     return -1
    elif action == 'roll' :
        return (-Epoint(do(action, state, one()))
                    + sum(Epoint(do(action, state,d())) for d in (two, three, four, five, six))) / 6

def one() : yield 1
def two() : yield 2
def three() : yield 3
def four() : yield 4
def five() : yield 5
def six() : yield 6

@memo
def Epoint(state) :
    """The utility of a state; here it is the expected point outcome of a game,
    given that the players are optimal"""
    (p, me, you, pending, double) = state
    if me + pending >= goal :
        if double == 1 :
            return 1
        elif double == 'double' :
            return 1
        else :
            return 2
    elif you >= goal :
        if double == 1 :
            return -1
        elif double == 'double' :
            return -1
        else :
            return -2
    else :
        return max(Q_pig(state, action, Epoint)
                        for action in pig_actions_d(state))
def best_action(state, actions, Q, U) :
    """Returns optimal action for a state, given U."""
    def EU(action) : return Q(state, action, U)
    return max(actions(state), key=EU)

@memo
def max_expected_point(state) :
    """An optimal strategy for maximizing the expected point differential for given game.
        Given that outcomes of game are I win 2, I win 1, you win 1, you win 2,
        the differentials possible in one game are respectively 2, 1, -1, -2
    """
    return best_action(state, pig_actions_d, Q_pig, Epoint)


def hold_20_d(state):
    "Hold at 20 pending.  Always accept; never double."
    (p, me, you, pending, double) = state
    return ('accept' if double == 'double' else
            'hold' if (pending >= 20 or me + pending >= goal) else
            'roll')
    
def clueless_d(state):
    return random.choice(pig_actions_d(state))
 
def dierolls():
    "Generate die rolls."
    while True:
        yield random.randint(1, 6)

def play_pig_d(A, B, dierolls=dierolls()):
    """Play a game of pig between two players, represented by their strategies.
    Each time through the main loop we ask the current player for one decision,
    which must be 'hold' or 'roll', and we update the state accordingly.
    When one player's score exceeds the goal, return that player."""
    strategies = [A, B]
    state = (0, 0, 0, 0, 1)
    while True:
        (p, me, you, pending, double) = state
        if me >= goal:
            return strategies[p], double
        elif you >= goal:
            return strategies[other[p]], double
        else:
            action = strategies[p](state)
            state = do(action, state, dierolls)

## No more roll() and hold(); instead, do:

def do(action, state, dierolls):
    """Return the state that results from doing action in state.
     If action is not legal, return a state where the opponent wins.
    Can use dierolls if needed."""
    (p, me, you, pending, double) = state
    if action not in pig_actions_d(state):
        return (other[p], goal, 0, 0, double)
    elif action == 'roll':
        d = next(dierolls)
        if d == 1:
            return (other[p], you, me+1, 0, double) # pig out; other player's turn
        else:
            return (p, me, you, pending+d, double)  # accumulate die in pending
    elif action == 'hold':
        return (other[p], you, me+pending, 0, double)
    elif action == 'double':
        return (other[p], you, me, pending, 'double')
    elif action == 'decline':
        return (other[p], goal, 0, 0, 1)
    elif action == 'accept':
        return (other[p], you, me, pending, 2)

goal = 40
other = {1:0, 0:1}

def strategy_compare(A, B, N=1000):
    """Takes two strategies, A and B, as input and returns the percentage
    of points won by strategy A."""
    A_points, B_points = 0, 0
    for i in range(N):
        if i % 2 == 0:  # take turns with who goes first
            winner, points = play_pig_d(A, B)
        else: 
            winner, points = play_pig_d(B, A)
        if winner.__name__ == A.__name__:
            A_points += points
        else: B_points += points
    A_percent = 100*A_points / float(A_points + B_points)
    print 'In %s games of pig, strategy %s took %s percent of the points against %s.' % (N, A.__name__, A_percent, B.__name__)
    return A_percent
    
def test():
    assert set(pig_actions_d((0, 2, 3, 0, 1)))          == set(['roll', 'double'])
    assert set(pig_actions_d((1, 20, 30, 5, 2)))        == set(['hold', 'roll']) 
    assert set(pig_actions_d((0, 5, 5, 5, 1)))          == set(['roll', 'hold', 'double'])
    assert set(pig_actions_d((1, 10, 15, 6, 'double'))) == set(['accept', 'decline']) 

    assert(Epoint((0,40,39,0,2))) == 2
    assert(Epoint((0,39,39,0,2))) == 2
    assert(Epoint((0,39,40,0,2))) == -2
    assert(Epoint((0,39,40,0,1))) == -1
    assert(max_expected_point((0,39,39,0,2)) == 'roll')
    assert(max_expected_point((0,38,38,0,1)) == 'double')

    assert strategy_compare(strategy_d, hold_20_d) > 60 # must win 60% of the points      
    return 'test passes'

print test()

def test_pig_actions_d() :
    cases = { (0,0,0,0,1) : ['roll', 'double'],
                (0,0,0,2,1) : ['roll', 'hold', 'double'], 
                (1,1,1,2,2) : ['roll','hold'],
                (0,0,0,0,'double') : ['accept','decline'],
                (0,0,0,2,'double') : ['accept','decline'], 
                (0,2,2,0,1) : ['roll','double']}
    assert all(pig_actions_d(state) == acts for state, acts in cases.items())
    return "passes all tests"

# print test_pig_actions_d()


