# Written by Huimin (Cinny) Cao

import unittest
import ex2

class TestSwitchBoard(unittest.TestCase):
    def setUp(self):
        self._small_board = ex2.SwitchBoard(5)
        
    def tearDown(self):
        print('I just finished one test! o^.^o')
    
    def test_default_state(self):
        self.assertEqual(self._small_board.which_switch(),
                         [],
                         'Your switches should all be off in the beginning. Check __init__')
        self.assertEqual(self._small_board.__str__(),
                         'The following switches are on:  ',
                         'Is there any typo? Check __str__!')
    
    def test_which_switch(self):
        self._small_board.flip(2)
        self.assertNotEqual(self._small_board.which_switch(),
                            ['2'],
                            'which_switch should return a list of int, I got a list of str :(')        
        self.assertEqual(self._small_board.which_switch(),
                         [2],
                         'flip() with n=2 fails')
    
    def test_str(self):
        self._small_board.flip(2)
        self.assertEqual(self._small_board.__str__(),
                         'The following switches are on:  2',
                         '__str__ goes wrong')
        self._small_board.flip(0)
        self.assertEqual(self._small_board.__str__(),
                         'The following switches are on:  0 2',
                         '__str__ goes wrong')
        
    def test_flip_simple(self):
        self._small_board.flip(0)
        self.assertEqual(self._small_board.which_switch(),
                         [0],
                         'flip() with n=0 fails; cannot flip it on')
        self._small_board.flip(0)
        self.assertEqual(self._small_board.which_switch(),
                         [],
                         'flip() with n=0 fails; cannot flip it off')
            
    def test_flip_every_simple(self):
        self._small_board.flip_every(1)
        self.assertEqual(self._small_board.which_switch(),
                         [0, 1, 2, 3, 4],
                         'flip_every() with n=1 fails')
        self._small_board.flip(3)
        self.assertEqual(self._small_board.which_switch(),
                         [0, 1, 2, 4],
                         'flip() fails')
        self._small_board.flip_every(2)
        self.assertEqual(self._small_board.which_switch(),
                         [1],
                         'playing with flip_every() fails')
        
    def test_ISIExc_with_negative_int(self):
        #should raise InvalidSwitchIndexException
        #when a negative int is provided to either flip() or flip_every()
        self.assertRaises(ex2.InvalidSwitchIndexException,
                          self._small_board.flip,
                          -1)
        self.assertRaises(ex2.InvalidSwitchIndexException,
                          self._small_board.flip_every,
                          -1)

    def test_ISIExc_with_greater_int(self):
        #for flip_every()
        #should raise InvalidSwitchIndexException
        #if provided a parameter that is greater than the num of switches
        self.assertRaises(ex2.InvalidSwitchIndexException,
                          self._small_board.flip_every,
                          6)
        
    def test_NSSExc_for_flip(self):
        #for flip()
        #should raise NoSuchSwitchException 
        #when input is greater or equal than num of switches
        self.assertRaises(ex2.NoSuchSwitchException,
                          self._small_board.flip,
                          6)
        self.assertRaises(ex2.NoSuchSwitchException,
                          self._small_board.flip,
                          5)
            
    def test_reset_with_all_on_switches(self):
        self._small_board.flip_every(1)
        self.assertEqual(self._small_board.which_switch(),
                         [0, 1, 2, 3, 4],
                         'flip_every() with n=1 fails')        
        self._small_board.reset()
        self.assertEqual(self._small_board.which_switch(),
                         [],
                         'Testing reset fails')
    
    def test_reset_with_some_on_switces(self):
        self._small_board.flip(2)
        self.assertEqual(self._small_board.which_switch(),
                         [2],
                         'flip() fails')
        try:
            self._small_board.reset()
            self.assertEqual(self._small_board.which_switch(),
                             [],
                             'Testing reset fails')
        except:
            self.fail('reset() shouldn\'t produce any exceptions')
                
    def test_with_Light_Switch_Problem(self):
        self._2014_board = ex2.SwitchBoard(2014)
        for i in range(1, 2014):
            self._2014_board.flip_every(i)
        self.assertEqual(self._2014_board.__str__(),
                         'The following switches are on:  0 1 4 9 16 25 36 49 64 81 100 121 144 169 196 225 256 289 324 361 400 441 484 529 576 625 676 729 784 841 900 961 1024 1089 1156 1225 1296 1369 1444 1521 1600 1681 1764 1849 1936',
                         'Your answer for the 2014 Light Switch Problem is wrong.')

print('')
print('Note: If which_switch fails, all other methods may fail')
print('')
print('Start working now!!')
print('')
unittest.main(exit = False)
print('All tests finished! LOL')
input('Press Enter to exit')
