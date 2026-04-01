# -*- coding: utf-8 -*-
from collective.tiles.collection.interfaces import ICollectionTileRenderer
from Products.Five.browser import BrowserView
from zope.interface import implementer

from redturtle.bandi import bandiMessageFactory as _


@implementer(ICollectionTileRenderer)
class View(BrowserView):

    display_name = _("bandi_layout", default="Layout Bandi")
