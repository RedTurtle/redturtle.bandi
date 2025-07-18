# -*- coding: utf-8 -*-
from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName


def runProfile(portal, profileName):
    setupTool = getToolByName(portal, "portal_setup")
    setupTool.runAllImportStepsFromProfile(profileName)


def uninstall(portal, reinstall=False):
    out = StringIO()
    if not reinstall:
        runProfile(portal, "profile-redturtle.bandi:uninstall")
