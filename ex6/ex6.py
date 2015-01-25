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

        return repr(self.data)


class DoublyLinkedList(object):
    """A doubly linked list"""
    
    def __init__(self):
        '''(DoublyLinkedList) -> NoneType
        Create a new empty DoublyLinkedList
        '''
        self._head = None
        
        return

    def __str__(self):
        '''(DoublyLinkedList) -> str
        
        Return a str representation of the contents of this
        DoublyLinkedList.
        '''
        # List to store strings of each node
        node_strs = []
        
        # Go through each node, append its string to node_strs
        curr = self._head
        while(curr is not None):
            node_strs.append(str(curr))
            # Advance to next node
            curr = curr.next_link
        
        # Put commas between each node string and format the string nicely
        return "DoublyLinkedList: [{}]".format(', '.join(node_strs))
    
    def __len__(self):
        """(DoublyLinkedList) -> int
        Return the number of nodes in this DoublyLinkedList
        """
        # Use recursive helper method
        return self._len_rec(self._head)

    def _len_rec(self, head):
        """(DoublyLinkedList, DLLNode) -> int
        Use recursion to return the number of nodes in the linked list
        starting at head
        """
        # Base Case:
        if(head is None):
            return 0
        
        # Recursive Decompostion:
        else:
            return (1 + self._len_rec(head.next_link))

    def _check_index(self, index):
        """(DoublyLinkedLIst, int) -> NoneType
        Raise IndexError if index is not a valid index for self
        """
        if(index < 0) or (index > len(self)):
            raise IndexError
        return
    
    def _link_nodes(self, curr_node, next_node):
        """(DoublyLinkedList, DLLNode, DLLNode) -> NoneType
        Link curr_node to next_node.
        """
        # Link curr_node to next_node
        curr_node.next_link = next_node
        
        # Only need to link next_node back to curr_node if it exists
        if(next_node is not None):
            next_node.prev_link = curr_node
        
        return
    
    def _add_rec(self, add_node, head, index):
        """(DoublyLinkedList, DLLNode, DLLNode, int) -> DLLNode
        Use recursion to insert add_node as a node at the specified index
        of the DLLNode linked list starting at head.
        Return the head of the modified DLLNode linked list.
        """
        
        # Base Case: if the linked list is empty, return add_node as the head
        if(head is None):
            return add_node
        
        # Base Case: if the index is 0, link add_node to the head,
        # and return add_node as the head
        elif(index == 0):
            self._link_nodes(add_node, head)
            return add_node
        
        # Recursive Decomposition: n-1 approach
        # If index is not 0
        else:
            # Make a recursive call with an index one lower, 
            # and a list one node shorter
            result = self._add_rec(add_node, head.next_link, (index - 1))
            
            # If the result is not linked to the current head,
            # link the current head to the result
            if ((not (result.prev_link is head)) or
                    (not (head.next_link is result))):
                self._link_nodes(head, result)
            
            return head
    
    def add_head(self, add_obj):
        '''(DoublyLinkedList, object) -> NoneType
        Add add_obj to the head of this DoublyLinkedList.
        '''
        # Create a DLLNode for add_obj
        add_node = DLLNode(add_obj)
        
        # Set head to the result of inserting add_node at index 0
        self._head = self._add_rec(add_node, self._head, 0)
        
        return
    
    def add_tail(self, add_obj):
        '''(DoublyLinkedList, object) -> NoneType
        Add add_obj to the tail of this DoublyLinkedList.
        '''
        # Create a DLLNode for add_obj
        add_node = DLLNode(add_obj)
        
        # Set head to the result of inserting add_node at the last index
        self._head = self._add_rec(add_node, self._head, len(self))
        
        return
    
    def add_index(self, add_obj, add_index):
        '''(DoublyLinkedList, object, int) -> NoneType
        Add add_obj to this DoublyLinkedList at index add_index.
        
        If add_index is not a valid index for this DoublyLinkedList, 
        IndexError will be raised.
        '''
        # Check if index is valid
        self._check_index(add_index)
        
        # Create a DLLNode for add_obj
        add_node = DLLNode(add_obj)
        
        # Set head to the result of inserting add_node add_index
        self._head = self._add_rec(add_node, self._head, add_index)
        
        return
    
    def _unlink_nodes(self, curr_node):
        """(DoublyLinkedList, DLLNode, DLLNode) -> DLLNode
        Unlink curr_node from its next node, and return the next node
        """
        # Remember the next node
        next_node = curr_node.next_link
        
        # Only need to unlink if next_node exists
        if(next_node is not None):
            curr_node.next_link = None
            next_node.prev_link = None
        
        return next_node

    def _remove_rec(self, head, index):
        """(DoublyLinkedList, DLLNode, int) -> tuple of (DLLNode, DLLNode)
        Use recursion to remove the node at the specified index
        of the DLLNode linked list starting at head.
        Return the head of the modified DLLNode linked list, and the node
        that was removed
        (new_head, removed_node)
        """
        
        # Base Case: if the linked list is empty, return none
        if(head is None):
            return (None, None)
        
        # Base Case: if the index is 0, unlink head from the next node in 
        # the linked list.
        # Return the new head, and the current head as the removed node
        elif(index == 0):
            new_head = self._unlink_nodes(head)
            return (new_head, head)
        
        # Recursive Decomposition: n-1 approach
        # If index is not 0
        else:
            # Make a recursive call with an index one lower, 
            # and a list one node shorter
            (new_head, removed_node) = \
                self._remove_rec(head.next_link, (index - 1))
            
            # If the new head does not exist,
            # or is not linked to the current head,
            # link the current head to the new head
            if((new_head is None) or
               (not (new_head.prev_link is head)) or
               (not (head.next_link is new_head))):
                
                self._link_nodes(head, new_head)
            
            return (head, removed_node)
    
    def remove_head(self):
        '''(DoublyLinkedList) -> object
        Remove and return the first item in this DoublyLinkedList.
        
        If the DoublyLinkedList is empty return None
        '''
        # Set head to the result of removing the node at index 0
        (self._head, removed_node) = self._remove_rec(self._head, 0)
        
        return removed_node.data
        
    def remove_tail(self):
        '''(DoublyLinkedList) -> object
        Remove and return the last item in this DoublyLinkedList.
        
        If the DoublyLinkedList is empty return None
        '''
        # Set head to the result of removing the node at the index
        # of the last node
        (self._head, removed_node) = \
            self._remove_rec(self._head, (len(self) - 1))
        
        return removed_node.data

    def remove_index(self, remove_index):
        '''(DoublyLinkedList, int) -> object
        Remove and return the item at index remove_index in this
        DoublyLinkedList.
        
        If the DoublyLinkedList is empty return None
        
        If add_index is not a valid index for this DoublyLinkedList, 
        IndexError will be raised.
        '''
        # Check if index is valid
        self._check_index(remove_index)
        
        # Set head to the result of removing the node at remove_index
        (self._head, removed_node) = \
            self._remove_rec(self._head, remove_index)
        
        return removed_node.data


if(__name__ == "__main__"):
    l = DoublyLinkedList()
    print('l is a', l)
    
    while(1):
        output = eval(input('>>> '))
        print(output if (output is not None) else '')
        print(l)
