"""Definition of the dezurstvo content type (Dexterity)."""

import json
from io import BytesIO

from DateTime.DateTime import DateTime
from plone import api
from plone.dexterity.content import Container
from xlwt import Workbook
from zope.interface import implementer

from nadomescanja.produkti.interfaces import Idezurstvo


@implementer(Idezurstvo)
class dezurstvo(Container):
    """Dexterity-based dezurstvo content type for nadomescanja."""

    meta_type = "dezurstvo"
    portal_type = "dezurstvo"

    nadomescanja_json = u"[]"

    def getNadomescanja_json(self):
        value = getattr(self, 'nadomescanja_json', u'[]') or u'[]'
        if isinstance(value, bytes):
            return value.decode('utf-8', errors='replace')
        return value

    def getNadomescanjaRows(self):
        raw = self.getNadomescanja_json()
        try:
            rows = json.loads(raw or '[]')
        except (TypeError, ValueError):
            return []
        return rows if isinstance(rows, list) else []

    def getNadomescanjaDict(self):
        rows = self.getNadomescanjaRows()
        return {
            row.get('laboratorij_okrajsava'): row.get('nadomestni_vodja_naziv')
            for row in rows
            if row.get('laboratorij_okrajsava')
        }

    def getSampleVocabulary50(self):
        try:
            obj = api.portal.get().restrictedTraverse('dezurstva/seznam_zaposlenih')
            obj = obj.getFolderContents(contentFilter={'sort_on': 'getObjPositionInParent'})
        except Exception:
            return [('', '')]

        vocabulary = [('', '')]
        for item in obj:
            description = str(item.Description or '')
            if '|' not in description:
                continue
            target = item.getObject()
            if getattr(target, 'getExcludeFromNav', lambda: False)():
                continue
            suffix = description.split('|', 1)[1]
            vocabulary.append((item.id if suffix == '-' else suffix, item.Title))
        return vocabulary

    def excel_export(self, first_day, last_day, oseba):
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog(portal_type="dezurstvo", sort_on="id")
        nadomescanja = []
        for brain in brains:
            brain_id = brain.id
            if 'undefined' in brain_id:
                continue
            if brain_id == 'objekt-za-seznam-zaposlenih-v-formi-spremeni-nadomescanje-ne-brisi':
                continue
            try:
                current_day = DateTime(brain_id)
            except Exception:
                continue
            if current_day < first_day or current_day > last_day:
                continue
            nadomescanja.append(brain)

        if oseba:
            filtered = []
            for brain in nadomescanja:
                for row in brain.getObject().getNadomescanjaRows():
                    if oseba == row.get('nadomestni_vodja_id'):
                        filtered.append(brain)
                        break
            nadomescanja = filtered

        workbook = Workbook()
        sheet = workbook.add_sheet('izpis')

        od = '.'.join(reversed(first_day.Date().split('/')))
        do = '.'.join(reversed(last_day.Date().split('/')))
        title = 'Izpis: {} - {}'.format(od, do)
        if oseba:
            try:
                person = self.restrictedTraverse('dezurstva/seznam_zaposlenih/{}'.format(oseba)).Title()
                title = '{} za osebo {}'.format(title, person)
            except Exception:
                title = '{} za osebo {}'.format(title, oseba)
        sheet.write(0, 0, title)

        row_index = 2
        sheet.write(row_index, 0, 'Datum')
        sheet.write(row_index, 1, 'Enota')
        sheet.write(row_index, 2, 'Vodja')
        sheet.write(row_index, 3, 'Nadomešča')

        for brain in nadomescanja:
            datum = '.'.join(reversed(brain.id.split('-')))
            for row in brain.getObject().getNadomescanjaRows():
                if oseba and oseba != row.get('nadomestni_vodja_id'):
                    continue
                row_index += 1
                sheet.write(row_index, 0, datum)
                sheet.write(row_index, 1, row.get('laboratorij_okrajsava', ''))
                sheet.write(row_index, 2, row.get('privzeti_vodja_naziv', ''))
                sheet.write(row_index, 3, row.get('nadomestni_vodja_naziv', ''))

        output = BytesIO()
        workbook.save(output)

        request = getattr(self, 'request', self.REQUEST)
        response = request.RESPONSE
        response.setHeader("Content-type", "application/vnd.ms-excel")
        od = '_'.join(reversed(first_day.Date().split('/')))
        do = '_'.join(reversed(last_day.Date().split('/')))
        response.setHeader("Content-disposition", "attachment;filename=izpis_{}-{}.xls".format(od, do))
        response.write(output.getvalue())
        return response
