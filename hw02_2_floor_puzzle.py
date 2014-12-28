import itertools 

def floor_puzzle() :
    """ Solves floor puzzle as stated in hw 2"""
    floors = range(1,6)
    orderings = itertools.permutations(floors)
    return next( (Hopper, Kay, Liskov, Perlis, Ritchie) for (Hopper, Kay, Liskov, Perlis, Ritchie) in orderings
                                                        if Hopper != 5
                                                        if Kay != 1
                                                        if Liskov not in [1,5]
                                                        if Perlis > Kay
                                                        if abs(Ritchie - Liskov) != 1
                                                        if abs(Liskov - Kay) != 1)

if __name__ == '__main__' :
	print(floor_puzzle())