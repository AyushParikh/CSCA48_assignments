class BTNode(object):
    """A node in a binary tree."""

    def __init__(self, value, left=None, right=None):
        """(BTNode, int, BTNode, BTNode) -> NoneType
        Initialize this node to store value and have children left and right,
        as well as depth 0.
        """
        self.value = value
        self.left = left
        self.right = right
        self.depth = 0  # the depth of this node in a tree

    def __str__(self):
        return self._str_helper("")

    def _str_helper(self,indentation = "", arrow = ''):
        """(BTNode, str) -> str
        Return a "sideways" representation of the subtree rooted at this node,
        with right subtrees above parents above left subtrees and each node on
        its own line, preceded by as many TAB characters as the node's depth.
        """
        ret = ""

        if(self.right != None):
            ret += self.right._str_helper(indentation + "\t", '/- ')
        ret += (indentation + arrow + str(self.value) +
                ',' + str(self.depth) + "\n")
        if(self.left != None):
            ret += self.left._str_helper(indentation + "\t", '\\- ')
        return ret
    # --- End of starter code ---

    def set_depth(self, curr_depth):
        """(BTNode, int) -> NoneType
        Recursively set the depth of all the nodes in the tree rooted at self.
        The depth values start at curr_depth at the root (self), and the depth
        of each subsequent level of child nodes increases by one.
        """
        # Set self's depth to curr_depth
        self.depth = curr_depth

        ## Testing
        #print(self.value, self.depth)

        # For each child that exists, set it's depth to curr_depth + 1
        for child in (self.left, self.right):
            if(child is not None):
                child.set_depth(curr_depth + 1)

        return

    def leaves_and_internals(self):
        """(BTNode, int) -> tuple of (set, set)
        Return a tuple containing:
        0: A set of the values of all leaf nodes in the tree rooted at self
        1: A set of the values of all internal nodes in the tree
           rooted at self
        Note that the root (self) does not count as an internal node
        """
        # Use helper method
        (leaves, internals) = self._leaves_and_internals_helper()

        # Remove the value of self from internals
        try:
            internals.remove(self.value)
        except KeyError:
            # The value of self was not in internals anyway, so do nothing
            pass

        return (leaves, internals)

    def _leaves_and_internals_helper(self):
        """(BTNode, int) -> tuple of (set, set)
        Return a tuple containing:
        0: A set of the values of all leaf nodes in the tree rooted at self
        1: A set of the values of all internal nodes in the tree
           rooted at self
        Note that for the purposes of this method, a root can be an internal
        node
        """
        # Sets to return
        leaves = set()
        internals = set()

        # Base case: self is a leaf node
        if((self.left is None) and (self.right is None)):
            # leaves contain only self's value
            leaves.add(self.value)
            # internals is an empty set
            return (leaves, internals)

        # Recursive decomposition:
        # Self is an internal node
        else:
            # For each child that exists,
            # add its leaves, internals to the sets
            for child in (self.left, self.right):
                if(child is not None):
                    (child_leaves, child_internals) = \
                        child._leaves_and_internals_helper()
                    leaves.update(child_leaves)
                    internals.update(child_internals)

            # Add self's value to the internals set
            internals.add(self.value)

            return (leaves, internals)

    def sum_to_deepest(self):
        """(BTNode) -> int
        Return the sum of the values of the deepest path in the tree rooted at
        self. Ties are broken in favour of the path with the greater sum.
        """
        # Set the depth of all the nodes, starting from zero
        self.set_depth(0)

        # Use helper function
        (depth, path_sum) = self._sum_to_deepest_rec()
        return path_sum

    def _sum_to_deepest_rec(self):
        """(BTNode) -> tuple of (int, int)
        Return the depth of the deepest path in the tree rooted at
        self, as well as the sum of its value. Ties are broken in
        favour of the path with the greater sum.

        Return format: (max_depth, path_sum)

        REQ: the depths of all the node in the tree rooted at self must have
        been set correctly
        """
        # Base case: If self is a leaf node,
        # it is the deepest node in the path, so return its depth and value
        if((self.left is None) and (self.right is None)):
            return (self.depth, self.value)

        # Recursive decomposition:
        # self is an internal node
        else:
            # list of (max_depth, path_sum)
            depth_sum_list = []

            # Get and append to list the deepest sum of each existent child
            for child in (self.left, self.right):
                if(child is not None):
                    depth_sum_list.append(child._sum_to_deepest_rec())

            ## testing
            #print(depth_sum_list)

            # Get the path sum of the deepest child path
            # Using tuple comparison:
            # the max_depth (0th element) gets compared first,
            # ties are broken with the path sum (1th element)
            (max_depth, path_sum) = max(depth_sum_list)

            ## testing
            #print((max_depth, path_sum))

            # Add self's value to the value of path_sum, and return
            return (max_depth, path_sum + self.value)


if(__name__ == "__main__"):
    #just a simple tree to practice on
    my_tree = BTNode(10, BTNode(3, BTNode(5), BTNode(2,
                     BTNode(8, BTNode(11), BTNode(13)))),
                     BTNode(7, BTNode(4, BTNode(9)), BTNode(6, BTNode(12))))
    my_tree.set_depth(0)
    print(my_tree)

    (leaves, internals) = my_tree.leaves_and_internals()
    print("leaves:", leaves, (leaves == {12, 9, 13, 11, 5}))
    print("internals:", internals, (internals == {7, 6, 4, 3, 2, 8}))

    deepest_sum = my_tree.sum_to_deepest()
    print("sum to deepest:", deepest_sum,
          (deepest_sum == sum((10, 3, 2, 8, 13))))

    BTNode(10).leaves_and_internals()
