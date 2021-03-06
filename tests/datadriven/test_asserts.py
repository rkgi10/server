"""
Tests the datadriven assert methods
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest
import tests.datadriven as datadriven


class TestAsserts(unittest.TestCase):

    def setUp(self):
        self.testCase = datadriven.TestCase()

    def testAssertEqual(self):
        self.testCase.assertEqual(0, 0)
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertEqual(0, 1)

    def testAssertNotEqual(self):
        self.testCase.assertNotEqual(0, 1)
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertNotEqual(0, 0)

    def testAssertTrue(self):
        self.testCase.assertTrue(True)
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertTrue(False)

    def testAssertFalse(self):
        self.testCase.assertFalse(False)
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertFalse(True)

    def testAssertIs(self):
        a = object()
        b = object()
        self.testCase.assertIs(a, a)
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertIs(a, b)

    def testAssertIsNot(self):
        a = object()
        b = object()
        self.testCase.assertIsNot(a, b)
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertIsNot(a, a)

    def testAssertIsNone(self):
        self.testCase.assertIsNone(None)
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertIsNone(0)

    def testAssertIsNotNone(self):
        self.testCase.assertIsNotNone(0)
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertIsNotNone(None)

    def testAssertIn(self):
        self.testCase.assertIn(0, [0])
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertIn(0, [])

    def testAssertNotIn(self):
        self.testCase.assertNotIn(0, [])
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertNotIn(0, [0])

    def testAssertIsInstance(self):
        self.testCase.assertIsInstance(0, int)
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertIsInstance(0, str)

    def testAssertIsNotInstance(self):
        self.testCase.assertNotIsInstance(0, str)
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertNotIsInstance(0, int)

    def testAssertGreater(self):
        self.testCase.assertGreater(1, 0)
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertGreater(0, 0)
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertGreater(0, 1)

    def testAssertGreaterEqual(self):
        self.testCase.assertGreaterEqual(0, 0)
        self.testCase.assertGreaterEqual(1, 0)
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertGreaterEqual(0, 1)

    def testAssertLess(self):
        self.testCase.assertLess(0, 1)
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertLess(1, 0)
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertLess(0, 0)

    def testAssertLessEqual(self):
        self.testCase.assertLessEqual(0, 0)
        self.testCase.assertLessEqual(0, 1)
        with self.testCase.assertRaises(AssertionError):
            self.testCase.assertLessEqual(1, 0)

    def testAssertRaises(self):
        def func(*args, **kwargs):
            raise AssertionError()
        self.testCase.assertRaises(AssertionError, func, 1, a=2)
