# Copyright 2012 Jeffrey R. Spies
# License: Apache License, Version 2.0
# Website: http://jspi.es/benchmark

from . import __VERSION__
from . import Benchmark

import time
import platform
import os
import sys
from six import string_types


class BenchmarkProgram(object):
    
    def __init__(self, module="__main__", **kwargs):
        if isinstance(module, string_types):
            self.module = __import__(module)
        
        benchmarks = self.loadFromModule(self.module)
        
        totalRuns = 0
        objects = []
        for obj in benchmarks:
            obj = obj(**kwargs)
            obj.run()
            objects.append(obj)
            totalRuns += obj.get_total_runs()
        
        title = 'Benchmark Report'
        info = 'Each of the above %s runs were run in random, non-consecutive order by' % str(totalRuns)
        info += os.linesep
        info += '`benchmark` v' + __VERSION__ + ' (http://jspi.es/benchmark) with Python ' + platform.python_version()
        info += os.linesep
        info += '%s-%s-%s on %s' % (
            platform.system(), 
            platform.release(), 
            platform.machine(), 
            time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        ) + '.'
        
        sys.stdout.write(self.printMarkdown(objects, title, info, **kwargs))
    
    def printMarkdown(self, benchmarks, title, info, **kwargs):
        lines = ''

        lines += os.linesep
        lines += title
        lines += os.linesep + '='*len(title)
        lines += os.linesep*2
        
        for obj in benchmarks:
            title = obj.label
            labelLength = len(title) if len(title) > 5 else 5
            lines += title
            lines += os.linesep
            lines += '-'*labelLength
            lines += os.linesep*2
            
            lines += obj.get_table(**kwargs)
            lines += os.linesep*2
        
        lines += info
        lines += os.linesep*2

        return lines
        
    def loadFromModule(self, module):
        benchmarks = []
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, Benchmark.Benchmark):
                benchmarks.append(obj)
        return benchmarks

main = BenchmarkProgram