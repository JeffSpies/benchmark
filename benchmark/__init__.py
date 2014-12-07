__author__ = "Jeffrey R. Spies"
__copyright__ = "Copyright 2012--2014 Jeffrey R. Spies"
__credits__ = ["Jeffrey R. Spies", "Russel Winder"]
__license__ = "Apache License, Version 2.0"
__VERSION__ = '0.1.7-SNAPSHOT'
__maintainer__ = "Jeffrey R. Spies"
__email__ = "jspies@gmail.com"
__status__ = "Beta"

import sys

if sys.version_info >= (3, 0):
    from .main import BenchmarkProgram, main
    from .Benchmark import Benchmark
else:
    from main import BenchmarkProgram, main
    from Benchmark import Benchmark
