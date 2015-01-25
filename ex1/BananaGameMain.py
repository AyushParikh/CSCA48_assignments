# A command line user interface used to play
# the BANANA game (CSCA48 Excercise 01)
# Requires the LetterMovingGame and Containers modules
# Written by Xiuqi (Rex) Xia

from LetterMovingGame import *

DEFAULT_SOURCE_WORD = 'BANANA'
DEFAULT_TARGET_WORD = 'AAABNN'

def start_game():
    """Starts the BANANA game
    """
    
    print('Welcome to the BANANA game command-line user interface!\n')
    
    source_word = input('Enter the source word, '
                        'or a blank line to use the default:\n')
    if(source_word == ''):
        source_word = DEFAULT_SOURCE_WORD
    source_word = source_word.upper()   # For case-insensitivity
    
    target_word = input('Enter the target word, '
                        'or a blank line to use the default:\n')
    if(target_word == ''):
        target_word = DEFAULT_TARGET_WORD
    target_word = target_word.upper()   # For case-insensitivity
    
    # Keep asking for a container type until a valid one is entered
    keep_going = True
    while(keep_going):
        container_type = input('Enter the container type\n'
                               '(QUEUE, STACK, or BUCKET): ')
        # Try to create a game, if container_type is not valid, 
        # loop again
        try:
            game = LetterMovingGame(source_word, target_word, container_type)
            keep_going = False  # loop exits
        except ContainerTypeError:
            print('\nInvalid container type!')
            # keep_going remains True, so will loop again
    
    # run the main game loop
    run_game(game)
    
    # if you don't like autoprint, use this:
    # run_game(game, autoprint=False)
    
    return


def run_game(game, autoprint=True):
    """(LetterMovingGame, [bool]) -> NoneType
    
    Ask for user commands, run them on game, and display the results
    Exit when the user enters 'Quit' (case-insensitive)
    
    Iff autoprint is True, information about the game will be printed
    each time the user enters a command.
    """
    
    # Some constants for client commands
    QUIT_CMD = 'QUIT'
    QUIT_DESCRIP = "'QUIT': Exits the program"
    HELP_CMD = 'HELP'
    CLIENT_CMDS = {QUIT_CMD, HELP_CMD}
    DESCRIP_LINES = [QUIT_DESCRIP]
    
    print('\n---Game starting now!---')
    print('Enter ' + HELP_CMD + ' for information on allowed commands')
    
    # Display initial state of the game
    print('\n' + str(game) + '\n')
    
    keep_going = True
    while(keep_going):
        # Reset error messages
        error_msg = []
        
        # Prompt for a user command
        cmd = input('>>> ')
        cmd = cmd.upper()
        
        # Pass cmd on to game if it's not a client command
        if not(cmd in CLIENT_CMDS):
            # Try to perform the command, if fail, set an error messge
            try:
                game.do_cmd(cmd)
            except NoSuchCommandError:
                error_msg.append('***No such command!***')
            except InvalidCommandError:
                error_msg.append('***Invalid Command!***')
        # cmd is help
        elif(cmd == HELP_CMD):
            # print help, with an additional line describing the quit cmd
            print(game.str_help(additional_lines=DESCRIP_LINES))
        # cmd is quit
        else:
            return  # Exit program immediately

        # Display current state of the game if autoprint is on
        if(autoprint):
            print('\n' + str(game) + '\n')
        
        # Display error messages, if any
        for msg in error_msg:
            print(msg)
        
        # Check if the game has been won
        (source, target, container_type) = game.get_param()
        (cur_source, cur_container, cur_target) = game.get_state()
        if(cur_target == target):
            print('***Congratulations, you won!***')
    
    return


if(__name__ == '__main__'):
    start_game()