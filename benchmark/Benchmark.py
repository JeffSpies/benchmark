# Copyright 2012--2014 Jeffrey R. Spies
# License: Apache License, Version 2.0
# Website: http://jspi.es/benchmark

import time
import random
import operator
import sys
from . import statistics
from . import tables

def benchmark_fn(tests, each=5, setup=None, teardown=None, eachsetup=None, eachteardown=None):
    pass

class Benchmark(object):
    def __init__(self,

        each=5,

        prefix="test_",
        setUp="setUp",
        tearDown="tearDown",
        eachSetUp="eachSetUp",
        eachTearDown="eachTearDown",

        format="markdown",
        sort_by="mean",
        order=['name', 'rank', 'runs', 'mean', 'sd', 'factor'],
        header=None,
        cellFormats=None,
        numberFormat = "%.4g",

        **kwargs):

        self.__set_from_attribute("each", each)
        self.__set_from_attribute("label", self.__class__.__name__.replace('_', ' '))

        self.__set_from_attribute("format", format)
        self.__set_from_attribute("sort_by", sort_by)
        self.__set_from_attribute("order", order)
        self.__set_from_attribute("header", header)
        self.__set_from_attribute("cellFormats", cellFormats)
        self.__set_from_attribute("numberFormat", numberFormat)

        if sys.platform == "win32":
            self.__timer = time.clock # On Windows, the best timer is time.clock()
        else:
            self.__timer = time.time # On most other platforms the best timer is time.time()

        self.__prefix = prefix
        self.__setUp = setUp
        self.__tearDown = tearDown
        self.__eachSetUp = eachSetUp
        self.__eachTearDown = eachTearDown

    def __collect_tests(self):
        return [test for test in dir(self) if test.startswith(self.__prefix)]

    def __set_from_attribute(self, name, value):
        try:
            getattr(self, name)
        except:
            setattr(self, name, value)

    def __run_test(self, name):
        tick = self.__timer()
        tResult = self.__run_fn(name)
        tTime = self.__timer()-tick
        self.results[name]['total'] += tTime
        self.results[name]['sumOfSq'] += pow(tTime, 2)
        return tTime, tResult

    def __run_fn(self, name):
        return getattr(self, name)()

    def __testAndRunFn(self, name):
        if name in dir(self):
            self.__run_fn(name)

    def run(self, previousResults=None):
        # TODO Add previous results

        self.__testAndRunFn(self.__setUp)

        tests = self.__collect_tests()
        testQueue = []

        self.results = {}
        for number, testname in enumerate(tests):
            self.results[testname] = {'total':0, 'sumOfSq':0}
            testQueue.extend([number for i in range(0, self.each)])

        random.shuffle(testQueue)

        dirSelf = dir(self)

        # Why the following?  Checks to see if eachSetUp and eachTearDown
        # functions would have to be done "each" number of times; this
        # checks once, and then, if there, runs them accordingly.
        if self.__eachSetUp in dirSelf and self.__eachTearDown in dirSelf:
            for testId in testQueue:
                self.__run_fn(self.__eachSetUp)
                self.__run_test(tests[testId])
                self.__run_fn(self.__eachTearDown)
        elif self.__eachSetUp in dirSelf:
            for testId in testQueue:
                self.__run_fn(self.__eachSetUp)
                self.__run_test(tests[testId])
        elif self.__eachTearDown in dirSelf:
            for testId in testQueue:
                self.__run_test(tests[testId])
                self.__run_fn(self.__eachTearDown)
        else:
            for testId in testQueue:
                self.__run_test(tests[testId])

        self.table = []

        for key in list(self.results.keys()):
            row = {}
            row['name'] = key.replace(self.__prefix, '').replace('_', ' ')
            row['runs'] = self.each
            row['mean'] = self.results[key]['total']/row['runs']
            row['total'] = self.results[key]['total']
            row['sumOfSquares'] = self.results[key]['sumOfSq']
            if row['runs'] > 1:
                row['var'] = (row['sumOfSquares']-pow(row['total'], 2)/row['runs'])/(row['runs']-1)
                row['sd'] = row['var']**.5
            else:
                row['var'] = 'NA'
                row['sd'] = 'NA'
            self.table.append(row)

        self.table = sorted(self.table, key=operator.itemgetter('mean'))
        for i, v in enumerate(self.table):
            v['rank'] = i+1
            v['factor'] = str(float(v['mean'])/float(self.table[0]['mean']))
            if row['runs'] > 1:
                v['pvalue'] = statistics.tTest(
                    v['mean'], v['sd'], v['runs'],
                    self.table[0]['mean'], self.table[0]['sd'], self.table[0]['runs'],
                    unequalVariance=True)[2] if i > 0 else 'NA'
            else:
                v['pvalue'] = 'NA'

        self.__testAndRunFn(self.__tearDown)

    def get_total_runs(self):
        return self.each*len(self.table)

    def get_table(self, format=None, sort_by=None, order=None, header=None,
        cellFormats=None, numberFormat = None, **kwargs):

        format = format if format else self.format
        sort_by = sort_by if sort_by else self.sort_by
        order = order if order else self.order
        header = header if header else self.header
        cellFormats = cellFormats if cellFormats else self.cellFormats
        numberFormat = numberFormat if numberFormat else self.numberFormat

        self.table = sorted(self.table, key=operator.itemgetter(sort_by))

        header = header if header else order

        reduced_table = []
        for i in self.table:
            row = []
            for inc, o in enumerate(order):
                value = i[o]
                if cellFormats:
                    try:
                        value = cellFormats[inc] % float(value)
                    except:
                        try:
                            value = cellFormats[inc] % str(value)
                        except:
                            pass
                else:
                    try:
                        value = numberFormat % float(value)
                    except: pass
                value = str(value)
                row.append(value)
            reduced_table.append(row)

        if format.lower() in ['markdown', 'md']:
            return tables.as_markdown(header, reduced_table)
        elif format.lower() in ['csv', 'comma']:
            return tables.as_csv(header, reduced_table)
        else:
            return tables.as_rst(header, reduced_table)
