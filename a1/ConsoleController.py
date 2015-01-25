# Copyright 2014 Dustin Wehr, Xiuqi (Rex) Xia
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
ConsoleController: User interface for manually solving Anne Hoy's problems 
from the console.

move: Apply one move to the given model, and print any error message 
to the console. 
"""

from TOAHModel import TOAHModel, Cheese, IllegalMoveError


def move(model: TOAHModel, origin: int, dest: int):
    '''
    Module method to apply one move to the given model, and print any
    error message to the console. 
    
    model - the TOAHModel that you want to modify
    origin - the stool number (indexing from 0!) of the cheese you want 
             to move
    dest - the stool number that you want to move the top cheese 
            on stool origin onto.
    
    >>> m = TOAHModel(2)
    >>> m.fill_first_stool(1)
    >>> m.top_cheese(0)
    Cheese(1)
    >>> move(m, 0, 1)
    >>> m.top_cheese(1)
    Cheese(1)
    '''
    # Try to make the move with model
    try:
        model.move(origin, dest)
    except IllegalMoveError as e:
        # Print the error message
        print("Illegal Move:", e)
    
    return


def input_pos_int(prompt: str, allow_zero: bool) -> int:
    """
    Continue to ask the user for input using prompt until the user inputs a
    valid positive integer.
    Return the integer.
    
    If allow_zero is False, zero will not be allowed as a valid input.
    """
    # Keep trying until the user enters a valid input
    input_valid = False
    while(not input_valid):
        # Input from user using prompt
        user_inp = input(prompt)    # user_inp is a str at this point
        
        # Make sure the input is a valid positive int
        # ValueError will be raised if its not an int or is negative
        try:
            # Convert the user input to a positive int
            user_inp = str_to_pos_int(user_inp, allow_zero)
            # If no exceptions are thrown, the input is valid
            input_valid = True
        
        except ValueError:
            # Inform the user of the input requirements
            if(allow_zero):
                print("Error: Input must be a non-negative integer.")
            else:
                print("Error: Input must be a non-zero positive integer.")
    
    return user_inp


def str_to_pos_int(input_str: str, allow_zero: bool) -> int:
    """
    Convert input_str to an int and return it.
    If input_str does not represent a valid non-negative integer,
    raise ValueError
    If allow_zero is set to False, an input_str of zero will also
    raise ValueError
    """
    # Convert input_str to an int
    result = int(input_str)
    
    # Make sure it is non-negative
    if(result < 0):
        raise ValueError
    
    # If zero is not allowed, zero will also raise error
    if((not allow_zero) and (result == 0)):
        raise ValueError
    
    return result


class EndGameException(Exception):
    """
    Exception raised to tell ConsoleController.play_loop to end the game
    """
    pass


class ConsoleController:
    """
    A console-based interface for controlling a TOAHModel
    """
    
    def __init__(self: 'ConsoleController', 
                 number_of_cheeses: int, number_of_stools: int):
        """
        Initialize a new 'ConsoleController'.

        number_of_cheeses - number of cheese to tower on the first stool
        number_of_stools - number of stools
        """
        # Initialize dict for converting the user command strings
        # to their methods
        self._cmd_to_method = {"MOVE": self.move,
                               "HELP": self.help,
                               "QUIT": self.quit,
                               "EXIT": self.quit}
        
        # Create a TOAHModel with the specified number of stools
        self._model = TOAHModel(number_of_stools)
        
        # Put the TOAHModel in the starting config with the number of cheeses
        self._model.fill_first_stool(number_of_cheeses)
        
        return
    
    def move(self, params: 'list of str'=[]):
        """(ConsoleController, list of str) -> NoneType
        Move a cheese from one stool to another.
        The 0th element of params represents the index of the source stool.
        The 1th element of params represents the index
            of the destination stool.
        
        If the input is invalid, or the move is illegal, 
        print an error message to the screen
        """
        # This method handles errors related to the command parameters entered
        # by the user
        try:
            # Try to convert the first two params to
            # positive ints (zero allowed)
            (src_stool, dest_stool) = (str_to_pos_int(p, True)
                                       for p in (params[0], params[1]))
        except IndexError:
            # Less than two parameters were given
            print("Error: MOVE operation requires two parameters")
            return
        except ValueError:
            # The parameters are not valid non-negative ints
            print("Error: MOVE parameters must be non-negative integers")
            return
        
        # Perform the move using the module function
        # This should print any errors due to illegal moves
        move(self._model, src_stool, dest_stool)
        
        return
    
    def help(self, params: 'list of str'=None):
        """
        Print a list of recognized commands and their discriptions.
        Ignore the content of params.
        """
        
        help_str = (
            "Console controller commands:\n"
            "(not case sensitive)\n"
            "\n"
            "MOVE n1 n2\n"
            "   Move the top cheese from the stool labeled n1\n"
            "   to the stool labeled n2.\n"
            "   n1 and n2 must be non-negative integers.\n"
            "   Example: MOVE 0 2\n"
            "\n"
            "HELP\n"
            "   Show these instructions again\n"
            "\n"
            "QUIT or EXIT\n"
            "   End this console controller session\n"
        )
        
        print(help_str)
        return
    
    def quit(self, params: 'list of str'=None):
        """(ConsoleController, list of str) -> NoneType
        Raise EndGameException to tell play_loop to end the game.
        Ignore the content of params.
        """
        raise EndGameException
    
    def play_loop(self: 'ConsoleController'):
        '''    
        Console-based game. 
        TODO:
        -Start by giving instructions about how to enter moves (which is up to
        you). Be sure to provide some way of exiting the game, and indicate
        that in the instructions.
        -Use python's built-in function input() to read a potential move from
        the user/player. You should print an error message if the input does
        not meet the specifications given in your instruction or if it denotes
        an invalid move (e.g. moving a cheese onto a smaller cheese).
        You can print error messages from this method and/or from
        ConsoleController.move; it's up to you.
        -After each valid move, use the method TOAHModel.__str__ that we've 
        provided to print a representation of the current state of the game.
        '''
        
        # Print help at the start of the game
        self.help()
        
        # Keep looping until EndGameException is raised
        continue_game = True
        while(continue_game):
            
            # print the current state of the game
            print(self._model)
            
            # Ask user for input
            user_inp = input('ToAH> ')
            
            # Only need to do stuff if the user entered something
            if(user_inp):
                
                # Split user input into words
                user_inp = user_inp.split()
                # The 0th word is the command,
                # convert it to all caps for case-insensitivity
                cmd = user_inp[0].upper()
                # The rest of the words are parameters for the command methods
                params = user_inp[1:]
                
                try:
                    # Try to call the method corresponding to the user command
                    self._cmd_to_method[cmd](params)
                    
                except KeyError:
                    # if the command is unrecognized,
                    # tell the user to try again
                    print("Command unrecognized: please try again\n" 
                          "or type HELP for a list of recognized commands.")
                    
                except EndGameException:
                    # if EndGameException is raised, end the game
                    continue_game = False
        
        return


if __name__ == '__main__':
    
    # Print the welcome message
    welcome_str = "Welcome to the Tour d'Auyne H'Oeuil console controller!"
    print('-' * len(welcome_str))
    print(welcome_str)
    print('-' * len(welcome_str) + '\n')
    
    # Get TOAHModel parameters from user
    num_stools = input_pos_int("Please enter the number of stools: ", False)
    num_cheeses = input_pos_int("Please enter the number of cheeses: ", False)
    
    # Create a ConsoleController and run its play_loop
    controller = ConsoleController(num_cheeses, num_stools)
    print("\nTour d'Auyne H'Oeuil started!")
    print('-' * len(welcome_str) + '\n')
    controller.play_loop()
    
    # Print a quit message
    print("Bye!")
