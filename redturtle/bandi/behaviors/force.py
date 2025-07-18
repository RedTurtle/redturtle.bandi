from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from redturtle.bandi import _
from redturtle.bandi.config import STATES
from redturtle.bandi.interfaces.bando import IBando
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IFormFieldProvider)
class IForcedState(model.Schema):
    """Marker inteerface for content type Bando"""

    forced_state = schema.Choice(
        title=_("stato_avanzamento_label", default="Stato di avanzamento"),
        description=_(
            "stato_avanzamento_help",
            default=(
                "Indica lo stato di avanzamento. Se il campo esiste, viene "
                "utilizzato per determinare lo stato del bando. Se non esiste, "
                "viene utilizzato il metodo di base per cui lo stato del bando "
                "è determinato dalle date di inizio e fine."
            ),
        ),
        required=False,
        vocabulary=SimpleVocabulary(
            [SimpleTerm(state, state, STATES[state]["label"]) for state in STATES]
        ),
    )


@implementer(IBando)
@adapter(IDexterityContent)
class ForcedState(object):
    """Bando adapter"""

    def __init__(self, context):
        self.context = context
