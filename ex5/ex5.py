# CSCA48 Excercise 5
# Written by Xiuqi (Rex) Xia


def edit_distance(s1, s2):
    """(str, str) -> int
    Return the minimum number of single-character changes required
    to turn s1 into s2
    REQ: s1 and s2 must have the same length
    Will raise ValueError if REQ not met
    
    >>> edit_distance('', '')
    0
    >>> edit_distance('a', 'a')
    0
    >>> edit_distance('a', 'b')
    1
    >>> edit_distance('aaa', 'aaa')
    0
    >>> edit_distance('aaa', 'bbb')
    3
    >>> edit_distance('aaa', 'aba')
    1
    >>> edit_distance('abcdefghijklmnopqrstuvwxyz',
    ...               'ab1de2ghij34mnop5rst6v7xyz')
    7
    """
    
    # if s1 and s2 have different lengths, raise ValueError
    if (len(s1) != len(s2)):
        raise ValueError("s1 and s2 cannot have different lengths")
    
    # Base case: if the strings are empty, no changes required
    if (not s1):
        return 0
    
    # Recursive decomposition: n-1 approach
    else:
        # Check if the zeroth char needs changing
        # Edit distance for this char is 1 if it needs changing        
        return ((1 if (s1[0] != s2[0]) else 0) +
                # Add the edit distance of the rest of the strings
                edit_distance(s1[1:], s2[1:]))


def subsequence(s1, s2):
    """(str, str) -> bool
    Return True iff s2 can be made equal to s1 by having 0 or more of its
    characters removed
    
    >>> subsequence('', '')
    True
    >>> subsequence('', 'abc')
    True
    >>> subsequence('abc', '')
    False
    >>> subsequence('abc', 'abc')
    True
    >>> subsequence('abc', 'aacba')
    False
    >>> subsequence('abc', '123abc123')
    True
    >>> subsequence('abc', '123a123b123c123')
    True
    >>> subsequence('abc', '123a123a123c12ba3')
    False
    >>> subsequence('dog', 'XYZdABCo123g!!!')
    True
    """
    
    # Base case: If s1 is empty, s1 is a subsequence of s2
    if (not s1):
        return True
    # Base case: If s2 is empty, s1 is not a subsequence of s2
    elif (not s2):
        return False
    
    # Recursive decomposition: n-1 approach on both s1 and s2
    else:
        # If s1[0] and s2[0] match, continue to recurse with shorter s1 and s2
        if (s1[0] == s2[0]):
            return subsequence(s1[1:], s2[1:])
        # If they don't match, continue to recurse with shorter s2 only
        else:
            return subsequence(s1, s2[1:])


def perms(s):
    """(str) -> set of str
    Return a set containing all permutations of the characters in s.
    
    >>> perms('') == {''}
    True
    >>> perms('a') == {'a'}
    True
    >>> perms('ab') == {'ab', 'ba'}
    True
    >>> perms('abc') == {'abc', 'acb', 'bac', 'bca', 'cab', 'cba'}
    True
    >>> perms('abb') == {'abb', 'bab', 'bba'}
    True
    >>> perms('abcd') == {'adbc', 'adcb', 'abdc', 'abcd', 'acdb', 'acbd',
    ...                   'badc', 'bacd', 'bdac', 'bdca', 'bcad', 'bcda',
    ...                   'cabd', 'cadb', 'cbad', 'cbda', 'cdab', 'cdba',
    ...                   'dabc', 'dacb', 'dbac', 'dbca', 'dcab', 'dcba'}
    True
    """
    
    # Base case: if s is 1 character or shorter,
    # it has only one permutation (itself)
    if (len(s) <= 1):
        return {s}
    
    # Recursive decomposition: n-1 approach
    # Permutations of s consist of each character in s plus each permutation
    # of s minus that character
    else:
        # New set for storing the permutations
        result = set()
        
        # For each character in s,
        # find the permutations of s minus that character.
        # Add s to the begining of each permutation, and add to result set
        for i in range(len(s)):
            char = s[i]
            
            # String of characters in s other than the current char
            s_minus = s[:i] + s[i+1:]
            
            # Set of permutations of s_minus
            perms_minus = perms(s_minus)
            
            # Add char to the begining of each permutation of s_minus,
            # and update result set to include these results.
            result.update({(char + p) for p in perms_minus})
    
        return result


if(__name__ == '__main__'):
    import doctest
    doctest.testmod(verbose=True)