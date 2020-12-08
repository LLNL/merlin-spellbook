###############################################################################
# Copyright (c) 2019, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory
# Written by the Merlin dev team, listed in the CONTRIBUTORS file.
# <merlin@llnl.gov>
#
# LLNL-CODE-797170
# All rights reserved.
# This file is part of merlin-spellbook.
#
# For details, see https://github.com/LLNL/merlin-spellbook and
# https://github.com/LLNL/merlin.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################

from __future__ import print_function

from sklearn import base


try:
    from sklearn.utils import all_estimators
except ImportError:
    from sklearn.utils.testing import all_estimators


class sklearnRegressors(object):
    """Scikit learn regressor factory.

    Usage:
    import surrogates
    rf1 = surrogates.sklearnRegressors.factory('RandomForestRegressor', n_estimators=5, max_depth=3)
    gp1 = surrogates.sklearnRegressors.factory('GaussianProcessRegressor')
    choices = surrogates.sklearnRegressors.names()
    """

    def reg_dict():
        _all_regressors = {}
        estimators = all_estimators()
        for name, class_ in estimators:
            if issubclass(class_, base.RegressorMixin):
                _all_regressors[name] = class_
        return _all_regressors

    all_regs = reg_dict()

    @classmethod
    def factory(cls, name, *args, **kwargs):
        if name in cls.all_regs:
            return cls.all_regs[name](*args, **kwargs)
        else:
            raise ValueError(
                "Unknown regressor name "
                + name
                + "! For valid choices see sklearnRegressors.names()"
            )

    @classmethod
    def names(cls):
        return sorted(cls.all_regs.keys())


def test_factory():

    regressors = sklearnRegressors.names()
    for r in regressors:
        _ = sklearnRegressors.factory(r)


def test_random_forest():

    rf1 = sklearnRegressors.factory(
        "RandomForestRegressor", n_estimators=10, max_depth=5
    )
    rf2 = sklearnRegressors.factory(
        "RandomForestRegressor", n_estimators=2, max_depth=3
    )

    assert rf1.n_estimators == 10
    assert rf1.max_depth == 5

    assert rf2.n_estimators == 2
    assert rf2.max_depth == 3


if __name__ == "__main__":
    test_factory()
    test_random_forest()
