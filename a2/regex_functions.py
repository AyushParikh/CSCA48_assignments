"""
# Copyright 2013 Nick Cheng, Brian Harrington, Danny Heap, Xiuqi (Rex) Xia
# 2013, 2014
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2014
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

# Do not change anything above this comment

# Student code below this comment.
# -------------------------------------------------
# CSCA48 Assignment 2
# Written by Xiuqi (Rex) Xia

# Valid regex symbols/operators
NULLARY_SYMB = {'0', '1', '2', 'e'}  # These are the only one-char regexes
UNARY_OP = {'*': StarTree}                # Requires one operand
BINARY_OP = {'.': DotTree, '|': BarTree}  # Requires two operands


def is_regex(s):
    R"""(str) -> Bool
    Return True iff s is a valid regular expression.

    >>> is_regex('0')
    True
    >>> is_regex('1*')
    True
    >>> is_regex('2**')
    True
    >>> is_regex('*2')
    False
    >>> is_regex('(((0*.1)|2).(e|0*))')
    True
    >>> is_regex('(((0*.1)|2.(e|0*))')
    False
    """
    # Base case: s has only one character
    if(len(s) <= 1):
        # Only return True if s is a valid nullary regex symbol
        return (s in NULLARY_SYMB)

    # Recursive decomposition:

    # A regex with a unary regex operator as the last character is valid if
    # the string preceeding the unary operator is also a valid regex
    elif(s[-1] in UNARY_OP):
        return is_regex(s[:-1])

    # If a regex starts with '(' and ends with ')',
    # it must be a binary operation statement.
    elif(s[0] == '(') and (s[-1] == ')'):
        # Try to identify the left operand, operator, and right operand
        try:
            (left, op, right) = parse_binary_operation(s)
        except ValueError:
            # if parse_binary_operation fails, s was not formatted correctly
            # so it can't be valid regex
            return False

        # This binary operation statement is a regex if its left and right
        # operands are both valid regexes, and the operator is a valid
        # regex binary operator
        return ((op in BINARY_OP) and
                (is_regex(left)) and
                (is_regex(right)))

    # Anything else is not a regex
    else:
        return False


def parse_binary_operation(s):
    R"""(str) -> tuple of (str, str, str)
    Parse s and return a tuple of (left_operand, operator, right_operand).

    s must start with '(' and end with ')'. These outer parentheses are
    removed before the left_operand, operator, and right_operand are identified
    according to the following rules:

    - left_operand (see help(find_l_operand_end) for left operand rules)
    - operator is the next character after left_operand in s
    - right_operand consists of the rest of s after operator

    REQ: s must contain enough characters for the outer parentheses,
    a left_operand, operator, and right_operand to be present.
    (Min length is: len(left_operand) + 4)
    REQ: s must start with '(' and end with ')'
    REQ: The parentheses in s must match
    (there must be equal numbers of '( and ')')

    If REQs not met raise ValueError

    >>> parse_binary_operation('(0|1)')
    ('0', '|', '1')
    >>> parse_binary_operation('(((0*.1)|2).(e|0*))')
    ('((0*.1)|2)', '.', '(e|0*)')
    >>> parse_binary_operation('(((0*.1)|2.(e|0*)')
    Traceback (most recent call last):
    builtins.ValueError: <error message here>
    """
    # Deal with some REQs
    if(len(s) < 5):
        raise ValueError('Parameter s is too short')
    if((s[0] != '(') or (s[-1] != ')')):
        raise ValueError("Parameter s must start with '(' and end with ')'")

    try:
        # Remove the start and end parentheses from s
        s = s[1:-1]

        # Figure out where left_operand ends
        l_operand_end = find_l_operand_end(s)
        left_operand = s[:l_operand_end]

        # Operator is the next character after left_operand
        # (0th character after the end of left_operand)
        operator = s[l_operand_end]

        # right_operand is the rest of s after operator
        # (1th character after the end of left_operand)
        right_operand = s[(l_operand_end + 1):]

        return (left_operand, operator, right_operand)

    except IndexError:
        # If at any point an index cannot be found in s, it must have
        # violated the REQs
        raise ValueError('Parameter s is formatted incorrectly '
                         '(eg: operands missing, ummatched parentheses, etc)')


def find_l_operand_end(s):
    R"""(str) -> int

    Given s, a regex binary operation statement with the outer parentheses
    removed:

    Identify the part of s that forms a left operand, and return the index
    corresponding to the end of left operand

    left_operand consists of all the characters of s up to a valid regex
    binary operator, ignoring any regex operators found inside
    parenthesis-enclosed substrings.

    If it is not possible to identify a left_operand according to the above
    criteria, return the length of the string as the end index.

    >>> find_l_operand_end('')
    0
    >>> find_l_operand_end('0|1')
    1
    >>> find_l_operand_end('0***.1')
    4
    >>> find_l_operand_end('0***1')
    5
    >>> find_l_operand_end('((0*.1)|2).(e|0*)')
    10
    >>> find_l_operand_end('(1')
    2
    >>> find_l_operand_end('((0*.1)|2.(e|0*')
    15
    """
    # if s is empty, return 0
    if(not s):
        return 0

    else:
        # Go through s and return the first occurence of a regex
        # binary operator (ignoring stuff in parentheses)
        i = 0
        bin_op_found = False
        while((i < len(s)) and (not bin_op_found)):
            char = s[i]

            # If char is a regex binary operator, exit loop and
            # return current index
            if(char in BINARY_OP):
                bin_op_found = True

            # If char is the start of a parenthesis-enclosed substring,
            # find its end and skip to that index
            elif(char == '('):
                i = find_paren_end(s, i)

            else:
                # advance index
                i += 1

        # i is either the index of the first (non-parenthesized) occurence
        # of a regex binary operator, or len(s) if no such binary operators
        # are found
        return i


def find_paren_end(s, start_index):
    """(str, int) -> int
    Find the index of the end of the parenthesis-enclosed substring in s
    starting at start_index.

    If the parenthesis-enclosed substring is not closed before the end of s,
    return len(s)

    REQ: start_index must be a valid index for s
    if REQ not met raise IndexError
    REQ: s[start_index] must be '('
    if REQ not met raise ValueError

    >>> find_paren_end('spam(h(())a()m)eggs', 4)
    15
    >>> find_paren_end('spam(h(())a()m(eggs', 4)
    19
    """
    # Deal with REQ violation
    if(s[start_index] != '('):
        raise ValueError("s[start_index] must be '('")

    # Set current parenthesization level to 1
    level = 1
    # Start at the 1th character after start_index
    # (since we know 0th character after start_index is '(')
    char_index = start_index + 1

    # Keep looping until the first parenthesis is closed,
    # (level becomes zero)
    # or until the end of s is reached
    while(level and (char_index < len(s))):
        char = s[char_index]
        # if char is '(', increase the parenthesization level
        if(char == '('):
            level += 1
        # if char is ')', decrease the parenthesization level
        elif(char == ')'):
            level -= 1

        # advance the index
        char_index += 1

    # The char_index is the end of the parenthesis-enclosed substring,
    # or the end of s (whichever was reached earlier)
    return char_index


def all_regex_permutations(s):
    R"""(str) -> set of str
    Return the set of all permutations of the characters in s that form valid
    regular expressions

    >>> all_regex_permutations('spam')
    set()
    >>> all_regex_permutations('**1*')
    {'1***'}
    >>> all_regex_permutations('**1*0')
    set()
    >>> all_regex_permutations('(0|1')
    set()
    >>> all_regex_permutations('(0|1)()()()()')
    set()
    >>> all_regex_permutations('01*|()') == \
    ... {'(0*|1)', '(0|1*)', '(1*|0)', '(1|0*)', '(1|0)*', '(0|1)*'}
    True
    """
    # Base case: if s is empty,
    # then obviously no permutations can be formed
    if(not s):
        return set()

    # Base case: if s has only one character
    if(len(s) == 1):
        # if s is a regex nullary symbol,
        # then it is the only permutation
        if(s in NULLARY_SYMB):
            return {s}
        # Otherwise, there are no valid regex permutations
        else:
            return set()

    # Base case: if s has parentheses, but they're not matched
    # (unequal numbers of '(' and ')'), then it's not possible to form
    # any valid regexes
    if((('(' in s) or (')' in s)) and
       (s.count('(') != s.count(')'))):
        return set()

    # Base case: if s has binary operators but the wrong number of parentheses
    # (there must be one '(' for each binary operator found),
    # then it's not possible to form any valid regexes

    # Count the number of occurences of binary operators in s
    binary_op_count = 0
    for op in BINARY_OP:
        binary_op_count += s.count(op)
    # Check to see if there is one '(' for each occurence of a binary operator
    if(s.count('(') != binary_op_count):
        return set()

    # Recursive decomposition
    else:
        # Set to store all the permutations
        perms = set()

        # For each type of unary operator found in s
        for op in UNARY_OP:
            if(op in s):
                # Make a slice of s with one less occurence of the operator
                lesser_s = remove_occurences(s, op)

                # Find all the regex permutations of lesser_s
                lesser_perms = all_regex_permutations(lesser_s)

                # Concatenate the operator to the end of all the lesser_perms,
                # and update perms with these permutations
                perms.update({(perm + op) for perm in lesser_perms})

        # For each type of binary operator found in s
        for op in BINARY_OP:
            if(op in s):
                # Make a slice of s with one less occurence of the
                # operator, '(', and ')'
                lesser_s = remove_occurences(s, (op, '(', ')'))

                # For each possible way to divide lesser_s into
                # two non-empty strings:
                for (left, right) in split_combinations(lesser_s):

                    # Get all possible regex permutations of (left, right).
                    # Format it like this: "({l_perm}{op}{r_perm})"
                    # And add it to perms
                    for l_perm in all_regex_permutations(left):
                        for r_perm in all_regex_permutations(right):
                            perms.add("({}{}{})".format(l_perm, op, r_perm))

        return perms


def remove_occurences(s, chars):
    """(str, iterable of char) -> str
    Return a new string with the first occurences of each char in chars
    removed from s.

    REQ: all characters in chars must occur in s
    raise ValueError if REQ not met

    >>> remove_occurences('spam_ham_eggs', 'sam_')
    'pham_eggs'
    >>> remove_occurences('spam_ham_eggs', ('s', 'a', 'm', '_'))
    'pham_eggs'
    """
    # Convert s to a list.
    # This is neccessary because list supports remove, while str does not
    s_list = list(s)

    # for each char in chars, remove in from s_list
    for char in chars:
        s_list.remove(char)

    # convert s_list back into a string and return it
    return ''.join(s_list)


def split_combinations(s):
    R"""(str) -> set of {tuple of (str, str)}
    Return the set of all possible ways (combinations of characters) to
    split s into two non-empty strings.

    Order of characters does not matter.

    >>> split_combinations('01*') ==\
    ... {('*', '01'), ('1', '0*'), ('0', '1*'),
    ...  ('01', '*'), ('0*', '1'), ('1*', '0')}
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
            # Also add the reverse combination
            split_combs.add((left_over_chars, comb))

    return split_combs


