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
                "o": "plone.app.querystring.operation.date.largerThanRelativeDate",
                "v": now,
                "i": "scadenza_bando",
            },
            {
                "o": "plone.app.querystring.operation.date.largerThanRelativeDate",
                "v": now,
                "i": "chiusura_procedimento_bando",
            },
        ),
        "in-progress": (
            {
                "o": "plone.app.querystring.operation.date.lessThanRelativeDate",
                "v": now,
                "i": "scadenza_bando",
            },
            {
                "o": "plone.app.querystring.operation.date.largerThanRelativeDate",
                "v": now,
                "i": "chiusura_procedimento_bando",
            },
        ),
        "closed": (
            {
                "o": "plone.app.querystring.operation.date.lessThanRelativeDate",
                "v": now,
                "i": "chiusura_procedimento_bando",
            },
        ),
    }

    for i in query:
        if i.get("i", "") == "bando_state":
            item = i

            for value in i.get("v", []):
                operator = state_operators.get(value, None)

                if operator:
                    query_extender.extend(operator)

    if item:
        query.remove(item)
        query.extend(query_extender)

    return query
