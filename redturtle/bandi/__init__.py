"""Main product initializer"""

import logging

from zope.i18nmessageid import MessageFactory

logger = logging.getLogger("redturtle.bandi")
bandiMessageFactory = MessageFactory("redturtle.bandi")
_ = bandiMessageFactory
