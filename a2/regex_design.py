"""
CSCA48 Assignment 2 Part 1
Written by Xiuqi (Rex) Xia
"""


class RegexNode(object):
    """
    Represents a node in a regex tree
    """

    def __init__(self, regex_symbol, operands):
        """(RegexNode, str, iterable of RegexNode) -> NoneType
        Create a new RegexNode, with symbol as its representation in a
        regular expression, and with the nodes in operands as its child nodes
        The 0th node in operands is the left operand, and the 1th node in
        operands is the right operand.

        If this RegexNode has no operands, operands must be an empty iterable
        """
        self._regex_symbol = regex_symbol
        # A tuple is used to store the operands because we will not be
        # allowing the attributes to be changed after intialization
        self._operands = tuple(operands)

        return

    def get_regex_symbol(self):
        """(RegexNode) -> str
        Return the symbol representing this RegexNode in a regular expression
        """
        return self._regex_symbol

    def get_operands(self):
        """(RegexNode) -> tuple of RegexNode
        Return all the child nodes (operands) of this RegexNode as a tuple.

        If this RegexNode has no operands return an empty tuple.
        """
        return self._operands

    def _get_specific_operand(self, index):
        """(RegexNode) -> RegexNode
        Return the operand at index
        Return None if it does not exist

        >>> n = RegexNode('spam', ())
        >>> n._get_specific_operand(0) is None
        True
        >>> n._get_specific_operand(1) is None
        True
        """
        # Try to return the element at index
        try:
            return self._operands[index]
        except IndexError:
            # If the operand does not exist, return None instead
            return None

    def get_left_operand(self):
        """(RegexNode) -> RegexNode
        Return the left operand of RegexNode.
        Return None if it does not exist
        """
        # Try to return the operand at index 0
        return self._get_specific_operand(0)

    def get_right_operand(self):
        """(RegexNode) -> RegexNode
        Return the right operand of RegexNode.
        Return None if it does not exist
        """
        # Try to return the operand at index 1
        return self._get_specific_operand(1)

    def _repr_formatter(self, init_params):
        """(RegexNode, iterable of obj) -> str
        Format and return a string that has self's class name, followed by
        a comma separated list of the reprs of the init_params in parentheses

        >>> a = RegexNode('spam', ())
        >>> a._repr_formatter(('ham', (1,2,3), 'eggs'))
        "RegexNode('ham', (1, 2, 3), 'eggs')"
        """
        # Get the name of self's class
        class_name = type(self).__name__

        # Get the repr string of each init_param,
        # and join them together into a string with comma separation
        init_params_repr = ", ".join(repr(param) for param in init_params)

        # Format the string and return it
        return "{}({})".format(class_name, init_params_repr)

    def __repr__(self):
        """(RegexNode) -> str
        Return a string representation of self that can be used as a valid
        Python statement to reconstruct an equivalent node/tree to self.
        """
        # Format the repr string with the regex symbol and operands as the
        # init parameters
        return self._repr_formatter((self.get_regex_symbol(),
                                     self.get_operands()))

    def __str__(self, indent=''):
        """(RegexNode, str) -> str
        Return a string representation of self that shows the structure
        of the tree with indentation.
        """

        # a list of lines to be formed into a string at the end
        lines = []

        # Add the first line, showing indentation, an arrow, and self's symbol
        lines.append(indent + '\-> ' + repr(self.get_regex_symbol()))

        # Add a line for each subtree, with four more spaces of indentation
        for subtree in (self.get_operands()):
            lines.append(subtree.__str__(indent + '    '))

        # Join all the lines (with newline separating lines), and return it
        return '\n'.join(lines)

    def __eq__(self, other):
        R"""(RegexNode, RegexNode) -> bool
        Return True iff the regex symbol of self and other are the same,
        and they both contain the same operands in the same order

        Note that the order of the operands is important. If they are not in
        the same order, they are not equal

        >>> RegexNode('.', (RegexNode('1', ()), RegexNode('0', ()))) ==\
        ... RegexNode('.', (RegexNode('1', ()), RegexNode('0', ())))
        True
        >>> RegexNode('.', (RegexNode('1', ()), RegexNode('0', ()))) ==\
        ... RegexNode('.', (RegexNode('0', ()), RegexNode('1', ())))
        False
        >>> RegexNode('.', (RegexNode('1', ()), RegexNode('0', ()))) ==\
        ... RegexNode('|', (RegexNode('1', ()), RegexNode('0', ())))
        False
        """
        # Make sure other is a RegexNode
        if(isinstance(other, RegexNode)):
            # Check that regex symbol is the same
            return ((self.get_regex_symbol() == other.get_regex_symbol()) and
                    # Check that the operands are the same and in the same
                    # order(using tuple comparison)
                    (self.get_operands() == other.get_operands()))
        else:
            # If other is not a RegexNode it can't be equal
            return False


