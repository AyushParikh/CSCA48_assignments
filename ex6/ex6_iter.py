class DLLNode(object):
    """A Node in a doubly-linked list"""
    
    def __init__(self, data, prev_link=None, next_link=None):
        '''(DLLNode, object, DLLNode, DLLNode) -> NoneType

        Create a new DLLNode containing object, with previous node
        prev_link, and next node next_link.
        '''
        
        self.data = data
        self.prev_link = prev_link
        self.next_link = next_link
    
    def __str__(self):
        '''(DLLNode) -> str
        Return a str representation of this DLLNode.
        '''

        return str(self.data)
    
class DoublyLinkedList(object):
    """A doubly linked list"""
    
    def __init__(self):
        '''(DoublyLinkedList) -> NoneType
        Create a new empty DoublyLinkedList
        '''
        self._head = None
        return
    
    def __iter__(self):
        """(DoublyLinkedList) -> iterable
        Return an iterable over this DoublyLinkedList
        """
        return self._iter_gen()
    
    def _iter_gen(self):
        """(DoublyLinkedList) -> obj
        Generator for an iterable over this DoublyLinkedList
        """
        # Start iteration at the head
        curr = self._head
        
        # In each iteration until the end of the DLL is reached
        while(curr != None):
            # Return the current node
            yield curr
            # Advance to the next node
            curr = curr.next_link
        
        # if the end of the DLL is reached, stop the iteration
        raise StopIteration
        
    def __str__(self):
        '''(DoublyLinkedList) -> str
        
        Return a str representation of the contents of this
        DoublyLinkedList.
        '''
        # List to store the str representations of each of the nodes
        node_strs = [str(node) for node in self]
        
        # Format the str like this: '[node, node, node, ... ]'
        return '[{}]'.format(', '.join(node_strs))
    
    def add_head(self, add_obj):
        '''(DoublyLinkedList, object) -> NoneType
        Add add_obj to the head of this DoublyLinkedList.
        '''
        # Create new node for the obj to be added
        new_node = DLLNode(add_obj)
        
        # If DLL is not empty
        if(self._head != None):
            # link new_node to the head
            new_node.next_link = self._head
            self._head.prev_link = new_node
            
        # set new_node to be the new head
        self._head = new_node
        return
    
    def add_tail(self, add_obj):
        '''(DoublyLinkedList, object) -> NoneType
        Add add_obj to the tail of this DoublyLinkedList.
        '''
        
        pass
    
    def add_index(self, add_obj, add_index):
        '''(DoublyLinkedList, object, int) -> NoneType
        Add add_obj to this DoublyLinkedList at index add_index.
        '''

        pass
    
    def remove_head(self):
        '''(DoublyLinkedList) -> object
        Remove and return the first item in this DoublyLinkedList.
        '''
        
        pass
        
    def remove_tail(self):
        '''(DoublyLinkedList) -> object
        Remove and return the last item in this DoublyLinkedList.
        '''

        pass

    def remove_index(self, remove_index):
        '''(DoublyLinkedList, int) -> object
        
        Remove and return the item at index remove_index in this
        DoublyLinkedList.
        '''

        pass
