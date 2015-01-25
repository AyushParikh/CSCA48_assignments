import unittest
from ex9_code import *


class TestEx9(unittest.TestCase):

    def test_init(self):
        h = Heap([1, 2, 3, 4, 5])
        self.assertEqual(h._heap, [5, 4, 2, 1, 3],
                         "Heap.__init__ does not add the elements in "
                         "insert_list to the heap correctly.")

    def test_empty_heap_is_empty(self):
        empty_h = Heap([])
        self.assertIsInstance(empty_h.is_empty(), bool)
        self.assertTrue(empty_h.is_empty(),
                        "Heap.is_empty incorrectly reports that an empty "
                        "Heap is not empty.")

    def test_non_empty_heap_is_not_empty(self):
        non_empty_h = Heap([1])
        self.assertIsInstance(non_empty_h.is_empty(), bool)
        self.assertFalse(non_empty_h.is_empty(),
                         "Heap.is_empty incorrectly reports that a non-empty "
                         "Heap is empty.")

    def test_insert_when_empty(self):
        h = Heap([])
        h.insert(1)
        self.assertEqual(h._heap, [1],
                         "Heap.insert does not correctly insert a value "
                         "into an empty heap.")

    def test_insert_small_val_when_non_empty(self):
        h = Heap([])
        h._heap = [5, 4, 2, 1, 3]
        h.insert(-1)
        self.assertEqual(h._heap, [5, 4, 2, 1, 3, -1],
                         "Heap.insert does not correctly insert a small "
                         "value into a non-empty heap.")

    def test_insert_large_val_when_non_empty(self):
        h = Heap([])
        h._heap = [5, 4, 2, 1, 3]
        h.insert(10)
        self.assertEqual(h._heap, [10, 4, 5, 1, 3, 2],
                         "Heap.insert does not correctly insert a large "
                         "value into a non-empty heap.")

    def test_bubble_up_no_violation(self):
        h = Heap([])
        h._heap = [5, 4, 2, 1, 3]
        h._bubble_up(4)

        self.assertEqual(h._heap, [5, 4, 2, 1, 3],
                         "Heap._bubble_up incorrectly modified the heap even "
                         "when no change was required.")

    def test_bubble_up_one_level(self):
        h = Heap([])
        h._heap = [10, 1, 2, 3]
        h._bubble_up(3)

        self.assertEqual(h._heap, [10, 3, 2, 1],
                         "Heap._bubble_up did not correctly bubble up an "
                         "element that violated the heap property.")

    def test_bubble_up_to_top(self):
        h = Heap([])
        h._heap = [3, 1, 2, 10]
        h._bubble_up(3)

        self.assertEqual(h._heap, [10, 3, 2, 1],
                         "Heap._bubble_up did not correctly bubble up the "
                         "largest element all the way to the top of the heap.")

    def test_remove_top_empty_heap(self):
        h = Heap([])
        self.assertRaises(HeapEmptyException, h.remove_top)

    def test_remove_top_last_value(self):
        h = Heap([1])
        self.assertEqual(h.remove_top(), 1,
                         "Heap.remove_top does not return the correct "
                         "element when there is only one element in the heap")
        self.assertEqual(h._heap, [],
                         "Heap.remove_top does not remove the last element "
                         "in the heap")

    def test_remove_top_non_empty_heap(self):
        h = Heap([])
        h._heap = [30, 20, 10, 4, 3, 2, 5, 1]
        self.assertEqual(h.remove_top(), 30,
                         "Heap.remove_top does not return the correct "
                         "element.")
        self.assertEqual(h._heap, [20, 4, 10, 1, 3, 2, 5],
                         "After removing the top element, Heap.remove_top "
                         "does not maintain the heap property.")

    def test_violates_no_violation(self):
        h = Heap([])
        h._heap = [5, 4, 2, 1, 3]

        self.assertFalse(h._violates(0),
                         "Heap._violates incorrectly reported a violation "
                         "of the heap property when there was no violation.")

    def test_violates_with_violation(self):
        h = Heap([])
        h._heap = [4, 5, 2, 1, 3]

        self.assertTrue(h._violates(0),
                        "Heap._violates incorrectly reported no violation "
                        "of the heap property when there was a violation.")

    def test_violates_no_children(self):
        h = Heap([])
        h._heap = [5, 4, 2, 1, 3]

        self.assertFalse(h._violates(4),
                         "Heap._violates incorrectly reported a violation "
                         "of the heap property when the element does not "
                         "have any children.")

    def test_bubble_down_no_violation(self):
        h = Heap([])
        h._heap = [5, 4, 2, 1, 3]
        h._bubble_down(0)

        self.assertEqual(h._heap, [5, 4, 2, 1, 3],
                         "Heap._bubble_down incorrectly modified the heap "
                         "even when no change was required.")

    def test_bubble_down_one_level(self):
        h = Heap([])
        h._heap = [3, 10, 2, 1]
        h._bubble_down(0)

        self.assertEqual(h._heap, [10, 3, 2, 1],
                         "Heap._bubble_up did not correctly bubble down an "
                         "element that violated the heap property.")

    def test_bubble_down_to_bottom(self):
        h = Heap([])
        h._heap = [1, 10, 2, 3]
        h._bubble_down(0)

        self.assertEqual(h._heap, [10, 3, 2, 1],
                         "Heap._bubble_up did not correctly bubble down the "
                         "smallest element all the way to the bottom of the "
                         "heap.")


if(__name__ == "__main__"):
    unittest.main(exit=False)
