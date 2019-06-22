"""Unit Tests for MarkovChain"""
from braidgenerator.markovchain import MarkovChain
from braidgenerator.braidword import BraidWord
import pandas as pd
import unittest

class TestMarkovChainMethods(unittest.TestCase):
    def test_aggregate(self):
        '''
        Should return non-empty self.braidagg
        '''
        mc = MarkovChain(BraidWord([1, 2, 3]))
        mc.model(num_braidreps=1, msteps=10)
        # Check if non-empty
        self.assertTrue(mc.aggregate())

    def test_logs(self):
        '''
        Should return non-empty self.braidagg.logs
        '''
        mc = MarkovChain(BraidWord([1, 2, 3]))
        mc.model(num_braidreps=1, msteps=10)
        # Check if non-empty
        self.assertTrue(mc.logs())

    def test_braidreps_0(self):
        '''
        Should return non-empty self.braidagg.braidreps
        in BraidWord form
        '''
        mc = MarkovChain(BraidWord([1, 2, 3]))
        mc.model(num_braidreps=1, msteps=10)
        isos = mc.braidreps(as_word=False)
        # Check if non-empty
        self.assertTrue(isos)
        # Check types
        self.assertIsInstance(isos[0], BraidWord)

    def test_braidreps_1(self):
        '''
        Should return non-empty self.braidagg.braidreps
        in word form
        '''
        mc = MarkovChain(BraidWord([1, 2, 3]))
        mc.model(num_braidreps=1, msteps=10)
        isos = mc.braidreps(as_word=True)
        # Check if non-empty
        self.assertTrue(isos)
        # Check types
        self.assertIsInstance(isos[0], list)

    def test_topandas_0(self):
        '''
        Should return non-empty pandas df
        of logs and braidreps in word form
        only_braidreps=False
        '''
        mc = MarkovChain(BraidWord([1, 2, 3]))
        mc.model(num_braidreps=1, msteps=10)
        df = mc.topandas(only_braidreps=False)
        # Check df columns
        self.assertTrue(df.shape[1] == 2)
        self.assertTrue(list(df.columns) == ['braidreps', 'Logs'])
        # Check if non-empty
        self.assertFalse(df['braidreps'].empty)
        self.assertFalse(df['Logs'].empty)
        # Check types of braidreps
        self.assertIsInstance(df['braidreps'][0], list)

    def test_topandas_1(self):
        '''
        Should return non-empty pandas df
        of only BraidWords in word form
        only_braidreps=True
        '''
        mc = MarkovChain(BraidWord([1, 2, 3]))
        mc.model(num_braidreps=1, msteps=10)
        df = mc.topandas(only_braidreps=True)
        # Check df columns
        self.assertTrue(df.shape[1] == 1)
        self.assertTrue(list(df.columns) == ['braidreps'])
        # Check if non-empty
        self.assertFalse(df['braidreps'].empty)
        # Check types of braidreps
        self.assertIsInstance(df['braidreps'][0], list)

    def test_clear_model(self):
        '''
        Should clear the model leaving
        self.braid_agg's components empty
        '''
        mc = MarkovChain(BraidWord([1, 2, 3]))
        mc.model(num_braidreps=1, msteps=10)
        mc.clear_model()
        # Check if empty
        self.assertFalse(mc.braidagg['braidreps'])
        self.assertFalse(mc.braidagg['logs'])

