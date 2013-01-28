import benchmark

import time
import datetime

class TimeTests(benchmark.Benchmark):
    label = 'datetime vs. time'
    def test_utcnow(self):
        return datetime.datetime.utcnow().isoformat()[:-6]+'000Z'
    
    def test_gmtime(self):
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

if __name__ == '__main__':
    benchmark.main(
        each=100, 
        format='rst', 
        order = ['rank', 'name', 'runs', 'mean'], # no sd
        header=["Rank", "Name","Runs", "Mean (s)"]
    )
