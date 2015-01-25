# Copyright 2013, 2014 Gary Baumgartner, Danny Heap, Dustin Wehr,
# Xiuqi (Rex) Xia
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2014.
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
TOAHModel:  Model a game of Towers of Anne Hoy
Cheese:   Model a cheese with a given (relative) size
IllegalMoveError: Type of exceptions thrown when an illegal move is attempted
MoveSequence: Record of a sequence of (not necessarily legal) moves. You will 
need to return MoveSequence object after solving an instance of the 4-stool 
Towers of Anne Hoy game, and we will use that to check the correctness of your
algorithm.
"""


class TOAHModel:
    """Model a game of Towers Of Anne Hoy.

    Model stools holding stacks of cheese, enforcing the constraint
    that a larger cheese may not be placed on a smaller one.

    fill_first_stool - put an existing model in the standard starting config
    move - move cheese from one stool to another
    add - add a cheese to a stool        
    top_cheese - top cheese on a non-empty stool
    cheese_location - index of the stool that the given cheese is on
    number_of_cheeses - number of cheeses in this game
    number_of_moves - number of moves so far
    number_of_stools - number of stools in this game
    get_move_seq - MoveSequence object that records the moves used so far
     
    """
    
    def __init__(self: 'TOAHModel', num_stools: int):
        """
        Create a TOAHModel with the number of stools specified in num_stools.
        
        Note: If num_stools is zero or less, the TOAHModel will not contain
        any stools, so there will be no way to add Cheeses to it
        """
        
        # Create a list of sublists to represent each stool
        # Each sublist represents a stool and will contain Cheeses
        self._stools = [[] for i in range(num_stools)]
        
        # Remember the number of stools
        self._num_stools = num_stools
        
        # Start off with no cheeses
        self._num_cheeses = 0
        
        # Initialize an empty MoveSequence
        self._move_seq = MoveSequence([])
        
        return

    def fill_first_stool(self: 'TOAHModel', number_of_cheeses: int):
        """
        Put number_of_cheeses cheeses on the first (i.e. 0-th) stool, in order 
        of size, with a cheese of size == number_of_cheeses on bottom and 
        a cheese of size == 1 on top.
        
        If this TOAHModel already has Cheeses in it,
        or if this TOAHModel does not have a first stool,
        raise IllegalMoveError
        """
        # Check to see if self already has Cheeses in it
        if(self.number_of_cheeses() > 0):
            raise IllegalMoveError("Cannot fill first stool because TOAModel " 
                                   "has already been filled.")
        
        # Add Cheeses to the first (0th) stool.
        # The biggest Cheese (with size = number_of_cheeses) is added first, 
        # and the smallest Cheese (with size = 1) is added last.
        for i in range(number_of_cheeses, 0, -1):
            self.add(0, Cheese(i))
            # ^ will raise IllegalMoveError if the 0th stool does not exist
        
        # Update the total number of cheese in self
        self._num_cheeses = number_of_cheeses
        
        return

    def __eq__(self: 'TOAHModel', other: 'TOAHModel') -> bool:
        """
        We're saying two TOAHModels are equivalent if their current 
        configurations of cheeses on stools look the same. 
        More precisely, for all h,s, the h-th cheese on the s-th 
        stool of self should be equivalent the h-th cheese on the s-th 
        stool of other
        
        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(7)
        >>> m1.move(0,1)
        >>> m1.move(0,2)
        >>> m1.move(1,2)
        >>> m2 = TOAHModel(4)
        >>> m2.fill_first_stool(7)
        >>> m2.move(0,3)
        >>> m2.move(0,2)
        >>> m2.move(3,2)
        >>> m1 == m2
        True
        """
        # If the stool lists in each TOAHModel are equilvalent,
        # then the arrangement of Cheeses and stools is equivalent.
        return (self._stools == other._stools)
    
    def number_of_cheeses(self: 'TOAHModel') -> int:
        """
        Return the total number of Cheeses in this TOAHModel
        """
        return self._num_cheeses
    
    def number_of_stools(self: 'TOAHModel') -> int:
        """
        Return the number of stools in this TOAHModel
        """
        return self._num_stools
    
    def __str__(self: 'TOAHModel') -> str:       
        """
        Depicts only the current state of the stools and cheese.
        """
        stool_str = "=" * (2 * (self.number_of_cheeses()) + 1)
        stool_spacing = "  "
        stools_str = (stool_str + stool_spacing) * self.number_of_stools()
        
        # Add the index of each stool as a label under the stools_str
        
        # New line for the stool indices
        stools_str += '\n'
        # List to store each stool label
        stool_labels = []
        # Iterate through the indices of all the stools
        for i in range(self.number_of_stools()):
            # Centre-justify the index within the width of a stool
            stool_labels.append(
                ('{:^' + str(len(stool_str)) + '}').format(str(i)))
        # Add space between stool labels, and add the stool labels line
        # to stools_str
        stool_labels = stool_spacing.join(stool_labels)
        stools_str += stool_labels
        
        def cheese_str(size: int):            
            if size == 0:
                return " " * len(stool_str)
            cheese_part = "-" + "--" * (size - 1)
            space_filler = " " * int((len(stool_str) - len(cheese_part)) / 2)
            return space_filler + cheese_part + space_filler
        
        lines = ""
        for height in range(self.number_of_cheeses() - 1, -1, -1):
            line = ""
            for stool in range(self.number_of_stools()):
                c = self._cheese_at(stool, height)
                if isinstance(c, Cheese):
                    s = cheese_str(int(c.size))
                else:
                    s = cheese_str(0)
                line += s + stool_spacing
            lines += line + "\n"
        lines += stools_str
        
        return lines

    def cheese_location(self: 'TOAHModel', cheese: 'Cheese') -> int:
        """
        Find and return the index of the stool that cheese is on
        in this TOAHModel
        
        Raise ValueError if the cheese is not found.
        """
        # Loop through all stools and all Cheeses until cheese is found
        # Remember the stool_index and return it
        
        stool_index = 0
        found = False
        
        # loop through stools
        while((not found) and (stool_index < len(self._stools))):
            curr_stool = self._stools[stool_index]
            cheese_index = 0
            
            # loop through Cheeses
            while((not found) and (cheese_index < len(curr_stool))):
                curr_cheese = curr_stool[cheese_index]
                if(curr_cheese is cheese):
                    # cheese has been found
                    found = True
                    # Remember the current stool_index
                    found_stool_index = stool_index
                
                cheese_index += 1
            
            stool_index += 1
        
        # If cheese had not been found, raise ValueError
        if(not found):
            raise ValueError("cheese was not found in the TOAHModel")
        else:
            return found_stool_index
    
    def _cheese_at(self: 'TOAHModel', stool_index, 
                   stool_height: int) -> 'Cheese':
        """
        If there are at least stool_height+1 cheeses 
        on stool stool_index then return the (stool_height)-th one.
        
        If the cheese or the stool does not exist at the specified location,
        return None
        
        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M._cheese_at(0,3).size
        2
        >>> M._cheese_at(0,0).size
        5
        """
        # Try to get the Cheese specified
        try:
            return self._stools[stool_index][stool_height]
        
        # If there is an IndexError, the cheese does not exist at the
        # specified location, so return None
        except IndexError:
            return None
    
    def top_cheese(self: 'TOAHModel', stool_index: int) -> 'Cheese':
        """
        Return the top (smallest) Cheese at the specified stool_index.
        If there are no Cheeses on the stool at stool_index,
        or if the stool does not exist, return None.
        """
        # The top cheese is always at the last position of a stool, 
        # so use an index of -1 to get it.
        return self._cheese_at(stool_index, -1)
    
    def add(self: 'TOAHModel', stool_index: int, add_cheese: 'Cheese'):
        """
        Add the add_cheese to this TOAHModel at the indicated stool_index.
        
        If the cheese to be added has a greater size than the top Cheese
        on the stool, raise IllegalMoveError.
        
        If the stool does not exist, raise IllegalMoveError
        """
        # Get top cheese from stool_index
        curr_top_cheese = self.top_cheese(stool_index)
        
        # Check if the top cheese exists
        # If so, raise exception if the cheese to be added is bigger than
        # the top cheese
        if((curr_top_cheese is not None) and
           (add_cheese.size > curr_top_cheese.size)):
            
            raise IllegalMoveError("Cannot put a bigger cheese on a "
                                   "smaller one.")
        
        # Try to add the cheese
        try:
            self._stools[stool_index].append(add_cheese)
        except IndexError:
            # The stool does not exist, so raise IllegalMoveError
            raise IllegalMoveError("Cannot put a cheese onto a stool "
                                   "that does not exist.")
            
        return
    
    def _pop_top_cheese(self: 'TOAHModel', stool_index: int) -> 'Cheese':
        """
        Remove and return the top Cheese at the specifed stool_index.
        Raise an InvalidMoveError if there are no Cheeses at stool_index,
        or if the stool does not exist
        """
        # Try to get the target stool
        try:
            target_stool = self._stools[stool_index]
        except IndexError:
            # The stool does not exist, so raise IllegalMoveError
            raise IllegalMoveError("Cannot remove a cheese from a stool that "
                                   "does not exist.")
        
        # Try to pop the top Cheese(last element) from target_stool
        try:
            popped_cheese = target_stool.pop()
        # If an IndexError is raised, there are no Cheeses in target_stool,
        # so raise an IllegalMoveError
        except IndexError:
            raise IllegalMoveError("Cannot move a cheese from an empty stool.")
        
        return popped_cheese
    
    def move(self: 'TOAHModel', src_stool: int, dest_stool: int):
        """
        Remove the top Cheese from src_stool and add it onto dest_stool.
        
        If this cannot be done according to the rules of the game,
        raise IllegalMoveError.
        """
        # Check if the user is trying to move a Cheese
        # from and to the same stool
        if(src_stool == dest_stool):
            raise IllegalMoveError("Source stool and destination stool "
                                   "cannot be the same stool.")
        
        # Pop the top cheese from src_stool
        move_cheese = self._pop_top_cheese(src_stool)
        # Code will stop here if top cheese cannot be popped
        # (IllegalMoveError raised)
        
        # Try to add move_cheese to dest_stool
        # and register the move with the MoveSquence
        try:
            self.add(dest_stool, move_cheese)
            # This move will not get registered with the MoveSequence
            # if unable to add move_cheese to the dest_stool
            self.get_move_seq().add_move(src_stool, dest_stool)
        
        except IllegalMoveError:
            # If unable to add the move_cheese to dest_stool,
            # must put the cheese back in src_stool
            # before passing the exception along
            self.add(src_stool, move_cheese)
            raise
        
        return

    def get_move_seq(self: 'TOAHModel') -> 'MoveSequence':
        """
        Return the MoveSequence of this TOAModel
        """
        return self._move_seq
    
    def number_of_moves(self: 'TOAHModel') -> int:
        """
        Return the number of moves in the MoveSequence of this TOAModel
        """
        return self._move_seq.length()
    
    
class Cheese:
    def __init__(self: 'Cheese', size: int):
        """
        Initialize a Cheese to diameter size.

        >>> c = Cheese(3)
        >>> isinstance(c, Cheese)
        True
        >>> c.size
        3
        """
        self.size = size

    def __repr__(self: 'Cheese') -> str:
        """
        Representation of this Cheese
        """
        return "Cheese(" + str(self.size) + ")"

    def __eq__(self: 'Cheese', other: 'Cheese') -> bool:
        """Is self equivalent to other? We say they are if they're the same 
        size."""
        return isinstance(other, Cheese) and self.size == other.size
    
       
class IllegalMoveError(Exception):
    """
    An exception to indicate that a move (adding/removing cheeses)
    cannot be conpleted
    """
    pass

       
class MoveSequence:
    def __init__(self: 'MoveSequence', moves: list):
        # moves - a list of integer pairs, e.g. [(0,1),(0,2),(1,2)]
        self._moves = moves
            
    def get_move(self: 'MoveSequence', i: int):
        # Exception if not (0 <= i < self.length)
        return self._moves[i]
        
    def add_move(self: 'MoveSequence', src_stool: int, dest_stool: int):
        self._moves.append((src_stool, dest_stool))
        
    def length(self: 'MoveSequence') -> int:
        return len(self._moves)
    
    def generate_TOAHModel(self: 'MoveSequence', number_of_stools: int, 
                           number_of_cheeses: int) -> 'TOAHModel':
        """
        An alternate constructor for a TOAHModel. Takes the two parameters for
        the game (number_of_cheeses, number_of_stools), initializes the game
        in the standard way with TOAHModel.fill_first_stool(number_of_cheeses),
        and then applies each of the moves in this move sequence.
        """
        model = TOAHModel(number_of_stools)
        model.fill_first_stool(number_of_cheeses)
        for move in self._moves:
            model.move(move[0], move[1])
        return model
        
    def __repr__(self: 'MoveSequence') -> str:
        return "MoveSequence(" + repr(self._moves) + ")"


if __name__ == '__main__':
    import doctest
    doctest.testmod()
