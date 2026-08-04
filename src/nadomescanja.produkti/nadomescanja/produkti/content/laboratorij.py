"""Definition of the laboratorij content type (Dexterity)."""

from plone import api
from plone.dexterity.content import Container
from zope.interface import implementer

from nadomescanja.produkti.interfaces import Ilaboratorij


@implementer(Ilaboratorij)
class laboratorij(Container):
    """Dexterity-based laboratorij content type for nadomescanja."""

    meta_type = "laboratorij"
    portal_type = "laboratorij"

    okrajsava = u""
    privzeti_vodja = ()

    def getOkrajsava(self):
        return getattr(self, 'okrajsava', u'') or u''

    def getPrivzeti_vodja(self):
        return getattr(self, 'privzeti_vodja', ()) or ()

    def getSampleVocabulary40(self):
        try:
            folder = api.portal.get().unrestrictedTraverse('dezurstva/seznam_zaposlenih')
        except Exception:
            return []

        values = []
        for obj in folder.objectValues():
            if not obj.getId():
                continue
            if getattr(obj, 'getExcludeFromNav', lambda: False)():
                continue
            values.append((obj.getId(), obj.Title()))
        return values
