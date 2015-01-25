# Unit test for ex3.py
# Written by Xiuqi (Rex) Xia
import ex3
import unittest
import re


class TestParallelogram(unittest.TestCase):
    def setUp(self):
        self.bst_init = [12.3, 4.56, 78.9]
        (base, side, theta) = self.bst_init
        self.shape = ex3.Parallelogram(base, side, theta)
        
        self.expected_area = 55.03874293799704
        
        self.shape_name = 'Parallelogram'
        
        return
    
    def test_str(self):
        """Use regex to test if the string representation is correct.
        This test passes/fails independently from the area method test.
        """
        
        # Create regex pattern
        expected_pattern = re.compile('I am a ' +
                                      self.shape_name + 
                                      ',? with area ?[:=]? *' + 
                                      '[\d]+\.?[\d]*[\.!1]*',
                                      re.IGNORECASE) # case insensitive
        
        # Get the actual string, and find its start and end
        actual_str = str(self.shape)
        actual_start_end = (0, len(actual_str))
        
        # Match the actual string to the regex pattern
        # Find the start and end of the part of the actual string that matched
        # the regex pattern
        match_result = expected_pattern.match(actual_str)
        # If no part of the string matched, match_result would be None,
        # causing AttributeError to be raised when we try to call its methods
        try:
            match_start_end = (match_result.start(), match_result.end())
        except AttributeError:
            match_start_end = None      # Abritrary value
        
        # If the actual start and end of the str is not the same as the
        # start and end of the match result, then the str does not match
        # the regex pattern completely,
        # so we conclude it is not properly formatted
        self.assertEqual(actual_start_end,
                         match_start_end,
                         "The string representation of your {} is "
                         "formatted incorrectly!".format(self.shape_name)
                         )
    
    def test_area(self):
        """Test the area method.
        """
        self.assertAlmostEqual(self.expected_area, self.shape.area(),
                               7,
                               "Unexpected result from the area method "
                               "of your {}!".format(self.shape_name))
    
    def test_bst(self):
        """Test the bst method.
        """
        self.assertEqual(self.bst_init, self.shape.bst(),
                         "Unexpected result from the bst method "
                         "of your {}!".format(self.shape_name))


class TestRectangle(TestParallelogram):
    def setUp(self):
        self.bst_init = [9.34, 5.2, 0.0]
        (base, side, theta) = self.bst_init
        self.shape = ex3.Rectangle(base, side)
        
        self.expected_area = 48.568
        
        self.shape_name = 'Rectangle'
        
        return


class TestRhombus(TestParallelogram):
    def setUp(self):
        self.bst_init = [14.23, 0.0, 84.5]
        (base, side, theta) = self.bst_init
        self.shape = ex3.Rhombus(base, theta)
        
        self.expected_area = 201.56066285634532
        
        self.shape_name = 'Rhombus'
        
        return


class TestSquare(TestParallelogram):
    def setUp(self):
        self.bst_init = [203.423, 0.0, 0.0]
        (base, side, theta) = self.bst_init
        self.shape = ex3.Square(base)
        
        self.expected_area = 41380.916929
        
        self.shape_name = 'Square'
        
        return


if(__name__ == '__main__'):
    unittest.main(exit=False, verbosity=2)
