"""Unit Tests for BraidWord"""
from braidgenerator.braidword import BraidWord
import unittest

class TestBraidWordInit(unittest.TestCase):
    def test_init_pathfail_0(self):
        '''
        Should raise TypeError if initword
        is not a list (args)
        '''
        with self.assertRaises(TypeError) as te:
            bw = BraidWord(1)

    def test_init_pathfail_1(self):
        '''
        Should raise ValueError if initword
        contains any zeros (args)
        '''
        with self.assertRaises(ValueError) as te:
            bw = BraidWord([0])

    def test_init_pathfail_0(self):
        '''
        Should raise TypeError if initword
        is not a list (kwargs)
        '''
        with self.assertRaises(TypeError) as te:
            bw = BraidWord(initword=1)

    def test_init_pathfail_1(self):
        '''
        Should raise ValueError if initword
        contains any zeros (kwargs)
        '''
        with self.assertRaises(ValueError) as te:
            bw = BraidWord(initword=[0])

    def test_init_success_0(self):
        '''
        Should successfully create BraidWord
        (args)
        '''
        bw = BraidWord([1, 2, 3])
        self.assertEqual(bw.word, [1, 2, 3])

    def test_init_success_0(self):
        '''
        Should successfully create BraidWord
        (kwargs)
        '''
        bw = BraidWord(initword=[1, 2, 3])
        self.assertEqual(bw.word, [1, 2, 3])


class TestBraidWordHelperMethods(unittest.TestCase):
    def test_canCancel_pathfail(self):
        """Should return False when adjacent
        generators are not inverses of one other"""
        bw = BraidWord([1, 2, 3, -3])
        # Execution path False
        self.assertFalse(bw.canCancel(0))

    def test_canCancel_pathsuccess(self):
        """Should return True when adjacent
        generators are inverses of one other"""
        bw = BraidWord([1, 2, 3, -3])
        # Execution path True
        self.assertTrue(bw.canCancel(2))

    def test_canTranspose_pathfail(self):
        """Should return False if adjacent
        generators have absolute distances <= 1"""
        bw = BraidWord([1, 2, 3, 5])
        # Execution path False
        self.assertFalse(bw.canTranspose(0))  # comparing 1 and 2

    def test_canTranspose_pathsuccess_0(self):
        """Should return True if adjacent generators
        have absolute distance > 1"""
        bw = BraidWord([1, 2, 3, 5])
        # Execution path True
        self.assertTrue(bw.canTranspose(2))  # comparing 3 and 5

    def test_canTranspose_pathsuccess_1(self):
        """Should return True if adjacent generators
        have absolute distance of absvals > 1"""
        bw = BraidWord([1, 2, -3, 5])
        # Execution path True
        self.assertTrue(bw.canTranspose(2))  # comparing -3 and 5

    def test_canFlip_pathfail_0(self):
        """Should return False if
        ~condP1:
        ( l[index] != l[(index+2) % len(l)] )
        and should not modify word.
        """
        bw = BraidWord([1, 2, 3])
        # Execution path False
        self.assertFalse(bw.canFlip(0))

    def test_canFlip_pathfail_1(self):
        """Should return False if
        ~condP2:
        abs(l[index] - l[(index+1) % len(l)]) != 1;
        and should not modify word.
        """
        bw = BraidWord([1, 3, 1])
        # Execution path False
        self.assertFalse(bw.canFlip(0))

    def test_canFlip_pathfail_2(self):
        """Should return False if
        ~condP2:
        abs(l[index] - l[(index+1) % len(l)]) != 1;
        i.e. l[index] < 0, l[(index+1) % len(l)]) > 0
        and should not modify word.
        """
        bw = BraidWord([-1, 2, -1])
        # Execution path False
        self.assertFalse(bw.canFlip(0))

    def test_canFlip_pathfail_3(self):
        """Should return False if
        ~condP2:
        abs(l[index] - l[(index+1) % len(l)]) != 1;
        i.e. l[index] > 0, l[(index+1) % len(l)]) < 0
        and should not modify word.
        """
        bw = BraidWord([1, -2, 1])
        # Execution path False
        self.assertFalse(bw.canFlip(0))

    def test_canFlip_pathsuccess_0(self):
        """Should return True when conditions met
        and testing only positive generators
        Refer to test_canFlip_pathfail_{0, 1}"""
        # Testing positive generators
        bw = BraidWord([1, 2, 1])
        # Execution path True
        self.assertTrue(bw.canFlip(0))

    def test_canFlip_pathsuccess_1(self):
        """Should return True when conditions met
        and testing for absolute values of generators"""
        # Testing negative generators
        bw = BraidWord([-1, -2, -1])
        # Execution path True
        self.assertTrue(bw.canFlip(0))

    def test_canDestabilize_pathfail_0(self):
        """Should return False if largestGenerator
        is not @end"""
        # largest generator not at end
        bw = BraidWord([1, 2, 5, 3])
        # Execution path False
        self.assertFalse(bw.canDestabilize())

    def test_canDestabilize_pathfail_1(self):
        """Should return False if more than one
        largestGenerator exists"""
        # More than one largest generator exists
        bw = BraidWord([1, 2, 3, 3])
        # Execution path False
        self.assertFalse(bw.canDestabilize())

    def test_canDestabilize_pathsuccess(self):
        """Should return True if only one largestGenerator
        and largestGenerator @end"""
        bw = BraidWord([1, 2, 3, 4])
        # Execution path True
        self.assertTrue(bw.canDestabilize())

