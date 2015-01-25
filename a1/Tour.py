# Copyright 2013, 2014 Gary Baumgartner, Danny Heap, Dustin Wehr,
# Xiuqi (Rex) Xia
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Fall 2013.
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
from TOAHModel import TOAHModel

import time

# Magic numbers:
# Indices for each of the stools in a 4-stool TOAHModel
SRC_INDEX = 0
TEMP0_INDEX = 1
TEMP1_INDEX = 2
DEST_INDEX = 3


def tour_of_four_stools(model: 'TOAHModel', delay_btw_moves: float=0.5, 
                        console_animate: bool=False):
    """Move a tower of cheeses from the first stool in model to the fourth.

       model - a TOAHModel with a tower of cheese on the first stool
                and three other empty stools
       console_animate - whether to animate the tour in the console
       delay_btw_moves - time delay between moves in seconds IF 
                         console_animate == True
                         no effect if console_animate == False
    
    >>> m = TOAHModel(4)
    >>> m.fill_first_stool(8)
    >>> tour_of_four_stools(m)
    >>> m.get_move_seq().length()
    33
    """
    
    # Use helper function to solve the problem
    four_stool_move(model, model.number_of_cheeses(), 
                    SRC_INDEX,                   # src_stool
                    DEST_INDEX,                  # dest_stool
                    (TEMP0_INDEX, TEMP1_INDEX))  # temp_stools
    
    # If animation is requested
    if(console_animate):
        # Get the MoveSequence from model
        move_seq = model.get_move_seq()
        
        # Create and set up a new 4-stool TOAHModel to animate
        anim_model = TOAHModel(4)
        anim_model.fill_first_stool(model.number_of_cheeses())
        # Print the initial state of anim_model
        print(anim_model)
        
        # Go through each move in move_seq
        for i in range(move_seq.length()):
            # Get the source and destination stool indices
            (src_stool, dest_stool) = move_seq.get_move(i)
            
            # Delay the next move
            time.sleep(delay_btw_moves)
            
            # Apply the move
            anim_model.move(src_stool, dest_stool)
            
            # Print the result
            print(anim_model)
    
    return


def four_stool_move(model: 'TOAHModel',
                    n: int,
                    src_stool: int,
                    dest_stool: int,
                    temp_stools: 'tuple of (int, int)'):
    """
    Using recursion, move a tower of n cheeses in model from the top of
    src_stool to dest_stool, using two temp_stools as intermediates.
    
    >>> m = TOAHModel(4)
    >>> m.fill_first_stool(8)
    >>> four_stool_move(m, 8, 0, 3, (1, 2))
    >>> m.get_move_seq().length()
    33
    """
    
    # Base case: if no cheeses need to be moved, do nothing
    if (n <= 0):
        return
    
    # Base case: if there is only one cheese to move,
    # move it directly to the dest_stool
    elif (n == 1):
        model.move(src_stool, dest_stool)
        return
    
    # Recursive decomposition: Use Anne Hoy's TOAH algorithm
    else:
        # Get the optimal i value from an optimal_i_generator starting at n
        op_i = optimal_i_generator(n)
        i = next(op_i)
        
        # Anne Hoy's step 1: Move n - i cheese rounds to an intermediate 
        # stool (temp_stools[0]) using all four stools.
        four_stool_move(model,
                        (n - i),                        # new n
                        src_stool,                      # new src
                        temp_stools[0],                 # new dest
                        (dest_stool, temp_stools[1]))   # new temps
        
        # Anne Hoy's step 2: Move i cheese rounds from the origin stool to 
        # the destination stool, using the 3 remaining stools
        # (temp_stools[0] is used by step 1, so cannot use it in this step)
        three_stool_move(model,
                         i,               # new n
                         src_stool,       # new src
                         dest_stool,      # new dest
                         temp_stools[1])  # new temp
        
        # Anne Hoy's step 3: Move the n-i smallest cheese rounds from the 
        # intermediate stool to the destination stool, using all four stools
        four_stool_move(model,
                        (n - i),                      # new n
                        temp_stools[0],               # new src
                        dest_stool,                   # new dest
                        (src_stool, temp_stools[1]))  # new temps
        
        return


def three_stool_move(model: 'TOAHModel',
                     n: int,
                     src_stool: int,
                     dest_stool: int,
                     temp_stool: int):
    """
    Using recursion, move a tower of n cheeses in model from the top of
    src_stool to dest_stool, using the temp_stool as an intermediate.
    
    >>> m = TOAHModel(4)
    >>> m.fill_first_stool(8)
    >>> three_stool_move(m, 8, 0, 2, 1)
    >>> m.get_move_seq().length()
    255
    """
    
    # Base case: if no cheeses need to be moved, do nothing
    if (n <= 0):
        return
    
    # Recursive decomposition: use Tower of Hanoi algorithm,
    # as demonstrated by Brian Harrington in CSCA48
    else:
        # move n-1 cheeses from src to temp, using dest as intermediate
        three_stool_move(model, (n - 1),
                         src_stool, temp_stool, dest_stool)
        
        # move the last cheese from src to dest
        model.move(src_stool, dest_stool)
        
        # move n-1 cheeses from temp to dest, using src as intermediate
        three_stool_move(model, (n - 1),
                         temp_stool, dest_stool, src_stool)
        
        return

# The following two functions were used to find the optimal values of i
# Unfortunately, the recursion takes way too long to run when n > 20ish,
# so these functions are not actually used in the code.
# However, I did notice a pattern in the i-values, which I used to write a 
# generator function that generates optimal i-values more efficiently than
# the recursive functions.
# (see optimal_i_generator below)

