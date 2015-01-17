# -----------------
# User Instructions
# 
# Write a function, subway, that takes lines as input (read more about
# the **lines notation in the instructor comments box below) and returns
# a dictionary of the form {station:{neighbor:line, ...}, ... } 
#
# For example, when calling subway(boston), one of the entries in the 
# resulting dictionary should be 'foresthills': {'backbay': 'orange'}. 
# This means that foresthills only has one neighbor ('backbay') and 
# that neighbor is on the orange line. Other stations have more neighbors:
# 'state', for example, has 4 neighbors.
#
# Once you've defined your subway function, you can define a ride and 
# longest_ride function. ride(here, there, system) takes as input 
# a starting station (here), a destination station (there), and a subway
# system and returns the shortest path.
#
# longest_ride(system) returns the longest possible ride in a given 
# subway system. 

# -------------
# Grading Notes
#
# The subway() function will not be tested directly, only ride() and 
# longest_ride() will be explicitly tested. If your code passes the 
# assert statements in test_ride(), it should be marked correct.

# -------------
# COMPARISON WITH NORVIGS -- GOOD!
#
# subway - same method and design (his is a little more readable because
        # he has helper function for getting adjacent stops)
# ride - same 
# longest_ride - I did a little more efficient search by only choosing end stops to look
    #   but we basically have the same design apart from that

from collections import defaultdict
from itertools import combinations

def subway(**lines):
    """Define a subway map. Input is subway(linename='station1 station2...'...).
    Convert that and return a dict of the form: {station:{neighbor:line,...},...}"""
    # Make {stop: [(adj_stop, line)]} dictionary, assumes each line as at least 2 stops
    network = defaultdict(dict)
    for line, stops in lines.items() :
        stops = stops.split()
        length = len(stops) 
        for i in range(1,length) :
            network[stops[i]][stops[i-1]] = line
            network[stops[i-1]][stops[i]] = line
    return network

boston = subway(
    blue='bowdoin government state aquarium maverick airport suffolk revere wonderland',
    orange='oakgrove sullivan haymarket state downtown chinatown tufts backbay foresthills',
    green='lechmere science north haymarket government park copley kenmore newton riverside',
    red='alewife davis porter harvard central mit charles park downtown south umass mattapan')

def ride(here, there, system=boston):
    "Return a path on the subway system from here to there."
    def neighbors(stop) :
        return system[stop]
    return shortest_path_search(here, neighbors, (lambda x : x == there))

def longest_ride(system):
    """"Return the longest possible 'shortest path' 
    ride between any two stops in the system."""
    end_stops = [stop for stop, adj in system.items() if len(adj) == 1]
    return max([ride(stops[0],stops[1],system) for stops in combinations(end_stops,2)], key=len)

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return []

def path_states(path):
    "Return a list of states in this path."
    return path[0::2]
    
def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

def tests() :
    # Tests the subway function
    #       4    6
    #       |    |
    #  1 -- 2 -- 3    Line a
    #       |    |
    #       5    7
    # 
    #       b    c

    network = defaultdict(dict)
    network['1'] = {'2':'a'}
    network['2'] = {'1':'a', '3':'a', '4':'b', '5':'b'}
    network['3'] = {'2':'a','6':'c','7':'c'}
    network['4'] = {'2':'b'}
    network['5'] = {'2':'b'}
    network['6'] = {'3':'c'}
    network['7'] = {'3':'c'}

    assert subway(a="1 2 3",b="4 2 5",c="6 3 7") == network
    print "Passes tests"

def test_ride():
    assert ride('mit', 'government') == [
        'mit', 'red', 'charles', 'red', 'park', 'green', 'government']
    assert ride('mattapan', 'foresthills') == [
        'mattapan', 'red', 'umass', 'red', 'south', 'red', 'downtown',
        'orange', 'chinatown', 'orange', 'tufts', 'orange', 'backbay', 'orange', 'foresthills']
    assert ride('newton', 'alewife') == [
        'newton', 'green', 'kenmore', 'green', 'copley', 'green', 'park', 'red', 'charles', 'red',
        'mit', 'red', 'central', 'red', 'harvard', 'red', 'porter', 'red', 'davis', 'red', 'alewife']
    assert (path_states(longest_ride(boston)) == [
        'wonderland', 'revere', 'suffolk', 'airport', 'maverick', 'aquarium', 'state', 'downtown', 'park',
        'charles', 'mit', 'central', 'harvard', 'porter', 'davis', 'alewife'] or 
        path_states(longest_ride(boston)) == [
                'alewife', 'davis', 'porter', 'harvard', 'central', 'mit', 'charles', 
                'park', 'downtown', 'state', 'aquarium', 'maverick', 'airport', 'suffolk', 'revere', 'wonderland'])
    assert len(path_states(longest_ride(boston))) == 16
    return 'test_ride passes'

tests()
print test_ride()