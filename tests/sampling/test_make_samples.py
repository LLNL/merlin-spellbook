import os
import numpy as np
import numpy.testing

from spellbook.sampling.make_samples import scale_samples
from spellbook.ml.learn import stack_arrays


def test_scale_samples_nolog():

# Turn 0:1 samples into -1:1

 norm_values = np.linspace(0,1,5).reshape((-1,1))
 real_values = scale_samples(norm_values, [(-1,1)])
 expected =   np.array([[-1. ], [-0.5], [ 0. ], [ 0.5], [ 1. ]])

 print ("real------------------------------")
 print(real_values)
 print ("expected------------------------------")
 print(expected)

 numpy.testing.assert_array_equal(real_values, expected)
 
def test_scale_samples_log():
  norm_values = np.linspace(0,1,5).reshape((1,5))
  real_values = scale_samples(norm_values, [(1,10)], do_log=True)
  print ("real------------------------------")
  print(real_values)
  expected = [[  1.0,
           1.77,
           3.16,
           5.62,
           10.0]]
  print ("expected------------------------------")
  print(expected)
  numpy.testing.assert_allclose(real_values, expected, rtol=0.02, atol=.02,verbose=True)