def n_combinations(s, n):
    R"""(str, int) -> set of str
    Return the set of all combinations of n characters in s.

    Order of characters does not matter.

    REQ: 0 <= n <= len(s)

    >>> n_combinations('1234', 1) == {'1', '2', '3', '4'}
    True
    >>> n_combinations('1234', 2) == \
    ... {'12', '13', '14', '23', '24', '34'}
    True
    >>> len(n_combinations('1234567890', 5)) == 252
    True
    """
    # Base case: if REQ not met, no combinations are possible
    if((n <= 0) or (n > len(s))):
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


def regex_match(r, s):
    R"""(RegexTree, str) -> bool
    Return True iff s matches the regular expression represented by the
    RegexTree r

    >>> regex_match(build_regex_tree('((1.(0|1)*).2)'), '10110012')
    True
    >>> regex_match(build_regex_tree('((1.(0|1)*).2)'), '12')
    True
    >>> regex_match(build_regex_tree('((1.(0|1)*).2)'), '21')
    False
    >>> regex_match(build_regex_tree('((1.(0|1)*).2)'), '122')
    False
    >>> regex_match(build_regex_tree('(((1.(0|1)*).2)|e)'), '')
    True
    >>> regex_match(build_regex_tree('((0*|1*)*.2)'), '000112')
    True
    """
    # If the regex succeessfuly matches the entire length of the string,
    # return True
    (num_chars_matched, match_success) = num_matched(r, s)
    if(match_success and (num_chars_matched == len(s))):
        return True
    else:
        return False


