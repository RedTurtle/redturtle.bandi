from plone.app.querystring.interfaces import IQueryModifier
from zope.interface import provider
from plone.restapi.serializer.converters import json_compatible
from DateTime import DateTime


@provider(IQueryModifier)
def modify_bandi_state_query(query):
    now = json_compatible(DateTime())
    item = None
    query_extender = []

    state_operators = {
        "open": (
            {
                "o": "plone.app.querystring.operation.date.afterDateTime",
                "v": now,
                "i": "scadenza_bando",
            },
            {
                "o": "plone.app.querystring.operation.date.afterDateTime",
                "v": now,
                "i": "chiusura_procedimento_bando",
            },
        ),
        "in-progress": (
            {
                "o": "plone.app.querystring.operation.date.beforeDateTime",
                "v": now,
                "i": "scadenza_bando",
            },
            {
                "o": "plone.app.querystring.operation.date.afterDateTime",
                "v": now,
                "i": "chiusura_procedimento_bando",
            },
        ),
        "closed": (
            {
                "o": "plone.app.querystring.operation.date.beforeDateTime",
                "v": now,
                "i": "chiusura_procedimento_bando",
            },
        ),
        "scheduled": (
            {
                "o": "plone.app.querystring.operation.date.afterDateTime",
                "v": now,
                "i": "apertura_bando",
            },
        ),
    }

    query_items_to_remove = []

    for i in query:
        if i.get("i", "") == "bando_state":
            item = i

            value = i.get("v", "")

            if type(value) is list:
                value = value and value[0] or ""

            operator = state_operators.get(value, None)

            if operator:
                query_extender.extend(operator)
                query_items_to_remove.append(item)

    if query_extender:
        for i in query_items_to_remove:
            query.remove(i)

        query.extend(query_extender)

    return query