class TestMarkovChainInit(unittest.TestCase):
    def test_init_pathfail_0(self):
        """Should throw error if BraidWord not given"""
        with self.assertRaises(Exception) as te:
            MarkovChain()

    def test_init_pathfail_1(self):
        '''
        Should throw error if number of arguments
        is greater than three
        (args)
        '''
        with self.assertRaises(Exception) as ex:
            MarkovChain(BraidWord([1, 2, 3]), 0, 0, 0)

    def test_init_pathfail_2(self):
        """
        Should throw error if argument maxgen
        is negative
        (args)
        """
        with self.assertRaises(ValueError) as ve:
            MarkovChain(BraidWord([1, 2, 3]), -1, 1)

    def test_init_pathfail_3(self):
        """
        Should throw error if argument maxLen
        is negative
        (args)
        """
        with self.assertRaises(ValueError) as ve:
            MarkovChain(BraidWord([1, 2, 3]), 1, -1)

    def test_init_pathfail_4(self):
        """
        Should throw error if keyword argument
        maxgen is negative
        (kwargs)
        """
        with self.assertRaises(ValueError) as ve:
            MarkovChain(braidword=BraidWord([1, 2, 3]), maxgen=-1, maxlen=1)

    def test_init_pathfail_5(self):
        """
        Should throw error if keyword argument
        maxlen is negative
        (kwargs)
        """
        with self.assertRaises(ValueError) as ve:
            MarkovChain(braidword=BraidWord([1, 2, 3]), maxgen=1, maxlen=-1)

    def test_init_pathsuccess_0(self):
        """
        Should create MarkovChain if all arguments are valid
        (args)
        """
        bw = MarkovChain(BraidWord([1, 2, 3]), 1, 1)
        # Check types
        self.assertEqual(type(bw.braid), BraidWord)
        # Check words
        self.assertEqual(bw.braid.word, BraidWord([1, 2, 3]).word)
        self.assertEqual(bw.maxgen, 1)
        self.assertEqual(bw.maxlen, 1)

    def test_init_pathsuccess_1(self):
        """
        Should create MarkovChain if all keyword arguments are valid
        (kwargs)
        """
        bw = MarkovChain(braidword=BraidWord([1, 2, 3]), maxgen=1, maxlen=1)
        # Check types
        self.assertEqual(type(bw.braid), BraidWord)
        # Check words
        self.assertEqual(bw.braid.word, BraidWord([1, 2, 3]).word)
        self.assertEqual(bw.maxgen, 1)
        self.assertEqual(bw.maxlen, 1)

    def test_init_pathsuccess_2(self):
        """
        Should create MarkovChain with only BraidWord argument given
        (kwargs)
        """
        bw = MarkovChain(braidword=BraidWord([1, 2, 3]))
        # Check types
        self.assertEqual(type(bw.braid), BraidWord)
        # Check words
        self.assertEqual(bw.braid.word, BraidWord([1, 2, 3]).word)

    def test_init_pathsuccess_3(self):
        """
        Should create MarkovChain with only list argument given
        (args)
        """
        bw = MarkovChain([1, 2, 3])
        # Check types
        self.assertEqual(type(bw.braid), BraidWord)
        # Check words
        self.assertEqual(bw.braid.word, BraidWord([1, 2, 3]).word)

    def test_init_pathsuccess_4(self):
        """
        Should create MarkovChain with only list argument given
        (kwargs)
        """
        bw = MarkovChain(braidword=[1, 2, 3])
        # Check types
        self.assertEqual(type(bw.braid), BraidWord)
        # Check words
        self.assertEqual(bw.braid.word, BraidWord([1, 2, 3]).word)


if __name__ == '__main__':
    unittest.main()

    # mc = MarkovChain(BraidWord([1, 2, 3]))
    # mc.model(10)

    # z = mc.topandas()
    # t = mc.topandas(only_braidreps=True)

    # Should export braidreps and logs
    # mc.tocsv()

    # # Should export both
    # mc.tocsv("both.csv")

    # # Should only export braidreps
    # mc.tocsv(only_braidreps=True)

    # # Should export braidreps and logs
    # mc.totxt()

    # # Should export braidreps and logs to a.txt
    # mc.totxt('a.txt')

    # # Should only export braidreps
    # mc.totxt(only_braidreps=True)

    # # Should only export braidreps to b.txt
    # mc.totxt('b.txt', only_braidreps=True)

    # Should export both to path given
    # mc.totxt('/Users/miladnasrollahi/Desktop/f.txt')
