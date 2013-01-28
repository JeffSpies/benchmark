"""
These functions are mostly:

Copyright (c) Maurice H.T. Ling <mauriceling@acm.org>
@see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python 
Papers Source Codes 1:4

The exception is my t-test function at the end:

Copyright Jeffrey R. Spies <jspies@gmail.com>
"""
  
import math
import random

def gammln(n):
    """
    Complete Gamma function.
    @see: NRP 6.1
    @see: http://mail.python.org/pipermail/python-list/2000-June/671838.html
    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python 
    Papers Source Codes 1:4
  
    @param n: float number
    @return: float number
    """
    gammln_cof = [76.18009173, -86.50532033, 24.01409822,
                  -1.231739516e0, 0.120858003e-2, -0.536382e-5]
    x = n - 1.0
    tmp = x + 5.5
    tmp = (x + 0.5) * math.log(tmp) - tmp
    ser = 1.0
    for j in range(6):
        x = x + 1.
        ser = ser + gammln_cof[j] / x
    return tmp + math.log(2.50662827465 * ser)

def betacf(a, b, x):
    """
    Continued fraction for incomplete beta function.
    Adapted from salstat_stats.py of SalStat (www.sf.net/projects/salstat)
    @see: NRP 6.3
    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python 
    Papers Source Codes 1:4
    """
    iter_max = 200
    eps = 3.0e-7

    bm = az = am = 1.0
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    bz = 1.0 - qab * x / qap
    for i in range(iter_max + 1):
        em = float(i + 1)
        tem = em + em
        d = em * (b - em) * x / ((qam + tem) * (a + tem))
        ap = az + d * am
        bp = bz + d * bm
        d = -(a + em) * (qab + em) * x / ((qap + tem) * (a + tem))
        app = ap + d * az
        bpp = bp + d * bz
        aold = az
        am = ap / bpp
        bm = bp / bpp
        az = app / bpp
        bz = 1.0
        if (abs(az - aold) < (eps * abs(az))):
            return az

def betai(a, b, x):
    """
    Incomplete beta function

    I-sub-x(a,b) = 1/B(a,b)*(Integral(0,x) of t^(a-1)(1-t)^(b-1) dt)

    where a,b>0 and B(a,b) = G(a)*G(b)/(G(a+b)) where G(a) is the gamma
    function of a.

    Adapted from salstat_stats.py of SalStat (www.sf.net/projects/salstat)
    Depend: betacf, gammln
    @see: NRP 6.3

    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python 
    Papers Source Codes 1:4
    """
    if (x < 0.0 or x > 1.0):
        raise ValueError('Bad value for x: %s' % x)
    if (x == 0.0 or x == 1.0):
        bt = 0.0
    else:
        bt = math.exp(gammln(a+b) - gammln(a) - gammln(b) + a *
                      math.log(x) + b * math.log(1.0-x))
    if (x < (a + 1.0) / (a + b + 2.0)):
        return bt * betacf(a, b, x) / float(a)
    else:
        return 1.0 - bt * betacf(b, a, 1.0 - x) / float(b)
  