def num_matched(r, s):
    """(RegexTree, str) -> (int, bool)
    Return the index of the first character in s that is not matched by the
    regular expression represented by the RegexTree r, as well as whether
    or not the this match attempt is considered to have succeeded.

    Format of return tuple: (num_chars_matched, match_success)

    >>> num_matched(build_regex_tree('(1.2)'), '12012')
    (2, True)
    >>> num_matched(build_regex_tree('(1.2)'), '21012')
    (0, False)
    >>> num_matched(build_regex_tree('(1.2)'), '1')
    (0, False)
    >>> num_matched(build_regex_tree('(1|2)'), '12121200012')
    (1, True)
    >>> num_matched(build_regex_tree('(1|2)'), '21121200012')
    (1, True)
    >>> num_matched(build_regex_tree('(1|2)'), '02121200012')
    (0, False)
    >>> num_matched(build_regex_tree('(1*|e)'), '111')
    (3, True)
    >>> num_matched(build_regex_tree('(1*|e)'), '222')
    (0, True)
    >>> num_matched(build_regex_tree('1****'), '111212100')
    (3, True)
    >>> num_matched(build_regex_tree('1****'), '111')
    (3, True)
    >>> num_matched(build_regex_tree('2****'), '111212100')
    (0, True)
    >>> num_matched(build_regex_tree('1****'), '')
    (0, True)
    >>> num_matched(build_regex_tree('e'), '')
    (0, True)
    """
    # Base case: if r represents 'e'
    if(r.symbol == 'e'):
        # e dosen't match any characters, but it always succeeds
        return (0, True)

    # Base case: if r represents '0', '1', or '2'
    elif(r.symbol in {'0', '1', '2'}):
        # If the zeroth character of s matches the regex symbol,
        # one character is successfuly matched
        if(r.symbol == s[:1]):
            return (1, True)
        # Otherwise, the match fails
        else:
            return (0, False)

    # Recursive decomposition:

    # r represents '*' operator
    elif(r.symbol == '*'):
        # Try to match child with string
        (num_chars_matched, match_success) = num_matched(r.children[0], s)
        # Keep track of total number of characters already matched
        total_match = num_chars_matched
        # Keep trying to match if at least one character matched the last time
        while(num_chars_matched > 0):
            # Don't include the characters in s that are already matched
            (num_chars_matched, match_success) = \
                num_matched(r.children[0], s[total_match:])
            # Keep track of total
            total_match += num_chars_matched
        # Return the total number of characters matched
        # Always considered a success, even if no characters are matched
        return (total_match, True)

    # r represents '|' operator
    elif(r.symbol == '|'):
        # Match left and right child with string
        (l_num_matched, l_success) = num_matched(r.children[0], s)
        (r_num_matched, r_success) = num_matched(r.children[1], s)
        # if both children match, find out which one matched more characters
        # and return its num_matched
        if(l_success and r_success):
            return (max((l_num_matched, r_num_matched)), True)
        # if one of the children match, return its num_matched
        elif(l_success):
            return (l_num_matched, True)
        elif(r_success):
            return (r_num_matched, True)
        # Otherwise, the match failed
        else:
            return (0, False)

    # r represents '.' operator
    elif(r.symbol == '.'):
        # Match left child with string
        (l_num_matched, l_success) = num_matched(r.children[0], s)
        # if left child did not match, then there can't be a match for r
        if(not l_success):
            return (0, False)
        else:
            # Match right child with string, excluding the characters
            # already matched by left child
            (r_num_matched, r_success) = \
                num_matched(r.children[1], s[l_num_matched:])
            # if right child matched, return the total number of characters
            # matched by left and right child.
            # if not, the match failed
            if(r_success):
                return ((l_num_matched + r_num_matched), True)
            else:
                return (0, False)

    # Unsupported operator
    else:
        return (0, False)


