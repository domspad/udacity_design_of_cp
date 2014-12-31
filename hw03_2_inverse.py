# --------------
# User Instructions
#
# Write a function, inverse, which takes as input a monotonically
# increasing (always increasing) function that is defined on the 
# non-negative numbers. The runtime of your program should be 
# proportional to the LOGARITHM of the input. You may want to 
# do some research into binary search and Newton's method to 
# help you out.
#
# This function should return another function which computes the
# inverse of the input function. 
#
# Your inverse function should also take an optional parameter, 
# delta, as input so that the computed value of the inverse will
# be within delta of the true value.

# -------------
# Grading Notes
#
# Your function will be called with three test cases. The 
# input numbers will be large enough that your submission
# will only terminate in the allotted time if it is 
# efficient enough. 

import time

def slow_inverse(f, delta=1/128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def f_1(y):
        x = 0
        while f(x) < y:
            x += delta
        # Now x is too big, x-delta is too small; pick the closest to y
        return x if (f(x)-y < y-f(x-delta)) else x-delta
    return f_1 

def inverse(f, delta = 1/128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def f_1(y) :
        rhl = 1
        while f(rhl) < y :
            rhl *= 2
        x = adjust = rhl /2.0
        diff = f(x) - y
        while abs(diff) > delta :
            adjust /= 2.0
            x = x - adjust if (diff > 0) else x + adjust
            diff = f(x) - y
        return x
    return f_1    
    
def square(x): return x*x
sqrt = slow_inverse(square)

def timeit(code) :
    start = time.clock()
    result = eval(code)
    return time.clock() - start, result

fast_sqrt = inverse(square)
slow_sqrt = slow_inverse(square)

def test() :
    
    print 'function {:<20} time {:<40} result {}'.format('fast_sqrt',*timeit('fast_sqrt(1e8)'))
    print 'function {:<20} time {:<40} result {}'.format('slow_sqrt',*timeit('slow_sqrt(1e8)'))

test()