"""Test setup for integration and functional tests."""

from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Testing import ZopeTestCase as ztc


@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    import nadomescanja.produkti
    zcml.load_config('configure.zcml', nadomescanja.produkti)
    fiveconfigure.debug_mode = False
    ztc.installPackage('nadomescanja.produkti')


setup_product()
ptc.setupPloneSite(products=['nadomescanja.produkti'])


class TestCase(ptc.PloneTestCase):
    """Base class for package tests."""


class FunctionalTestCase(ptc.FunctionalTestCase):
    """Base class for functional doctests."""

    def afterSetUp(self):
        roles = ('Member', 'Contributor')
        self.portal.portal_membership.addMember('contributor', 'secret', roles, [])
