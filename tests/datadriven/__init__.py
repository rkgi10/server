"""
Data-driven tests for the GA4GH reference implementation. A data
driven test applies a given test method to a data file, and
each applicaton is an independent test case under nose.
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import contextlib
import os
import inspect


def _wrapTestMethod(method):
    """
    Takes an instance method of a DataDrivenTest subclass, and returns a
    function that can be used in a test generator in nose. This entails
    updating the description attribute so that we can see details of
    the tests being run in nose.
    """
    instance = method.im_self
    cls = instance.__class__

    def testFunction():
        method()
    testFunction.description = "{}.{}.{}:{}".format(
        method.__module__, cls.__name__, method.__name__,
        instance.getSetId())
    return testFunction


def makeTests(testDataDir, testClass):
    """
    Top-level entry point for data driven tests. For every subdirectory
    in testDataDir, create an instance of testClass and then yield
    each of its testMethods in a format suitable for use with nose
    test generators.
    """
    for testSetId in os.listdir(testDataDir):
        tester = testClass(testSetId, testDataDir)
        for name, _ in inspect.getmembers(testClass):
            if name.startswith("test"):
                yield _wrapTestMethod(getattr(tester, name))


class TestCase(object):
    """
    Base class for datadriven test classes.
    Contains assert methods.
    """
    def assertEqual(self, a, b):
        """
        Tests if a an b are equal. If not, output an error and raise
        an assertion error.
        """
        if a != b:
            raise AssertionError("{} != {}".format(a, b))

    def assertNotEqual(self, a, b):
        """
        Tests if a and b are not equal.  If they are equal, raise
        an assertion error.
        """
        if a == b:
            raise AssertionError("{} == {}".format(a, b))

    def assertTrue(self, x):
        """
        Tests that x is true.  If it is false, raise an assertion error.
        """
        if not bool(x):
            raise AssertionError("{} is False".format(x))

    def assertFalse(self, x):
        """
        Tests that x is false.  If it is true, raise an assertion error.
        """
        if bool(x):
            raise AssertionError("{} is True".format(x))

    def assertIs(self, a, b):
        """
        Tests that a is b.  If it is not, raise an assertion error.
        """
        if a is not b:
            raise AssertionError("{} is not {}".format(a, b))

    def assertIsNot(self, a, b):
        """
        Tests that a is not b.  If a is b, raise an assertion error.
        """
        if a is b:
            raise AssertionError("{} is {}".format(a, b))

    def assertIsNone(self, x):
        """
        Tests that x is None.  If x is not, raise an assertion error.
        """
        if x is not None:
            raise AssertionError("{} is not None".format(x))

    def assertIsNotNone(self, x):
        """
        Tests that x is not None.  If x is None, raise an assertion error.
        """
        if x is None:
            raise AssertionError("{} is None".format(x))

    def assertIn(self, a, b):
        """
        Tests that a is in b.  If a is not in b, raise an assertion error.
        """
        if a not in b:
            raise AssertionError("{} not in {}".format(a, b))

    def assertNotIn(self, a, b):
        """
        Tests that a is not in b.  If a is in b, raise an assertion error.
        """
        if a in b:
            raise AssertionError("{} in {}".format(a, b))

    def assertIsInstance(self, a, b):
        """
        Tests that a is an instance of b.  If a is not an instance of b,
        raise an assertion error.
        """
        if not isinstance(a, b):
            raise AssertionError("{} is not instance of {}".format(a, b))

    def assertNotIsInstance(self, a, b):
        """
        Tests that a is not an instance of b.  If a is an instance of b,
        raise an assertion error.
        """
        if isinstance(a, b):
            raise AssertionError("{} is instance of {}".format(a, b))

    def assertGreater(self, a, b):
        """
        Tests that a is greater than b.  If not, raise an assertion error.
        """
        if a <= b:
            raise AssertionError("{} is not greater than {}".format(a, b))

    def assertGreaterEqual(self, a, b):
        """
        Tests that a is greater than or equal to b.
        If not, raise an assertion error.
        """
        if a < b:
            raise AssertionError(
                "{} is not greater than or equal to {}".format(a, b))

    def assertLess(self, a, b):
        """
        Tests that a is less than b.  If not, raise an assertion error.
        """
        if a >= b:
            raise AssertionError("{} is not less than {}".format(a, b))

    def assertLessEqual(self, a, b):
        """
        Tests that a is less than or equal to b.
        If not, raise an assertion error.
        """
        if a > b:
            raise AssertionError(
                "{} is not less than or equal to {}".format(a, b))

    def assertRaises(self, exceptionType, func=None, *args, **kwargs):
        if func is None:
            return self.assertRaisesWith(exceptionType)
        exceptionRaised = False
        try:
            func(*args, **kwargs)
        except exceptionType:
            exceptionRaised = True
        if not exceptionRaised:
            raise AssertionError(
                "exception of type {} not raised".format(
                    exceptionType.__name__))

    @contextlib.contextmanager
    def assertRaisesWith(self, exceptionType):
        exceptionRaised = False
        try:
            yield
        except exceptionType:
            exceptionRaised = True
        if not exceptionRaised:
            raise AssertionError(
                "exception of type {} not raised".format(
                    exceptionType.__name__))


class DataDrivenTest(TestCase):
    """
    Superclass of all data driven tests for GA4GH datamodel objects.
    A data driven test class is instantiated with a set of data files
    that represent a some aggregation of data (for example, a
    ReferenceSet or VariantSet). We allocate a GA4GH datamodel object
    corresponding to this, and then test that these objects have the
    properties that we expect.
    """
    def __init__(self, setId, baseDir):
        self._setId = setId
        self._dataDir = os.path.join(baseDir, setId)
        self._gaObject = self.getDataModelClass()(
            self._setId, self._dataDir)

    def getSetId(self):
        """
        Return the ID of this GA4GH datamodel object we are testing.
        """
        return self._setId

    def getDataModelClass(self):
        """
        Returns the GA4GH datamodel class that this data driven test
        is exercising.
        """
        raise NotImplementedError()

    def getProtocolClass(self):
        """
        Returns the GA4GH protocol class that this data driven test
        is exercising.
        """
        raise NotImplementedError()

    def testProtocolElementValid(self):
        protocolElement = self._gaObject.toProtocolElement()
        jsonDict = protocolElement.toJsonDict()
        assert self.getProtocolClass().validate(jsonDict)
