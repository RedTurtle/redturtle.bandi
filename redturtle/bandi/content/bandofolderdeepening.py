# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from zope.interface import implementer

from redturtle.bandi.interfaces.bandofolderdeepening import IBandoFolderDeepening


@implementer(IBandoFolderDeepening)
class BandoFolderDeepening(Container):
    """ """
