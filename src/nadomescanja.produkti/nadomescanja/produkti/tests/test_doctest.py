import doctest
import unittest

from Testing import ZopeTestCase as ztc

from nadomescanja.produkti.tests import base


def test_suite():
    return unittest.TestSuite([
        ztc.ZopeDocFileSuite(
            'README.txt',
            package='nadomescanja.produkti',
            test_class=base.FunctionalTestCase,
            optionflags=(
                doctest.REPORT_ONLY_FIRST_FAILURE
                | doctest.NORMALIZE_WHITESPACE
                | doctest.ELLIPSIS
            ),
        ),
    ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
