# -*- coding: utf-8 -*-
import json

from plone import api
from Products.Five import BrowserView


class NadomescanjaDataView(BrowserView):

    def __call__(self):
        portal = api.portal.get()
        payload = {
            'laboratoriji': self._get_labs(portal),
            'zaposleni': self._get_zaposleni(portal),
        }
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(payload, ensure_ascii=False)

    def _get_labs(self, portal):
        try:
            folder = portal.unrestrictedTraverse('laboratoriji')
        except Exception as exc:
            return [{'error': 'laboratoriji folder not found: {}'.format(exc)}]

        result = []
        for obj in folder.objectValues():
            if getattr(obj, 'portal_type', None) != 'laboratorij':
                continue

            vodja_id = getattr(obj, 'privzeti_vodja', '') or ''
            if isinstance(vodja_id, (list, tuple)):
                vodja_id = vodja_id[0] if vodja_id else ''
            vodja_id = str(vodja_id).strip()

            vodja_naziv = ''
            if vodja_id:
                try:
                    vodja_obj = portal.unrestrictedTraverse(
                        'dezurstva/seznam_zaposlenih/{}'.format(vodja_id)
                    )
                    vodja_naziv = vodja_obj.Title()
                except Exception:
                    vodja_naziv = vodja_id

            result.append(
                {
                    'id': obj.getId(),
                    'naziv': obj.Title(),
                    'okrajsava': getattr(obj, 'okrajsava', '') or '',
                    'vodja_id': vodja_id,
                    'vodja_naziv': vodja_naziv,
                }
            )
        return result

    def _get_zaposleni(self, portal):
        try:
            folder = portal.unrestrictedTraverse('dezurstva/seznam_zaposlenih')
        except Exception as exc:
            return [{'error': 'seznam_zaposlenih folder not found: {}'.format(exc)}]

        result = []
        for obj in folder.objectValues():
            obj_id = obj.getId()
            if not obj_id:
                continue
            if getattr(obj, 'getExcludeFromNav', lambda: False)():
                continue
            result.append({'id': obj_id, 'naziv': obj.Title()})
        return result
