from regex_functions import remove_occurences

def split_combinations(s):
    R"""(str) -> set of {tuple of (str, str)}
    Return the set of all possible ways (combinations of characters) to
    split s into two non-empty strings.

    >>> split_combinations('01*') ==\
    ... {('*', '01'), ('1', '0*'), ('0', '1*')}
    True
    """
    # Set to be returned
    split_combs = set()

    # For each way to split len(s) characters into two parts
    # n is the number of characters in the smaller of the two parts
    for n in range(1, ((len(s) // 2) + 1)):
        # Find all the combinations of n characters in s
        combs = n_combinations(s, n)

        # For each combinations, get a string composed of the characters in
        # s that are not in the combination
        # Add the tuple of (comb, left_over_chars) to split_combs
        for comb in combs:
            left_over_chars = remove_occurences(s, comb)
            split_combs.add((comb, left_over_chars))

    return split_combs


def n_combinations(s, n):
    R"""(str, int) -> set of str
    Return the set of all combinations of n characters in s.

    >>> n_combinations('1234', 1) == {'1', '2', '3', '4'}
    True
    >>> n_combinations('1234', 2) == \
    ... {'12', '13', '14', '23', '24', '34'}
    True
    >>> len(n_combinations('1234567890', 5)) == 252
    True
    """
    # Base case: if n is zero, no combinations are possible
    if(n == 0):
        return set()

    # Base case: if n is one, return the set of characters in s
    if(n == 1):
        return set(s)

    # Recursive decomposition:
    else:
        # Set to return
        combs = set()

        # For each char,
        for i in range(len(s)):
            char = s[i]

            # Find the combinations of all characters of s to the right
            # of the current char, with smaller n
            smaller_combs = n_combinations(s[(i + 1):], (n - 1))

            # Concatenate char with each combination in smaller_combs
            # and add to combs
            combs.update({(char + comb) for comb in smaller_combs})

        return combs

if(__name__ == '__main__'):
    import doctest
    print(doctest.testmod())

    for i in n_combinations('1234', 2):
        print(i, remove_occurences('1234', i))