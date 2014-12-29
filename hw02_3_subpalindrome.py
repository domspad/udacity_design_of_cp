def longest_subpalindrome_slice(text) :
    " Return (i,j) such that text[i:j] is the longest (earliest) palindrom in text."
    #check 0,1 length
    if len(text) < 2 :
        return (0,len(text))
    #set text to lower
    text = text.lower()
    #set default longest
    longest = (0,1)
    #seed_gen
    #for each seed
    for seed in seed_gen(text) :
        #find longest growth
        stalk = grow(seed,text)
        if longest[1]-longest[0] < stalk[1]-stalk[0] :
            longest = stalk
    #return longest growth
    return longest

def seed_gen(text) :
    """
    A generator function for the 0 and 1 length substring indicies 
    that center all 2 and 3 length substrings
    Text is assumed to be at least 2 chars
    """
    for i in range(1,len(text)) :
        yield (i,i)
    if len(text) > 3 :
        for i in range(1,len(text)-1) :
            yield (i,i+1)

def grow(seed,text) :
    """
    Returns the longest palindrome with center ends
    """
    if not boundary(seed,text) and step(seed,text) :
        return grow((seed[0]-1,seed[1]+1),text)
    return seed

def boundary(seed,text) :
    return (seed[0] == 0) or (seed[1] == len(text))

def step(seed,text) :
    return text[seed[0]-1] == text[seed[1]]


def test() :
    L = longest_subpalindrome_slice
    assert L('racecar') == L('Racecar') == L('RacecarX') == (0,7)
    assert L('Race car') == (0,1)
    assert L('') == (0,0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0,5)
    assert L('Mad am I ma dam.') == (0,15)
    assert L('xxxxxxxxxxxxxxxxxxxx') == (0,20)
    return 'tests pass'

print test()