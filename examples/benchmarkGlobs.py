import benchmark

import tempfile
import os
from glob import iglob
import fnmatch
import re

# Source
# http://www.reddit.com/r/Python/comments/de2xp/dae_need_this_in_a_lot_of_projects/c0zj813?context=3

class BenchmarkGlobs(benchmark.Benchmark):
    
    label = "Glob Tests"
    
    def setUp(self):
        self.walk_root = tempfile.gettempdir()
        for i in xrange(0, 100):
            tempfile.mkstemp(suffix=".txt")
    
    def test_glob(self):
        items = []
        for root, dirs, files in os.walk(self.walk_root):
            for item in iglob(os.path.join(root, '*.txt')):
                items.append(item)
    
    def test_fnmatch(self):
        items = []
        for root, dirs, files in os.walk(self.walk_root):
            for item in fnmatch.filter(files, '*.txt'):
                items.append(os.path.join(root, item))
    
    def test_re(self):
        items = []
        rex = re.compile(".*\.txt$")
        for root, dirs, files in os.walk(self.walk_root):
            for item in files:
                if rex.match(item):
                    items.append(os.path.join(root, item))

if __name__ == '__main__':
    benchmark.main(each=50)