class NullaryRegexNode(RegexNode):
    """
    Represents a RegexNode with no operands (a leaf node).
    """

    def __init__(self, regex_symbol, match_string):
        """(NullaryRegexNode, str) -> NoneType
        Create a new NullaryRegexNode with regex_symbol as its regex symbol,
        and match_string as the string that this regex symbol matches
        eg: regex symbol '1' matches string '1'
            regex symbol 'e' matches string ''
        """
        # Initialize match_string (since it is unique to NullaryRegexNode)
        self._match_string = match_string

        # Use an empty tuple for operands in RegexNode init
        RegexNode.__init__(self, regex_symbol, ())

        return

    def get_match_string(self):
        """(NullaryRegexNode) -> str
        Return the string that self matches
        """
        return self._match_string

    def __repr__(self):
        """(NullaryRegexNode) -> str
        Return a string representation of self that can be used as a valid
        Python statement to reconstruct an equivalent node/tree to self.
        """
        # Format the repr string with regex symbol and match string as the
        # init parameters
        return self._repr_formatter((self.get_regex_symbol(),
                                     self.get_match_string()))

    def __eq__(self, other):
        """(NullaryRegexNode, RegexNode) -> bool
        Return True iff self and other have the same regex symbol and
        the same match string.

        >>> a = NullaryRegexNode('0','spam')
        >>> b = NullaryRegexNode('0','0')
        >>> a == b
        False

        >>> a = NullaryRegexNode('0','0')
        >>> b = NullaryRegexNode('0','0')
        >>> a == b
        True

        >>> a = NullaryRegexNode('0','0')
        >>> b = RegexNode('0',())
        >>> a == b
        False
        """
        # Make sure other is a NullaryRegexNode
        if(isinstance(other, NullaryRegexNode)):
            # Check the regex symbol and match string for equivalency
            return ((self.get_regex_symbol() == other.get_regex_symbol()) and
                    (self.get_match_string() == other.get_match_string()))
        else:
            # If it's not a NullaryRegexNode, it can't be equal
            return False


class LiteralRegexNode(NullaryRegexNode):
    """
    Represents a NullaryRegexNode where the regex symbol is the same as the
    string it matches
    """

    def __init__(self, symbol):
        """(LiteralRegexNode, str) -> NoneType
        Create a LiteralRegexNode, with symbol as both the regex symbol and
        the string it matches
        """
        # Use the same symbol for both regex_symbol and match_string
        # in NullaryRegexNode init
        NullaryRegexNode.__init__(self, symbol, symbol)
        return

    def __repr__(self):
        """(LiteralRegexNode) -> str
        Return a string representation of self that can be used as a valid
        Python statement to reconstruct an equivalent node/tree to self.
        """
        # Format the repr string with the regex symbol as the init parameter
        # (a one element tuple)
        return self._repr_formatter((self.get_regex_symbol(),))


class EpsilonRegexNode(NullaryRegexNode):
    """
    Represents a NullaryRegexNode where the regex symbol is 'e' and the
    match string is '' (empty string)
    """

    def __init__(self):
        """(EpsilonRegexNode) -> NoneType
        Create a new EpsilonRegexNode
        """
        # Use 'e' for the regex_symbol and '' for the match string
        # in NullaryRegexNode init
        NullaryRegexNode.__init__(self, 'e', '')
        return

    def __repr__(self):
        """(EpsilonRegexNode) -> str
        Return a string representation of self that can be used as a valid
        Python statement to reconstruct an equivalent node/tree to self.
        """
        # Format the repr string with no init parameters (empty tuple)
        return self._repr_formatter(())


