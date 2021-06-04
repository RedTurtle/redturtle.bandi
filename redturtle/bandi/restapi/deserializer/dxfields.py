# -*- coding: utf-8 -*-
from datetime import timedelta
from plone.app.contenttypes.interfaces import ILink
from plone.app.textfield.interfaces import IRichText
from plone.app.textfield.value import RichTextValue
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile.interfaces import INamedField
from plone.restapi.interfaces import IFieldDeserializer
from plone.restapi.services.content.tus import TUSUpload
from pytz import timezone
from pytz import utc
from z3c.form.interfaces import IDataManager
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import ICollection
from zope.schema.interfaces import IDatetime
from zope.schema.interfaces import IDict
from zope.schema.interfaces import IField
from zope.schema.interfaces import IFromUnicode
from zope.schema.interfaces import ITextLine
from zope.schema.interfaces import ITime
from zope.schema.interfaces import ITimedelta
from zope.schema.interfaces import IVocabularyTokenized
from redturtle.bandi.interfaces.bando import IBando
from plone.restapi.deserializer.dxfields import (
    DatetimeFieldDeserializer as DefaultDatetimeFieldDeserializer,
)
from plone.app.event.base import default_timezone

import codecs
import pytz
import dateutil
import six


@implementer(IFieldDeserializer)
@adapter(IDatetime, IBando, IBrowserRequest)
class DatetimeFieldDeserializer(DefaultDatetimeFieldDeserializer):
    def __call__(self, value):
        # Datetime fields may contain timezone naive or timezone aware
        # objects. Unfortunately the zope.schema.Datetime field does not
        # contain any information if the field value should be timezone naive
        # or timezone aware. While some fields (start, end) store timezone
        # aware objects others (effective, expires) store timezone naive
        # objects.
        # We try to guess the correct deserialization from the current field
        # value.

        if value is None:
            self.field.validate(value)
            return

        # get tz from already stored value
        dm = queryMultiAdapter((self.context, self.field), IDataManager)
        current = dm.get()
        if current is not None:
            tzinfo = current.tzinfo
        else:
            # this is the patch
            tzinfo = pytz.timezone(default_timezone())

        # Parse ISO 8601 string with dateutil
        try:
            dt = dateutil.parser.parse(value)
        except ValueError:
            raise ValueError(u"Invalid date: {}".format(value))

        # Convert to TZ aware in UTC
        if dt.tzinfo is not None:
            dt = dt.astimezone(utc)
        else:
            dt = utc.localize(dt)

        # Convert to local TZ aware or naive UTC
        if tzinfo is not None:
            tz = timezone(tzinfo.zone)
            value = tz.normalize(dt.astimezone(tz))
        else:
            value = utc.normalize(dt.astimezone(utc)).replace(tzinfo=None)

        self.field.validate(value)
        return value
