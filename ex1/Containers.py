# Classes that implement Queues, Stacks, and Buckets using
# Python's collections.deque
# This module is used by LetterMatchingGame
# Written by Xiuqi (Rex) Xia

from collections import deque


class Queue(deque):
    """An extention of collections.deque representing a FIFO queue.
    The first element is on the left (index 0),
    The last element is on the right (index -1)
    """
    
    def put(self, element):
        """Add an element to the Queue (at the last position),
        """
        self.append(element)
    
    def unput(self):
        """Remove and return the last element of the Queue,
        Raise an IndexError if the Queue is already empty
        """
        return self.pop()
    
    def get(self):
        """Remove and return the first element in the Queue,
        Raise an IndexError if the Queue is already empty
        """
        return self.popleft()
    
    def unget(self, element):
        """Add an element to the Queue (at the first position),
        """
        self.appendleft(element)
    

class Stack(deque):
    """An extention of collections.deque representing a LIFO stack.
    The first element is on the left (index 0)
    The last element is on the right (index -1)
    """
    
    def put(self, element):
        """Add an element to the Stack (at the last position),
        """
        self.append(element)
    
    def unput(self):
        """Remove and return the last element of the Stack,
        Raise an IndexError if the Stack is already empty
        """
        # In a stack, unput is the same as get
        return self.get()
    
    def get(self):
        """Remove and return the last element in the Stack,
        Raise an IndexError if the Stack is already empty
        """
        return self.pop()
    
    def unget(self, element):
        """Add an element to the Stack (at the last position),
        """
        # In a stack, unget is the same as put
        self.put(element)


class Bucket(Stack):
    """A one-element Queue/Stack.
    IndexError will be raised if an element is put() or unget() when the 
    Bucket already has an element (is full).
    """
    
    def __init__(self, element=[]):
        """(Bucket, [list]) -> NoneType
        
        Initialize a bucket with the element.
        If element is not provided, the Bucket will be empty.
        If element is a list with more than one element, IndexError will
        be raised
        """
        if(len(element) > 1):
            raise IndexError
        
        # Use the constructor for Queue, with a maxlen of 1
        Stack.__init__(self, list(element), 1)
    
    def put(self, element):
        """Add an element to the Bucket,
        Raise an IndexError if Bucket is already full
        """
        if(len(self) >= 1):
            raise IndexError
        self.append(element)


if(__name__ == '__main__'):
    pass
    # Code for testing