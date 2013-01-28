import benchmark

import random
from operator import itemgetter

# Source
# http://writeonly.wordpress.com/2008/08/30/sorting-dictionaries-by-value-in-python-improved/

def fnouter(x):
    return x[1]

class SortDictByValue(benchmark.Benchmark):
    
    label = "Sort Dict with 100 Keys by Value"
    each = 10000
    
    def setUp(self):
        self.d = dict(zip(range(100),range(100)))
    
    def eachSetUp(self):
        random.shuffle(self.d)
    
    def test_pep265(self):
        return sorted(self.d.iteritems(), key=itemgetter(1))
    
    def test_stupid(self):
        return [(k,v) for v,k in sorted([(v,k) for k,v in self.d.iteritems()])]
    
    def test_listExpansion(self):
        L = [(k,v) for (k,v) in self.d.iteritems()]
        return sorted(L, key=lambda x: x[1])
    
    def test_generator(self):
        L = ((k,v) for (k,v) in self.d.iteritems())
        return sorted(L, key=lambda x: x[1])
    
    def test_lambda(self):
        return sorted(self.d.iteritems(), key=lambda x: x[1])
    
    def test_formalFnInner(self):
        def fninner(x):return x[1]
        return sorted(self.d.iteritems(), key=fninner)
    
    def test_formalFnOuter(self):
        return sorted(self.d.iteritems(), key=fnouter)

class SortLargerDictByValue(SortDictByValue):
    
    label = "Sort Dict with 1000 Keys by Value"
    each = 1000
    
    def setUp(self):
        self.d = dict(zip(range(1000),range(1000)))

if __name__ == '__main__':
    benchmark.main() # each is a variable in the above classes