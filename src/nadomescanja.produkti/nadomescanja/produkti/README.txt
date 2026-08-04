Introduction
============

This doctest exercises the migrated Dexterity content types without relying on
legacy site data.

    >>> import json
    >>> portal = self.portal

We can create both migrated content types in the test portal.

    >>> dezurstvo_id = portal.invokeFactory(
    ...     'dezurstvo',
    ...     id='dezurstvo-sample',
    ...     title='Dezurstvo Sample',
    ... )
    >>> laboratorij_id = portal.invokeFactory(
    ...     'laboratorij',
    ...     id='laboratorij-sample',
    ...     title='Laboratorij Sample',
    ... )
    >>> dezurstvo = portal[dezurstvo_id]
    >>> laboratorij = portal[laboratorij_id]
    >>> dezurstvo.portal_type
    'dezurstvo'
    >>> laboratorij.portal_type
    'laboratorij'

The migrated classes expose safe defaults when legacy data is missing.

    >>> dezurstvo.getNadomescanjaRows()
    []
    >>> dezurstvo.getNadomescanjaDict()
    {}
    >>> laboratorij.getOkrajsava()
    ''
    >>> laboratorij.getPrivzeti_vodja()
    ()
    >>> laboratorij.getSampleVocabulary40()
    []

Serialized nadomescanja rows are parsed back into Python values.

    >>> sample_rows = [
    ...     {
    ...         'laboratorij_okrajsava': 'LAB',
    ...         'privzeti_vodja_naziv': 'Dr. Privzeti',
    ...         'nadomestni_vodja_id': 'nadomestni-1',
    ...         'nadomestni_vodja_naziv': 'Dr. Nadomestni',
    ...     }
    ... ]
    >>> dezurstvo.nadomescanja_json = json.dumps(sample_rows)
    >>> dezurstvo.getNadomescanjaRows() == sample_rows
    True
    >>> dezurstvo.getNadomescanjaDict()
    {'LAB': 'Dr. Nadomestni'}

The browser views remain callable even when the external folders they expect do
not exist in the test site.

    >>> dezurstvo_view = dezurstvo.restrictedTraverse('@@nadomescanja_view')
    >>> dezurstvo_view.rows() == sample_rows
    True
    >>> data_view = portal.restrictedTraverse('@@nadomescanja-data-json')
    >>> payload = json.loads(data_view())
    >>> sorted(payload.keys())
    ['laboratoriji', 'zaposleni']
    >>> payload['laboratoriji'][0]['error'].startswith('laboratoriji folder not found:')
    True
    >>> payload['zaposleni'][0]['error'].startswith('seznam_zaposlenih folder not found:')
    True