def build_regex_tree(regex):
    R"""(str) -> RegexTree
    Using the regular expression in regex, build and return a RegexTree
    representing regex.

    REQ: regex must be a valid regular expression
    If REQ not met, raise ValueError

    >>> build_regex_tree("(((0*.1)|2).(e|0*))") == \
    ... DotTree(BarTree(DotTree(StarTree(Leaf('0')), Leaf('1')), Leaf('2')), \
    ... BarTree(Leaf('e'), StarTree(Leaf('0'))))
    True
    """
    # Deal with REQ violation
    if(not is_regex(regex)):
        raise ValueError('regex must be a valid regular expression')
    # Rest of code assumes that regex is valid

    # Base case: one-character regex
    if(len(regex) == 1):
        # Create and return a leaf with the regex as the symbol
        return Leaf(regex)

    # Recursive decomposition:

    # Last character is a unary operator
    elif(regex[-1] in UNARY_OP):
        # Get the class corresponding to the unary operator
        unary_op_class = UNARY_OP[regex[-1]]
        # Use a slice of regex excluding the last char (the operator)
        # to create a tree, and set it to be the subtree of this unary op
        return unary_op_class(build_regex_tree(regex[:-1]))

    # Regex is a binary operation
    else:
        # Parse the left, operator, and right strings from regex
        (left, op, right) = parse_binary_operation(regex)
        # Get the class corresponding to the operator
        binary_op_class = BINARY_OP[op]
        # Use left and right to create subtrees for this binary operator
        return binary_op_class(build_regex_tree(left),
                               build_regex_tree(right))


if(__name__ == '__main__'):
    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
