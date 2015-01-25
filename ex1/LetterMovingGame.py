# A class representing the BANANA game (CSCA48 Excercise 01),
# or variants thereof
# Written by Xiuqi (Rex) Xia

from Containers import *


class ContainerTypeError(Exception):
    """Exeption raised by LetterMovingGame when an invalid container_type
    is entered.
    """
    pass


class NoSuchCommandError(Exception):
    """Exeption raised by LetterMovingGame when a command is unrecognized
    """
    pass


class InvalidCommandError(Exception):
    """Exeption raised by LetterMovingGame when an invalid command is entered
    """
    pass


class LetterMovingGame():
    """
    A class representing the BANANA game (CSCA48 Excercise 01).
    (Also supports variants with non-BANANA source words)
    
    Note to those writing client code for this class:
    The prefered way to issue commands to the game is to pass a string
    containing a user command to the do_cmd method. It is also possible to
    directly call some of methods associated with the commands, which is
    useful in the case of save_to_file, which allows the client to specify
    a filename in the parameters. However, _move, _put, and _get should not
    be called directly, because calling them directly does not update
    the operation history stack.
    """
    
    def __init__(self, source_word, target_word, container_type):
        """(LetterMovingGame, str, str, str, int) -> NoneType
        
        Create a LetterMovingGame that starts with source_word and tries
        to get to target_word using a container, whose type is specified by 
        container_type.
        
        container_type can be either 'Queue', 'Stack', or 'Bucket'
        (not case sensitive)
        An invaid container_type will raise a ContainerTypeError.
        """
        
        # These are the currently implemented container types
        str_to_container = {'QUEUE': Queue,
                            'STACK': Stack,
                            'BUCKET': Bucket}
        
        # Convert container_type to all caps, for case-insensitivity
        container_type = container_type.upper()
        
        # Check if the container_type is invalid
        if not (container_type in str_to_container.keys()):
            raise ContainerTypeError
        
        self._container_type = container_type
        
        # Initialize the container (starts out empty),
        # using the class corresponding to containter_type
        self._container = str_to_container[container_type]()
        
        self._source_word = source_word
        self._target_word = target_word
        
        # A queue is used to store the letters of the source word
        self._source = Queue(self._source_word)
        
        # The stack for the target word starts out empty
        self._target = Stack()
        
        # This is a stack for storing the history of
        # valid operations peformed during the game.
        # (see CSCA48 exercise 01 for the rules)
        # Each op_history element will be
        # a tuple of (operation:str, letter:str)
        # operation can be either 'MOVE', 'PUT', or 'GET'
        self._op_history = Stack()
        
        # Dict to associate the names of user commands
        # with their corresponding methods
        self._cmd_to_methods = \
            {'MOVE': self._move,
             'PUT': self._put,
             'GET': self._get,
             'UNDO': self.undo,
             'PARAMETERS': self.print_param,
             'STATE': self.print_state,
             'HISTORY': self.print_hist,
             'GIVEUP': self.giveup,
             'SAVE': self.save_to_file,
             'HELP': self.print_help
             }
        
        # Remember to keep this help str up-to-date with changes in the code
        self._cmd_help_str = (
            "Allowed commands (not case sensitive):\n"
            "'MOVE': move a letter from source to target\n"
            "'PUT': move a letter from source to container\n"
            "'GET': move a letter from container to target\n"
            "'UNDO': undo the last command\n"
            "'PARAMETERS': print the source word,\n" 
            "              target word, and container type\n"
            "'STATE': print the current state of source, container,\n"
            "         and target\n"
            "'HISTORY': print the history of operations performed\n"
            "           during the game\n"
            "'GIVEUP': Clears the operations history, source, container,\n"
            "          and target. Operations history is set to\n"
            "          'Impossible!'\n"
            "'SAVE': Appends the game parameters and operations history\n"
            "        to the file called 'ex1.txt'\n"
            "'HELP': Show this help string"
            )
        
        # Set of commands considered to be operations
        # (non-operation commands will not be added to self._op_history
        # when they are performed)
        self._operations = {'MOVE', 'PUT', 'GET'}
        
        return
    
    def __str__(self):
        """Return a string with the operation history,
        parameters, and current state of the game in a 
        user-friendly format.
        """
        # A list to store each line of the eventual string
        lines = []
        
        lines.append('Operations history:')
        lines.append(self.str_hist())
        lines.append('---')
        lines.append('Game parameters:')
        lines.append(self.str_param())
        lines.append('---')
        lines.append('Current state:')
        lines.append(self.str_state())
        
        return '\n'.join(lines)
    
    def str_param(self):
        """Return a string with the parameters of the game in a 
        human-readable format.
        """
        # Format a string for the game parameters
        param_line = "{0} -> {1}, using a {2}".format(self._source_word,
                                                      self._target_word,
                                                      self._container_type)
        
        return param_line
    
    def str_state(self):
        """Return a string with the current state of the game in a 
        human-readable table format.
        """
        
        # This method uses str.format() and its special syntax for formatting
        
        # There should only ever be 3 column_labels, due to hard-coding
        # in one of the later steps below
        column_labels = ("Source", "Container", "Target")
        
        # Find out what the maximum width of the table column should be
        # (longest one out of column_labels and source_word)
        column_data = column_labels + (self._source_word,)
        max_width = 0
        for s in column_data:
            max_width = max(max_width, len(s))
        
        # Create a string used to format each cell to the max_width
        cell_format = '{:' + str(max_width) + '}'
        
        # Create string used to format a line of the table:
        # Separate each cell_format with ' | '
        # There should be as many cells in one row as there are column_labels
        line_format = ' | '.join([cell_format] * len(column_labels))
        # ^ Should produce something like '{:9} | {:9} | {:9}'
        
        # A list to store each line of the eventual string
        lines = []
        
        # Format a line for the column labels.
        # Unfortunately, must hard-code to only use 3 column labels
        lines.append(line_format.format(column_labels[0],
                                        column_labels[1],
                                        column_labels[2]))
        
        # Format a line for the source, container, target
        # Must use join on source, container, and target because we want
        # them to appear as words, not as the deque representation
        lines.append(line_format.format(''.join(self._source),
                                        ''.join(self._container),
                                        ''.join(self._target)))
        
        # Assemble string and return it
        return '\n'.join(lines)

    def str_hist(self):
        """Return a string with the operation history of the game in a
        human-readable format.
        """
        # A list to store each line of the eventual string
        lines = []
                
        # Format the line for each record in self._op_history
        for record in self._op_history:
            (op, letter) = record
            lines.append(op + '(' + letter + ')')
        
        return '\n'.join(lines)
    
    def str_help(self, additional_lines =[]):
        """(LetterMovingGame, list of str) -> str
        Return a string that gives the user a list of allowed commands
        and their descriptions.
        
        If any lines are in additional_lines, they will be appended
        to the end of the help string
        """
        # A list to store lines of the eventual string
        lines = []
        
        lines.append(self._cmd_help_str)
        
        # Add the lines from additional lines
        for s in additional_lines:
            lines.append(s)
        
        # Assemble string and return it
        return '\n'.join(lines)
    
    def print_param(self):
        """Print parameters of the game in a user-friendly format.
        """
        print(self.str_param())    
    
    def print_state(self):
        """Print the current state of the game in a user-friendly format.
        """
        print(self.str_state())
    
    def print_hist(self):
        """Print the current operation history of the game in a 
        user-friendly format.
        """
        print(self.str_hist())
    
    def print_help(self):
        """Print the help string"""
        print(self.str_help())
    
    def get_param(self):
        """(LetterMovingGame) -> tuple of (str, str, str)
        
        Return the source word, target word, and container type in a tuple
        (in that order)
        """
        return (self._source_word, self._target_word, self._container_type)
    
    def get_hist(self):
        """(LetterMovingGame) -> Stack of (tuple of(str, str))
        
        Return the operations history stack, as a new Stack.
        Each record (element of the list) consists of
        a tuple of(operation, letter)
        Earlier records have lower index numbers than later records
        """
        return Stack(self._op_history)
    
    def get_state(self):
        """(LetterMovingGame) -> tuple of (str, str, str)
        
        Return the current state of the source queue, container, and target
        stack as a tuple of strings (in that order)
        """
        return (''.join(self._source),
                ''.join(self._container),
                ''.join(self._target)
                )
    
    def _get_put(self, source, target, undo=False):
        """(LetterMovingGame, container, container) -> str
        
        Get a letter from source, and puts it into target.
        Return the letter that is transfered.
        
        If undo is True, it will instead unput a letter from target,
        and unget it into source
        """
        if(not undo):
            letter = source.get()
            try:
                target.put(letter)
            # If this fails (target is full), unget the letter,
            # and re-raise the error (to inform the calling funcs)
            except IndexError:
                source.unget(letter)
                raise IndexError
        else:
            letter = target.unput()
            source.unget(letter)
        
        return letter
    
    def _move(self, undo=False):
        """(LetterMovingGame, [bool]) -> str
        
        Move a letter from self._source to self._target
        Return the letter moved.
        
        If undo is True, it will instead unmove a letter from
        self._target to self._source
        """
        # Set source and target
        (source, target) = (self._source, self._target)
        
        # do the operation and return the letter transfered
        return self._get_put(source, target, undo)
    
    def _put(self, undo=False):
        """(LetterMovingGame, [bool]) -> str
        
        Put a letter from self._source into self._container
        Return the letter put.
        
        If undo is True, it will instead unput a letter from
        self._container to self._source
        """
        # Set source and target
        (source, target) = (self._source, self._container)
        
        # do the operation and return the letter transfered
        return self._get_put(source, target, undo)
    
    def _get(self, undo=False):
        """(LetterMovingGame, [bool]) -> str
        
        Get a letter from self._container and put it into self._target
        Return the letter gotten.
        
        If undo is True, it will instead unget a letter from
        self._target to self._container
        """
        # Set source and target
        (source, target) = (self._container, self._target)
        
        # do the operation and return the letter transfered
        return self._get_put(source, target, undo)
    
    def undo(self):
        """Undo the last operation recorded in self._op_history,
        and remove its record from self._op_history
        """
        
        # Get (and delete) the last record from the operation history stack
        record = self._op_history.get()     # Pop from stack
        
        # Unpack data in record
        (op, letter) = record
        
        # Perform the op, but with undo set to True
        self._cmd_to_methods[op](undo=True)
        
        return
    
    def giveup(self):
        """Clears the operations history, source queue, container,
        and target stack. Operations history is set to 'Impossible!'
        """
        
        self._op_history.clear()
        # The '0' is to take the place of an expected element
        self._op_history.put(('Impossible!','0'))
        
        self._source.clear()
        self._container.clear()
        self._target.clear()
        
        return
    
    def save_to_file(self, filename='ex1.txt'):
        """
        Appends the game parameters and operations history
        to the file named in filename
        """
        
        # Assemble game parameters, operations history into
        # a string to be written to file
        str_to_be_written = '\n'.join(('\n---',
                                       self.str_param(),
                                       '',
                                       self.str_hist(),
                                       '---\n'
                                       ))
        
        # Write the string to file
        file = open(filename, 'a')
        file.write(str_to_be_written)
        file.close()
        
        return
    
    def do_cmd(self, cmd):
        """(LetterMovingGame, str) -> NoneType
        
        Accept a command (cmd), and execute it
        Allowed commands are:
            'MOVE': move a letter from source to target
            'PUT': move a letter from source to container
            'GET': move a letter from container to target
            'UNDO': undo the last command
            'PARAMETERS': print the source word, 
                          target word, and container type
            'STATE': print the current state of source, container, and target
            'HISTORY': print the history of operations performed
                       during the game
            'GIVEUP': Clears the operations history, source, container,
                      and target. Operations history is set to 'Impossible!'
            'SAVE': Appends the game parameters and operations history
                    to the file called 'ex1.txt'
        *Commands are not case sensitive
        
        Raise NoSuchCommand if command is not recognized
        Raise InvalidCommand if command cannot be executed
            (eg: when trying to use PUT when the bucket container is full)
        """
        
        # Convert cmd to uppercase for case-insensitivity
        cmd = cmd.upper()
        
        # Check if the command is recognized
        if not (cmd in self._cmd_to_methods.keys()):
            raise NoSuchCommandError
        
        # Try to do the command, and remember the letter transfered
        try:
            # Need to remember letter to put in operation history
            letter = self._cmd_to_methods[cmd]()
        except IndexError:
            raise InvalidCommandError
        
        # If the command is an operation, add the command and the letter
        # to the operation history
        if(cmd in self._operations):
            self._op_history.put((cmd, letter))
        
        return


if(__name__ == '__main__'):
    # Code for testing
    g = LetterMovingGame('BANANA', 'ANANAB', 'QUEUE')
    g.do_cmd('move')
    g.do_cmd('put')
    g.do_cmd('put')
    g.do_cmd('get')