class UnaryRegexNode(RegexNode):
    """
    Represents a RegexNode with only one operand
    """

    def __init__(self, regex_symbol, operand):
        """(UnaryRegexNode, str, RegexNode) -> NoneType
        Create a new UnaryRegexNode with regex_symbol as its regex symbol, and
        operand as its only child node.
        """
        # Use a one-element tuple for the operands in RegexNode init
        RegexNode.__init__(self, regex_symbol, (operand,))
        return

    def __repr__(self):
        """(UnaryRegexNode) -> str
        Return a string representation of self that can be used as a valid
        Python statement to reconstruct an equivalent node/tree to self.
        """
        # Format the repr string with regex_symbol and the
        # left operand (the only operand it has) as the init parameters
        return self._repr_formatter((self.get_regex_symbol(),
                                     self.get_left_operand()))


class StarRegexNode(UnaryRegexNode):
    """
    Represents a UnaryRegexNode where the regex_symbol is '*'
    """

    def __init__(self, operand):
        """(StarRegexNode, RegexNode) -> NoneType
        Create a new StarRegexNode with operand as the child node
        """
        # Use '*' as regex_symbol in UnaryRegexNode init
        UnaryRegexNode.__init__(self, '*', operand)
        return

    def __repr__(self):
        """(StarRegexNode) -> str
        Return a string representation of self that can be used as a valid
        Python statement to reconstruct an equivalent node/tree to self.
        """
        # Format the repr string with the left operand as the
        # init parameters (in an one element tuple)
        return self._repr_formatter((self.get_left_operand(),))


class BinaryRegexNode(RegexNode):
    """
    Represents a RegexNode with two operands
    """

    def __init__(self, regex_symbol, left_operand, right_operand):
        """(BinaryRegexNode, str, RegexNode, RegexNode) -> NoneType
        Create a new BinaryRegexNode with regex_symbol as its regex symbol
        and left_operand, right_operand as its child nodes
        """
        # Use left/right operands as the operands in RegexNode init
        RegexNode.__init__(self, regex_symbol, (left_operand, right_operand))
        return

    def __repr__(self):
        """(BinaryRegexNode) -> str
        Return a string representation of self that can be used as a valid
        Python statement to reconstruct an equivalent node/tree to self.
        """
        # Format the repr string with the regex symbol, and the left/right
        # operands
        return self._repr_formatter((self.get_regex_symbol(),
                                     self.get_left_operand(),
                                     self.get_right_operand()))