class TDistribution(object):
    """
    Class for Student's t-distribution.
  
    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python 
    Papers Source Codes 1:4
    """
  
    def __init__(self, location=0.0, scale=1.0, shape=2):
        """Constructor method. The parameters are used to construct
        the probability distribution.
  
        @param location: default = 0.0
        @param scale: default = 1.0
        @param shape: degrees of freedom; default = 2"""
        self._mean = float(location)
        self.stdev = float(scale)
        self.df = float(shape)
  
    def CDF(self, x):
        """
        Cummulative Distribution Function, which gives the cummulative
        probability (area under the probability curve) from -infinity or 0 to
        a give x-value on the x-axis where y-axis is the probability.
        """
        t = (x - self._mean) / self.stdev
        a = betai(self.df / 2.0, 0.5, self.df / (self.df + (t * t)))
        if t > 0:
            return 1 - 0.5 * a
        else:
            return 0.5 * a
  
    def PDF(self, x):
        """
        Calculates the density (probability) at x with n-th degrees of freedom
        as
        M{f(x) = S{Gamma}((n+1)/2) / 
        (sqrt(n * pi) S{Gamma}(n/2)) (1 + x^2/n)^-((n+1)/2)}
  
        for all real x. It has mean 0 (for n > 1) and variance n/(n-2) 
        (for n > 2)."""
        a = gammln((self.df + 1) / 2)
        b = math.sqrt(math.pi * self.df) * gammln(self.df / 2) * \
            self.stdev
        c = 1 + ((((x - self._mean) / self.stdev) ** 2) / self.df)
        return (a / b) * (c ** ((-1 - self.df) / 2))
  
    def inverseCDF(self, probability, start = -10.0, 
                   end = 10.0, error = 10e-8): 
        """
        It does the reverse of CDF() method, it takes a probability value and 
        returns the corresponding value on the x-axis, together with the 
        cumulative probability.
  
        @param probability: probability under the curve from -infinity
        @param start: lower boundary of calculation (default = -10)
        @param end: upper boundary of calculation (default = 10)
        @param error: error between the given and calculated probabilities 
        (default = 10e-8)
        @return: Returns a tuple (start, cprob) where 'start' is the standard 
        deviation for the area under the curve from -infinity to the given 
        'probability' (+/- step). 'cprob' is the calculated area under the 
        curve from -infinity to the returned 'start'.
        """
  
        # check for tolerance
        if abs(self.CDF(start)-probability) < error:
            return (start, self.CDF(start))
        # case 1: lower than -10 standard deviations
        if probability < self.CDF(start):
            return self.inverseCDF(probability, start-10, start, error)
        # case 2: between -10 to 10 standard deviations (bisection method)
        if probability > self.CDF(start) and \
        probability < self.CDF((start+end)/2):
            return self.inverseCDF(probability, start, (start+end)/2, error)
        if probability > self.CDF((start+end)/2) and \
        probability < self.CDF(end):
            return self.inverseCDF(probability, (start+end)/2, end, error)
        # case 3: higher than 10 standard deviations
        if probability > self.CDF(end):
            return self.inverseCDF(probability, end, end+10, error)
        # cprob = self.CDF(start)
        # if probability < cprob:
            # return (start, cprob)
        # while probability > cprob:
            # start = start + step
            # cprob = self.CDF(start)
        # return (start, cprob)
  
  
    def mean(self):
        """Gives the arithmetic mean of the sample."""
        return self._mean
  
    def mode(self):
        """Gives the mode of the sample."""
        return self._mean
  
    def kurtosis(self):
        """Gives the kurtosis of the sample."""
        a = ((self.df - 2) ** 2) * gammln((self.df / 2) - 2)
        return 3 * ((a / (4 * gammln(self.df / 2))) - 1)
  
    def skew(self):
        """Gives the skew of the sample."""
        return 0.0
  
    def variance(self):
        """Gives the variance of the sample."""
        return (self.df / (self.df - 2)) * self.stdev * self.stdev

# jspies
def tTest(mean1, s1, n1, mean2, s2, n2, unequalVariance=True):
    mean1, s1, n1, mean2, s2, n2 = (float(x) for x in [mean1, s1, n1, mean2, s2, n2])
    if n1 == n2:
        if not unequalVariance:
            sxx = (.5 * (pow(s1, 2) + pow(s2, 2)))**.5
            t = (mean1-mean2)/(sxx*((2/n1)**.5))
            df = 2*n1-2
        else:
            sxx = (pow(s1, 2)/n1 + pow(s2, 2)/n2)**.5
            t = (mean1-mean2)/sxx
            df = (sxx**2)**2/(((s1**2/n1)**2/(n1-1)) + ((s2**2/n2)**2/(n2-1)))

        p = 1-TDistribution(shape=df).CDF(t)
        
        return t, df, p
    else:
        return None