# -*- coding: utf-8 -*-
from Products.Five import BrowserView


class NadomescanjaView(BrowserView):

    def rows(self):
        return self.context.getNadomescanjaRows()
