# This is the first time writing anything in Python. Please do not murder me and maybe suggest a better option
# Stats from http://www.iqcomparisonsite.com/iqtable.aspx. Can't find above 200, and
# below 100 are feeble minds unworthy of consideration
import unittest
from scipy.stats import norm

def get_iq_perc(n):
    if n < 100:
        return 0
    else:
        return norm.cdf((n-100)/float(15))

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(get_iq_perc(100), .50)


if __name__ == '__main__':
    unittest.main()