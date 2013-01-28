import benchmark

import math

# Inspired by
# http://stackoverflow.com/questions/327002/which-is-faster-in-python-x-5-or-math-sqrtx

class Benchmark_Sqrt(benchmark.Benchmark):

    each = 50 # allows for differing number of runs

    def setUp(self):
        # Only using setUp in order to subclass later
        # Can also specify tearDown, eachSetUp, and eachTearDown
        self.size = 25000

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
    # Subclass the previous benchmark to change input using self.setUp()
    
    label = "Benchmark Sqrt on a larger range"
    # The benchmark abovel comes from the class name; this one comes from the
    # label attribute
    
    each = 10

    format="rst"
    sort_by = "mean" # could be anything allowed in order list
    label = "Benchmark Sqrt on a larger range"
    order =  ['name', 'rank', 'runs', 'mean', 'sd', 'factor', 'pvalue']
    header = ['Test', 'Rank', 'Runs', 'Mean (s)', 'SD (s)', 'Factor', 'T-Test P-Value']
    cellFormats = ['%s', '%d', '%d', "%.3e", "%.3e", "%.2g", "%.2g"]
    
    def setUp(self):
        self.size = 750000


if __name__ == '__main__':
    benchmark.main(format="markdown", numberFormat="%.5g", sort_by="mean") 
    # could have written benchmark.main(each=10) if the
    # first class shouldn't have been run 50 times.