# CSCA48 Excercise 2
# Written by Xiuqi (Rex) Xia


class InvalidSwitchException(Exception):
    """Raised when a LightSwitch is turned on when it is already on,
    or off when it is already off."""
    pass


class InvalidStateException(Exception):
    """Raised when LightSwitch is initialized with an invalid state.
    """
    pass


class LightSwitch:
    """A representation of a single light switch, which can be either
    on or off"""
    
    def __init__(self, state=False):
        """(LightSwitch, bool or str) -> NoneType
        Create a LightSwitch that is
        off if state is False or "OFF" (case insensitive),
        and on if state is True or "ON" (case insensitive).
        
        If state is an invalid str, InvalidStateException will be raised.
        """
        
        # If state is a string, convert it to all caps (for case insensitivity)
        # and convert it into bool
        # (True if it is "ON", False if it is "OFF")
        if(isinstance(state, str)):
            state = state.upper()
            if (state == "ON"):
                state = True
            elif (state == "OFF"):
                state = False
            else:
                raise InvalidStateException
        
        # Set the state of the switch
        self._on = state
        
        return
    
    def __str__(self):
        """(LightSwitch) -> str
        Return "I am on" if self is on, and "I am off" if self is off.
        
        >>> sw = LightSwitch()
        >>> sw.__str__()
        'I am off'
        >>> sw = LightSwitch('on')
        >>> sw.__str__()
        'I am on'
        """
        return ("I am on" if self._on else "I am off")
    
    def turn_on(self):
        """(LightSwitch) -> NoneType
        Set self to on. Raise InvalidSwitchException if self is already on.
        
        >>> sw = LightSwitch()
        >>> str(sw)
        'I am off!'
        >>> sw.turn_on()
        >>> str(sw)
        'I am on!'
        """
        if self._on:
            raise InvalidSwitchException
        else:
            self._on = True
        return
    
    def turn_off(self):
        """(LightSwitch) -> NoneType
        Set self to off. Raise InvalidSwitchException if self is already off.
        
        >>> sw = LightSwitch('On')
        >>> str(sw)
        'I am on!'
        >>> sw.turn_off()
        >>> str(sw)
        'I am off!'
        """
        if not self._on:
            raise InvalidSwitchException
        else:
            self._on = False
        return

    def flip(self):
        """(LightSwitch) -> NoneType
        Flip the state of self.
        If it's on, it becomes off.
        If it's off, it becomes on.
        
        >>> sw = LightSwitch()
        >>> str(sw)
        'I am off!'
        >>> sw.flip()
        >>> str(sw)
        'I am on!'
        >>> sw.flip()
        >>> str(sw)
        'I am off!'
        """
        self._on = not self._on
    
    def is_on(self):
        """(LightSwitch) -> bool
        Return True iff self is on
        
        >>> sw = LightSwitch("on")
        >>> sw.is_on()
        True
        """
        return self._on


class NoSuchSwitchException(Exception):
    """Raised when SwitchBoard tries to flip a switch that dosent exist
    """
    pass


class InvalidSwitchIndexException(Exception):
    """Raised when the index number provided to SwitchBoard methods are
    invalid (negative, or greater than the number of switches, etc)
    """
    pass


class SwitchBoard:
    """Contains a list of multiple LightSwitches
    """
    def __init__(self, n):
        """(SwitchBoard, int) -> Nonetype
        Create a SwitchBoard with n switches.
        All switches in the SwitchBoard are initialized to off
        """
        
        # Create a list of n LightSwitches
        # Each switch is off (default)
        self._switches = [LightSwitch('off') for i in range(n)]
        
        return
    
    def __str__(self):
        """(SwitchBoard) -> str
        Return a string stating which switches in the SwitchBoard are on
        
        >>> print(swbrd)
        The following switches are on:  0, 3, 8, 9
        """
        
        # Get a list of indices of switches that are on,
        # and cast all indices (int) to str
        on_indices = [str(i) for i in self.which_switch()]
        
        # Join all the indices into a str, with space to separate indices
        result_str = " ".join(on_indices)
        
        # Add a human readable message and return the string
        result_str = "The following switches are on:  " + result_str
        return result_str
    
    def which_switch(self):
        """(SwitchBoard) -> list of int
        Return a list of indices of LightSwitch in self that are on.
        
        >>> swbrd.which_switch()
        [0, 3, 8, 9]
        """
        
        # list to store indices of switches that are on
        on_indices = []
        
        # Go through self._switches, if it is on, add its index to on_indices
        for i in range(len(self._switches)):
            sw = self._switches[i]
            if(sw.is_on()):
                on_indices.append(i)
        
        return on_indices
    
    def flip(self, n):
        """(SwitchBoard, int) -> NoneType
        Flip the state of the switch at the index n.
        Raise NoSuchSwitchException if there is no switch at index n.
        Raise InvalidSwitchIndexException if n is negative
        
        >>> swbrd = SwitchBoard(10)
        >>> swbrd.flip(5)
        >>> swbrd.which_switch()
        [5]
        """
        # Raise InvalidSwitchIndexException if n is negative
        if (n < 0):
            raise InvalidSwitchIndexException
        
        # Try to access the switch at index n, if it fails raise an exception
        try:
            sw = self._switches[n]
        except IndexError:
            raise NoSuchSwitchException
        
        # Flip the switch
        sw.flip()
        
        return
    
    def flip_every(self, n):
        """(SwitchBoard, int) -> NoneType
        Flip the state of every nth switch, starting at 0.
        Raise InvalidSwitchIndexException if n is negative or is
        greater than the number of switches in self.
        
        >>> swbrd = SwitchBoard(10)
        >>> swbrd.flip_every(3)
        >>> swbrd.which_switch()
        [0, 3, 6, 9]
        """
        # If n is outside the acceptable range of indices, raise exception
        if not (n in range(len(self._switches))):
            raise InvalidSwitchIndexException
        
        # Go through a slice of self._switches that contains
        # every nth element starting from zero.
        # Since switches are mutable, the switches in the slice are the same
        # instances as the switches in the original self._switches
        # Call switch.flip() on each element in the slice
        for sw in self._switches[::n]:
            sw.flip()
        
        return
    
    def reset(self):
        """(SwitchBoard) -> NoneType
        Regardless of the state of the LightSwitches in self, change the state
        of all LightSwitches to off.
        
        >>> swbrd.which_switch()
        [0, 3, 6, 9]
        >>> swbrd.reset()
        >>> swbrd.which_switch()
        []
        """
        # Go through the list of switches and try to turn each one off
        for sw in self._switches:
            try:
                sw.turn_off()
            except InvalidSwitchException:
                # Don't need to do anything, it's already off
                pass
        
        return


if(__name__ == "__main__"):
    
    # number of switches in the problem
    NUM_SWITCHES = 1024
    
    # create a switchboard with the specified number of switches
    swbrd = SwitchBoard(NUM_SWITCHES)
    
    # peform each step, up to the max number of switches
    for n in range(1, NUM_SWITCHES):
        swbrd.flip_every(n)
        
        # for testing purposes:
        # print list of 1/0 to indicate which switches on/off
        ##print([int(sw.is_on()) for sw in swbrd._switches])
    
    # print the result
    print(swbrd)
