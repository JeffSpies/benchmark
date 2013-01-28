import benchmark

import time

class BenchmarkPause(benchmark.Benchmark):
    
    def test_one_hundredth(self):
        time.sleep(.01)
    
    def test_one_tenth(self):
        time.sleep(.1)
    
if __name__ == '__main__':
    benchmark.main(each=10)