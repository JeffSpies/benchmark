
import pytest
import benchmark
import sys
import platform

_PY3 = sys.version_info[0] == 3
_PYPY = platform.python_implementation() == 'PyPy'


def test_install():
    """
    Test the ecample provided in the documentation. Shows that the module
    installs well. Not yet intended to show proper operation--just that it
    properly installs and imports, esp. on Python 3 where previous versions have
    not run. More an integration test than a unit test, but whatev!
    """

    import math

    class Benchmark_Sqrt(benchmark.Benchmark):

        each = 4 # scaled for fast operation

        def setUp(self):
            # Only using setUp in order to subclass later
            # Can also specify tearDown, eachSetUp, and eachTearDown
            self.size = 20

        def test_pow_operator(self):
            for i in xrange(self.size):
                z = i**.5

        def test_pow_function(self):
            for i in xrange(self.size):
                z = pow(i, .5)

        def test_sqrt_function(self):
            for i in xrange(self.size):
                z = math.sqrt(i)

    class Benchmark_Sqrt2(Benchmark_Sqrt):
        # Subclass the previous benchmark to change input using
        # self.setUp()

        label = "Benchmark Sqrt on a larger range"
        # The above label comes from the class name, this oen
        # comes from the label attribute

        each = 9

        def setUp(self):
            self.size = 75

    benchmark.main(format="markdown", numberFormat="%.4g")
