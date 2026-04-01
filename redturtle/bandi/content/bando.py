# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from zope.interface import implementer

from redturtle.bandi.interfaces.bando import IBando


@implementer(IBando)
class Bando(Container):
    """ """
