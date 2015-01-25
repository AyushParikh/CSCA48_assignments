# Written by Huimin (Cinny) Cao

import unittest
from ex2 import LightSwitch,InvalidSwitchException

class TestLightSwitch(unittest.TestCase):
    def setUp(self):
        self._switch_on = LightSwitch('on')
        self._switch_off = LightSwitch('off')
    
    def tearDown(self):
        print('I just finished one test! o^.^o')
    
    def test_str(self):
        self.assertEqual(self._switch_on.__str__(), 
                         'I am on',
                         'Your switch doesn\'t tell the truth;check your __str__')
        self.assertEqual(self._switch_off.__str__(),
                         'I am off',
                         'Your switch doesn\'t tell the truth;check your __str__')
    
    def test_turn_on_off_normal(self):
        self._switch_off.turn_on()
        self.assertEqual(self._switch_off.__str__(),
                         'I am on',
                         'I cannot turn on the switch!Check turn_on!')
        self._switch_on.turn_off()
        self.assertEqual(self._switch_on.__str__(),
                         'I am off',
                         'I cannot turn off the switch!Check turn_off!')
        
    def test_turn_on_off_exception(self):
        self.assertRaises(InvalidSwitchException,
                          self._switch_on.turn_on)
        self.assertRaises(InvalidSwitchException,
                          self._switch_off.turn_off)
    
    def test_flip(self):
        self._switch_on.flip()
        self._switch_off.flip()
        self.assertEqual(self._switch_on.__str__(),
                         'I am off',
                         'flip goes wrong!')
        self.assertEqual(self._switch_off.__str__(),
                         'I am on',
                         'flip goes wrong!')

print('')
print('Note: If your __str__ method fails,')
print('all other test cases may fail')
print('even if your other methods are right')
print('')
print('Start working!')
print('')
unittest.main(exit = False)
print('All tests compeleted!')
input('Press Enter to exit')
