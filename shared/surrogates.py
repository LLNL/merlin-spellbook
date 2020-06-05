from sklearn.utils.testing import all_estimators
from sklearn import base

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
            print(f"Unknown regressor name {name}! For valid choices see sklearnRegressors.names():")

    @classmethod
    def names(cls):
        return sorted(cls.all_regs.keys())


def test_factory():

    regressors = sklearnRegressors.names()
    print("Building regressor objects...")
    for r in regressors:
        print(r, sklearnRegressors.factory(r))


def test_random_forest():

    rf1 = sklearnRegressors.factory('RandomForestRegressor',n_estimators=10,max_depth=5)
    rf2 = sklearnRegressors.factory('RandomForestRegressor',n_estimators=2,max_depth=3)

    print(rf1)
    print(rf2)
 
if __name__ == '__main__':
    test_factory()
    test_random_forest()
