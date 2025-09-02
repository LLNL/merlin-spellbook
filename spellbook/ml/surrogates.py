##############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other
# Merlin-Spellbook Project developers. See top-level LICENSE and COPYRIGHT
# files for dates and other details. No copyright assignment is required to
# contribute to Merlin-Spellbook.
##############################################################################

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
            raise ValueError("Unknown regressor name " + name + "! For valid choices see sklearnRegressors.names()")

    @classmethod
    def names(cls):
        return sorted(cls.all_regs.keys())


def test_factory():

    regressors = sklearnRegressors.names()
    for r in regressors:
        _ = sklearnRegressors.factory(r)


def test_random_forest():

    rf1 = sklearnRegressors.factory("RandomForestRegressor", n_estimators=10, max_depth=5)
    rf2 = sklearnRegressors.factory("RandomForestRegressor", n_estimators=2, max_depth=3)

    assert rf1.n_estimators == 10
    assert rf1.max_depth == 5

    assert rf2.n_estimators == 2
    assert rf2.max_depth == 3


if __name__ == "__main__":
    test_factory()
    test_random_forest()