class TestBraidWordMethods(unittest.TestCase):
    def test_conjugate(self):
        """Should conjugate word @ idx 2)"""
        bw = BraidWord([1, 2, 3, 4])
        # Execution path True
        self.assertTrue(bw.conjugate(2))
        # Word modification
        self.assertEqual(bw.word, [3, 4, 1, 2])

    def test_cancel_pathfail(self):
        """Should return False
        and fail to cancel gen @idx 1
        and not modify word"""
        bw = BraidWord([-1, 2, 3, 1])
        # Execution path False
        self.assertFalse(bw.cancel(1))
        # (No) Word modification
        self.assertEqual(bw.word, [-1, 2, 3, 1])

    def test_cancel_pathsuccess(self):
        """Should successfully cancel gen @idx 3
        and should modify word"""
        bw = BraidWord([-1, 2, 3, 1])
        # Execution path True
        self.assertTrue(bw.cancel(3))
        # Word modification
        self.assertEqual(bw.word, [2, 3])

    def test_insert_pathfail(self):
        """Should raise ValueError when given
        generator (5) > self.largestGenerator (4)
        and should not modify word."""
        bw = BraidWord([1, 2, 3, 4])
        with self.assertRaises(ValueError) as cm:
            bw.insert(2, 5)
        # (No) Word modification
        self.assertEqual(bw.word, [1, 2, 3, 4])

    def test_insert_pathsuccess(self):
        """Should successfully insert generator (3)
        @idx 2
        and should modify word
        and genCount."""
        bw = BraidWord([1, 2, 3, 4])
        # Execution path True
        self.assertTrue(bw.insert(2, 3))
        # Word modification
        self.assertEqual(bw.word, [1, 2, -3, 3, 3, 4])
        # genCount modification
        self.assertEqual(bw.genCount, [1, 1, 3, 1])

    def test_transpose_pathfail(self):
        """Should return False if two adjacent generators
        have absolute values differing by 1 or less
        and should not transpose word."""
        bw = BraidWord([1, 2, 3, -4])  # Checking absval with -4
        self.assertFalse(bw.transpose(2))
        # (No) Word modification
        self.assertEqual(bw.word, [1, 2, 3, -4])

    def test_transpose_pathsuccess(self):
        """Should return True if two adjacent generators
        have absolute values differing by more than 1
        and should successfully transpose word."""
        bw = BraidWord([1, 2, 3, 4])
        self.assertTrue(bw.transpose(3))  # Checking wrapping around with @idx 3
        # Word modification
        self.assertEqual(bw.word, [4, 2, 3, 1])

    def test_flip_pathfail_0(self):
        """Should return False if
        ~condP1:
        ( l[index] != l[(index+2) % len(l)] )
        and should not modify word.
        """
        bw = BraidWord([1, 2, 3])
        # NOTE condP2 holds (refer to test_flip_pathfail_1)
        self.assertFalse(bw.flip(0))
        # (No) Word modification
        self.assertEqual(bw.word, [1, 2, 3])
        # (No) genCount modification
        self.assertEqual(bw.genCount, [1, 1, 1])

    def test_flip_pathfail_1(self):
        """Should return False if
        ~condP2:
        abs(l[index] - l[(index+1) % len(l)]) != 1
        and should not modify word.
        """
        bw = BraidWord([1, 3, 1])
        # NOTE condP1 holds (refer to test_flip_pathfail_0)
        self.assertFalse(bw.flip(0))
        # (No) Word modification
        self.assertEqual(bw.word, [1, 3, 1])
        # (No) genCount modification
        self.assertEqual(bw.genCount, [2, 0, 1])

    def test_flip_pathfail_2(self):
        """Should return False if
        ~condP2:
        abs(l[index] - l[(index+1) % len(l)]) != 1;
        i.e. l[index] < 0, l[(index+1) % len(l)]) > 0
        and should not modify word.
        """
        bw = BraidWord([-1, 2, -1])
        # NOTE condP1 holds (refer to test_flip_pathfail_0)
        self.assertFalse(bw.flip(0))
        # (No) Word modification
        self.assertEqual(bw.word, [-1, 2, -1])
        # (No) genCount modification
        self.assertEqual(bw.genCount, [2, 1])

    def test_flip_pathfail_3(self):
        """Should return False if
        ~condP2:
        abs(l[index] - l[(index+1) % len(l)]) != 1;
        i.e. l[index] > 0, l[(index+1) % len(l)]) < 0
        and should not modify word.
        """
        bw = BraidWord([1, -2, 1])
        # NOTE condP1 holds (refer to test_flip_pathfail_0)
        self.assertFalse(bw.flip(0))
        # (No) Word modification
        self.assertEqual(bw.word, [1, -2, 1])
        # (No) genCount modification
        self.assertEqual(bw.genCount, [2, 1])

    def test_flip_pathsuccess(self):
        """
        Should return True if condP1 and condP2
        and successfully flip word.
        """
        bw_0 = BraidWord([1, 2, 1])
        bw_1 = BraidWord([1, 1, 2])  # Check wrapping around
        bw_2 = BraidWord([-1, -2, -1])
        self.assertTrue(bw_0.flip(0))
        self.assertTrue(bw_1.flip(1))
        self.assertTrue(bw_2.flip(0))

        # Word modifications
        self.assertEqual(bw_0.word, [2, 1, 2])
        self.assertEqual(bw_1.word, [2, 2, 1])
        self.assertEqual(bw_2.word, [-2, -1, -2])

        # genCount modifications
        self.assertEqual(bw_0.genCount, [1, 2])
        self.assertEqual(bw_1.genCount, [1, 2])
        self.assertEqual(bw_2.genCount, [1, 2])

    def test_stabilize(self):
        """Should stabilize the word and genCount."""
        bw = BraidWord([1, 2, 3])
        self.assertTrue(bw.stabilize())
        # Word modification
        self.assertEqual(bw.word, [1, 2, 3, 4])
        # genCount modification
        self.assertEqual(bw.genCount, [1, 1, 1, 1])

    def destabilize_pathfail(self):
        """Should return False if
        Cond1:
        more than one largestGenerator exist
        and should not modify word or genCount"""
        bw = BraidWord([1, 2, 3, 3])
        self.assertFalse(bw.destabilize())
        # (No) Word modification
        self.assertEqual(bw.word, [1, 2, 3, 3])
        # (No) genCount modification
        self.assertEqual(bw.genCount, [1, 1, 2])

    def destabilize_pathfail(self):
        """Should return False if
        Cond2:
        one largestGenerator exists but not at end
        and should not modify word or genCount"""
        bw = BraidWord([1, 2, 3])
        self.assertFalse(bw.destabilize())
        # (No) Word modification
        self.assertEqual(bw.word, [1, 2, 3])
        # (No) genCount modification
        self.assertEqual(bw.genCount, [1, 1, 1])

    def destabilize_pathsuccess(self):
        """Should return True if
        Cond1 and Cond2 are satisfied
        and should modifiy word and genCount"""
        bw = BraidWord([[-1, 2, 3]])  # Check absval of genCount with -1
        self.assertTrue(bw.destabilize())
        # Word modifications
        self.assertEqual(bw.word, [-1, 2])
        # genCount modification
        self.assertEqual(bw.genCount, [1, 1])


if __name__ == '__main__':
    unittest.main()