class BarRegexNode(BinaryRegexNode):
    """
    Represents a BinaryRegexNode where the regex symbol is '|'.
    This regex operator exhibits commutative property
    """

    def __init__(self, left_operand, right_operand):
        """(BarRegexNode, RegexNode, RegexNode) -> NoneType
        Create a BarRegexNode with left_operand and right_operand as the
        operands
        """
        # Initialize BinaryRegexNode, with '|' as regex symbol
        BinaryRegexNode.__init__(self, '|', left_operand, right_operand)
        return

    def __repr__(self):
        """(BarRegexNode) -> str
        Return a string representation of self that can be used as a valid
        Python statement to reconstruct an equivalent node/tree to self.
        """
        # Format the repr string with the left/right operands
        return self._repr_formatter((self.get_left_operand(),
                                     self.get_right_operand()))

    def __eq__(self, other):
        R"""(BarRegexNode, RegexNode) -> bool
        Return True iff the regex symbol of self and other are the same,
        and they both contain the same left and right operands

        Note that the order of the operands does not matter, due to the
        commutative property of BarRegexNode

        >>> BarRegexNode(LiteralRegexNode('1'),
        ...              LiteralRegexNode('0')) ==\
        ... BarRegexNode(LiteralRegexNode('1'),
        ...              LiteralRegexNode('0'))
        True
        >>> BarRegexNode(LiteralRegexNode('1'),
        ...              LiteralRegexNode('0')) ==\
        ... BarRegexNode(LiteralRegexNode('0'),
        ...              LiteralRegexNode('1'))
        True
        >>> BarRegexNode(LiteralRegexNode('1'),
        ...              LiteralRegexNode('0')) ==\
        ... BarRegexNode(LiteralRegexNode('1'),
        ...              LiteralRegexNode('1'))
        False
        >>> BarRegexNode(LiteralRegexNode('1'),
        ...              LiteralRegexNode('0')) ==\
        ... RegexNode('|',
        ...           (LiteralRegexNode('1'),
        ...            LiteralRegexNode('0')))
        True
        """
        # Make sure other is a RegexNode
        if(isinstance(other, RegexNode)):
            # If the regex symbol of self and other are not the same,
            # then they are definitely not equivalent
            if(self.get_regex_symbol() != other.get_regex_symbol()):
                return False

            else:
                # Get the left/right operands of self and other
                (self_left, self_right) = (self.get_left_operand(),
                                           self.get_right_operand())
                (other_left, other_right) = (other.get_left_operand(),
                                             other.get_right_operand())

                # Check if the combinations of self/other left/right are
                # equilvalent
                return ((self_left, self_right) == (other_left, other_right) or
                        (self_left, self_right) == (other_right, other_left))

        else:
            # If other is not a RegexNode, it can't be equal
            return False


class DotRegexNode(BinaryRegexNode):
    """
    Represents a BinaryRegexNode where the regex symbol is '.'
    """

    def __init__(self, left_operand, right_operand):
        """(DotRegexNode, RegexNode, RegexNode) -> NoneType
        Create a DotRegexNode with left_operand and right_operand as the
        operands
        """
        # Initialize BinaryRegexNode, with '.' as regex symbol
        BinaryRegexNode.__init__(self, '.', left_operand, right_operand)
        return

    def __repr__(self):
        """(DotRegexNode) -> str
        Return a string representation of self that can be used as a valid
        Python statement to reconstruct an equivalent node/tree to self.
        """
        # Format the repr string with the left/right operands
        return self._repr_formatter((self.get_left_operand(),
                                     self.get_right_operand()))


if(__name__ == '__main__'):
    import doctest
    doctest.testmod()

    #test_tree1 = \
        #RegexNode('.', (
            #RegexNode('.', (
                #RegexNode('2', ()),
                #RegexNode('*', (
                    #RegexNode('|', (
                        #RegexNode('0', ()),
                        #RegexNode('1', ()),
                    #)),
                #)),
            #)),
            #RegexNode('*', (
                #RegexNode('e', ()),
            #)),
        #))

    #print(test_tree1)
    #print(repr(test_tree1))
    #print('eval repr check:', test_tree1 == eval(repr(test_tree1)))
    #print('---\n')

    #test_tree2 = \
        #BinaryRegexNode('.',
            #BinaryRegexNode('.',
                #NullaryRegexNode('2', '2'),
                #UnaryRegexNode('*',
                    #BinaryRegexNode('|',
                        #NullaryRegexNode('0', '0'),
                        #NullaryRegexNode('1', '1'),
                    #),
                #),
            #),
            #UnaryRegexNode('*',
                #NullaryRegexNode('e', ''),
            #),
        #)

    #print(test_tree2)
    #print(repr(test_tree2))
    #print('eval repr check:', test_tree2 == eval(repr(test_tree2)))
    #print('---\n')

    #test_tree3 = \
        #DotRegexNode(
            #DotRegexNode(
                #LiteralRegexNode('2'),
                #StarRegexNode(
                    #BarRegexNode(
                        #LiteralRegexNode('0'),
                        #LiteralRegexNode('1'),
                    #),
                #),
            #),
            #StarRegexNode(
                #EpsilonRegexNode()
            #),
        #)

    #print(test_tree3)
    #print(repr(test_tree3))
    #print('eval repr check:', test_tree3 == eval(repr(test_tree3)))
    #print('---\n')

    #print("test_tree2 == test_tree3")
    #print(test_tree2 == test_tree3)
