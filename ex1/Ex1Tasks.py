from BananaGameMain import run_game
from LetterMovingGame import *

def main():
    """Go through all the task/container combinations in ex1, 
    and run the BANANA game for each
    """
    
    source_word = 'BANANA'
    
    # List of tasks
    tasks = ['AAABBN',
             'AAANNB',
             'BBAAAN',
             'BBNAAA',
             'NNAAAB',
             'NNBAAA',
             'ANANAB',
             'NABANA',
             'NANANANABATMAN']
    
    # List of container types
    cont_types = ['QUEUE', 'STACK', 'BUCKET']
    
    # Loop through each task/container combination
    for task in tasks:
        for cont in cont_types:
            # create a LetterMovingGame
            game = LetterMovingGame(source_word, task, cont)
            # run game
            run_game(game)
    
    return

if(__name__ == '__main__'):
    main()