def num_moves_req(n: int, i: int) -> int:
    """
    Calculate and return the number of moves required to move n cheeses using
    Anne Hoy's 4-stool TOAH algorithm. i is a parameter of the TOAH algorithm.
    
    REQ: i must be between 1 and n-1 (greater than 0 and less than n)
    Return None if req not met
    
    >>> num_moves_req(5, 4)
    17
    >>> num_moves_req(5, 3)
    13
    >>> num_moves_req(5, 2)
    13
    >>> num_moves_req(5, 1)
    19
    """
    # Base case: if no cheeses need to be moved, then no moves required
    if (n <= 0):
        return 0
    
    # Base case: if there is only one cheese to move,
    # can just move it directly to the destination in one move.
    elif (n == 1):
        return 1
    
    # if i is not valid return none
    elif ((i < 1) or (i > n-1)):
        return None
    
    # Recursive decomposition:
    # Use optimal_i to find the best i to use for moving n-i cheeses.
    # Plug the new i into math pilgrim's recursive formula
    else:
        # Mutual recursion
        new_i = optimal_i(n-i)
        
        # n-1 approach
        # Using math pilgrim's recursive formula
        return (2 * num_moves_req(n - i, new_i) + 2**i - 1)


def optimal_i(n: int) -> int:
    """
    Return the value of i that requires the least number of moves when
    using Anne Hoy's 4-stool TOAH algorithm on n cheeses.
    
    >>> optimal_i(5)
    2
    >>> optimal_i(15)
    5
    """
    
    # Base case: if only one or less cheeses need to be moved,
    # then there's no need to use i, (can just move to destination directly)
    if(n <= 1):
        return 0
    
    # Base case: if 2 cheeses need to be moved, the only valid value of i is 1
    elif(n == 2):
        return 1
    
    # Recursive decomposition: Mutual recursion
    # Call num_moves_req for each possible value of i,
    # and return the one that requires the least number of moves
    else:
        # List to store values of i and the number of moves required
        # Each element is a tuple of (num_moves, i)
        moves_i = []
        
        # All possible values of i are from 1 to n-1 (inclusive)
        for i in range(1, n):
            moves_i.append((num_moves_req(n, i), i))
        
        # Find the minimum number of moves required
        # This uses tuple comparison. Since num_moves is first, 
        # it will be the one to be compared
        min_moves_i = min(moves_i)
        
        # Return the i that leads to the lowest number of moves required.
        # i is at the 1th index location in the tuple
        return min_moves_i[1]

# These are the optimal i values (for n up to 25) generated by optimal_i:
# optimal_i_values = [0, 0, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 
#                     5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6]
# The index of each i value corresponds to the value of n.
# For example: optimal_i_vals[10] is the optimal i value when n = 10
#
# The following generator works by using the pattern I noticed in the above
# list of optimal i values
# 
# This is the pattern:
# Start with [0, 0, 1]
# The next 3 elements are 2
# The next 4 elements are 3
# The next 5 elements are 4
# The next 6 elements are 5
# and so on...

def optimal_i_generator(starting_n: int) -> 'generator object':
    """
    Generate a sequence of optimal i values, starting from starting_n cheeses.
    The optimal i is the value of i that requires the least number of moves 
    when using Anne Hoy's 4-stool TOAH algorithm on n cheeses.
    
    >>> g = optimal_i_generator(0)
    >>> l = []
    >>> for i in range(26):
    ...     l.append(next(g))
    >>> l == [0, 0, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 
    ...       6, 6, 6, 6, 6]
    True
    """
    # Intialize n as starting_n
    n = starting_n
    
    # Initialize the first 3 values of the list of optimal i-values.
    # The index of each i value corresponds to the value of n.
    # For example: op_i_vals[1] is the optimal i value when n = 1
    op_i_vals = [0, 0, 1]
    
    # main loop
    while(True):
        # Try to get the optimal i value by looking in op_i_vals
        try:
            # Using yield instead of return, so that when the function gets
            # called again, it remembers its previous state
            yield op_i_vals[n]
            # increment n for the next call
            n += 1          
        
        except IndexError:
            # If the optimal i value is not available, generate more i-values
            # until the length of op_i_vals is greater than n
            while(not (len(op_i_vals) > n)):
                # Apply the pattern to op_i_vals
                # See comments above header for details
                pattern_num = op_i_vals[-1] + 1
                op_i_vals += [pattern_num] * (pattern_num + 1)


if __name__ == '__main__': 
    
    #import doctest
    #doctest.testmod()
    
    ## Print a table of optimal i values and the number of moves required
    ## with 4 stools compared with 3 stools for n up to 20
    ## Also, create a list to store all the optimal i values
    #op_i_vals = []
    #for n in range(21):
        #i = optimal_i(n)
        ##print(n, i, num_moves_req(n, i), 2**n-1)
        #op_i_vals.append(i)
    #print(op_i_vals)
    
    ## Use the generator to generate a sequence of optimal i values up to n=50
    #g = optimal_i_generator(0)
    #l = []
    #for i in range(51):
        #l.append(next(g))
    #print(l)
    
    NUM_CHEESES = 8
    DELAY_BETWEEN_MOVES = .5
    CONSOLE_ANIMATE = False
    #CONSOLE_ANIMATE = True
    
    # DO NOT MODIFY THE CODE BELOW.
    four_stools = TOAHModel(4)    
    four_stools.fill_first_stool(number_of_cheeses=NUM_CHEESES)
    
    tour_of_four_stools(four_stools, 
                        console_animate=CONSOLE_ANIMATE,
                        delay_btw_moves=DELAY_BETWEEN_MOVES)
    
    print(four_stools.number_of_moves())
    
    