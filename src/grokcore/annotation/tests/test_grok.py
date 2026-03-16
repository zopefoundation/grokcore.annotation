import doctest
import importlib
import unittest
from importlib.resources import files

import zope.component.eventtesting
from zope.testing import cleanup


def setUpZope(test):
    zope.component.eventtesting.setUp(test)


def cleanUpZope(test):
    cleanup.cleanUp()


def suiteFromPackage(name):
    # Get the parent package (grokcore.annotation.tests)
    parent_package_name = __name__.rsplit('.', 1)[0]
    parent_package = importlib.import_module(parent_package_name)
    resource_path = files(parent_package).joinpath(name)
    file_list = [f.name for f in resource_path.iterdir()]
    suite = unittest.TestSuite()
    for filename in file_list:
        if not filename.endswith('.py'):
            continue
        if filename.endswith('_fixture.py'):
            continue
        if filename == '__init__.py':
            continue

        dottedname = 'grokcore.annotation.tests.{}.{}'.format(
            name, filename[:-3])
        test = doctest.DocTestSuite(
            dottedname,
            setUp=setUpZope,
            tearDown=cleanUpZope,
            optionflags=(
                doctest.ELLIPSIS +
                doctest.NORMALIZE_WHITESPACE)
        )

        suite.addTest(test)
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in ['annotation', ]:
        suite.addTest(suiteFromPackage(name))
    return suite
