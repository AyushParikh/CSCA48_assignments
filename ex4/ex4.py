# CSCA48 Excercise 4
# Written by Xiuqi (Rex) Xia


def gcd(a, b):
    """(int, int) -> int
    Return the greatest common denominator of a and b,
    using a recursive algorithm
    
    REQ: Both a and b must be non-negative
    
    >>> gcd(345, 0)
    345
    >>> gcd(0, 345)
    345
    >>> gcd(230, 230)
    230
    >>> gcd(7, 17)
    1
    >>> gcd(10, 9)
    1
    >>> gcd(12, 20)
    4
    >>> gcd(20, 10)
    10
    >>> gcd(61548, 58911)
    3
    """
    
    # Convert a and b to positive values if they are negative
    (a, b) = (abs(a), abs(b))
    
    # Base case: if one of the numbers is zero, gcd equals the other number
    if 0 in (a, b):
        return (b if (a == 0) else a)
    
    # Recursive decomposition: n-1 approach
    # if a <= b: gcd(a,b) = gcd(a, b-a)
    else:
        return (gcd(a, b-a) if (a <= b) else gcd(b, a-b))


def search(L, target):
    """(list of int, int) -> bool
    Return True iff target is in L, or any of its sublists,
    using a recursive algorithm
    
    >>> search([0,1,2,3,4], 2)
    True
    >>> search([0,1,2,3,4], 5)
    False
    >>> search([1, [2, 3], 4, [5, [6 , [], [8, 9]], 10]], 8)
    True
    >>> search([1, [2, 3], 4, [5, [6 , [], [8, 9]], 10]], 11)
    False
    """
    
    # Base case: if there are no elements left in L,
    # then target is not in L at all
    if (len(L) == 0):
        return False
    
    # Base case: if the zeroth element of L is the target,
    # then target has been found
    elif (L[0] == target):
        return True
    
    # Recursive decomposition: n-1 approach
    # If the zeroth element is a sublist, search within the sublist
    # Return True if the target is found in the sublist,
    # if not, search the rest of the list.
    elif (isinstance(L[0], list)):
        return (True if search(L[0], target) else search(L[1:], target))
    
    # Recursive decomposition: n-1 approach
    # If the zeroth element is not a sublist (it's a non-target int),
    # return True if the target is found in the rest of the list
    else:
        return search(L[1:], target)


def binarify(n):
    """(int) -> str
    Return a string of 1s and 0s, representing n as a binary number,
    using a recursive algorithm
    
    >>> binarify(0)
    '0'
    >>> binarify(1)
    '1'
    >>> binarify(2)
    '10'
    >>> binarify(255)
    '11111111'
    >>> binarify(256)
    '100000000'
    >>> binarify(1163223)
    '100011011111111010111'
    """
    # Change this constant to adapt this code for diferent numeral systems
    BASE = 2
    
    # Base case: if n is less than 2, it is the same in binary
    if (n < BASE):
        return str(n)
    
    # Recursive decomposition: n-1 approach
    else:
        # Get the quotient and remainder of n divided by 2
        (quotient, remainder) = divmod(n, BASE)
        # The binary representation has remainder as the right-most digit,
        # and the binarified quotient as the rest of the digits
        return binarify(quotient) + str(remainder)
    

if (__name__ == '__main__'):
    import doctest
    doctest.testmod(verbose=True)
