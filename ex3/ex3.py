# CSCA48 Excercise 3
# Written by Xiuqi (Rex) Xia
import math


class Parallelogram:
    """A shape defined by base, side, and theta
    """
    
    def __init__(self, base, side, theta):
        """(Parallelogram, float, float, float) -> NoneType
        Create a Parallelgram with the specified base, side, and
        theta (in degrees).
        """
        # convert parameters to floats, in case they are ints
        (base, side, theta) = map(float, (base, side, theta))
        
        self._base, self._side, self._theta = base, side, theta
        
        # If mask does not exist yet, set it
        # (in case subclasses have already set mask, we don't want to 
        # change its value)
        self._set_mask_bst([True, True, True])
        
        return
    
    def _set_mask_bst(self, mask):
        """(Parallelogram, list of [bool, bool, bool]) -> NoneType
        If self._mask_bst does not exist yet, set it to mask.
        If self._mask_bst does exist, leave it alone.
        
        self._mask_bst: 
        The elements in this list correspond to base, side, theta.
        If the element in mask is False, zero will take the place of the 
        corresponding value in the list returned by the bst method
        
        >>> pllel._set_mask_bst([True, True, True])
        """
        # See if self._mask_bst exists
        try:
            self._mask_bst
        # If it dosent exist, AttributeError will be raised
        except AttributeError:
            self._mask_bst = mask
        return
    
    def __str__(self):
        """(Parallelogram) -> str
        Return a string representation of self
        
        >>> str(pllel)
        'I am a Parallelogram with area 123.4'
        """
        return 'I am a {} with area {}'.format(self.__class__.__name__,
                                               self.area())
    
    def height(self):
        """(Parallelogram, optional float) -> float
        Return the height of self.
        
        >>> pllel.height()
        123.4
        """
        # Use trigonometry
        return self._side * math.sin(math.radians(self._theta))
    
    def area(self):
        """(Parallelogram) -> float
        Return the area of self.
        
        >>> pllel.area()
        123.4
        """
        # General equation for area of parallelogram
        return (self._base * self.height())
    
    def bst(self):
        """(Parallelgram) -> list of [float, float, float]
        Return a list of the base, side, and theta of self.
        If a value is not neccessary, 0.0 takes its place.
        
        >>> pllel.bst()
        [10.0, 5.0, 45.0]
        >>> rhom.bst()
        [10.0, 0.0, 45.0]
        >>> rect.bst()
        [10.0, 5.0, 0.0]
        >>> sq.bst()
        [10.0, 0.0, 0.0]
        """
        
        # List containing base, side, theta
        bst_list = [self._base, self._side, self._theta]
        
        # Apply the mask to bst_list
        bst_list = [(bst_list[i] if self._mask_bst[i] else 0.0) 
                    for i in range(len(bst_list))]
        
        return bst_list


class Rectangle(Parallelogram):
    """A Rectangle is a Parallelogram with theta == 90
    """
    def __init__(self, base, side):
        """(Rectangle, float, float) -> NoneType
        Create a Rectangle with the specified base and side.
        """
        # Set mask: require base, side, but not theta
        self._set_mask_bst([True, True, False])
        
        # Use Parallelogram's init, with theta set to 90
        theta = 90
        Parallelogram.__init__(self, base, side, theta)
        
        return
    
    def height(self):
        """(Rectange) -> float
        Return the height of self, which is the same is its side.
        
        >>> rect.height()
        123.4
        """
        return self._side


class Rhombus(Parallelogram):
    """A Rhombus is a Parallelogram with side == base
    """
    def __init__(self, base, theta):
        """(Rhombus, float, float) -> NoneType
        Create a Rhombus with the specified base and theta (in degrees)
        """
        # Set mask: require base, does require not side, require theta
        self._set_mask_bst([True, False, True])
        
        # Use Parallelogram's init, with side == base
        Parallelogram.__init__(self, base, base, theta)
        
        return


class Square(Rectangle, Rhombus):
    """A Square is both a Rectangle and a Rhombus.
    Its side == base, and theta == 90.
    """
    
    def __init__(self, base):
        """(Square, float) -> NoneType
        Create a Square with the specified base.
        """
        # Set mask: require base, but neither side, nor theta
        self._set_mask_bst([True, False, False])
        
        # Use Rectangle's init, with side == base
        Rectangle.__init__(self, base, base)
        
        return
