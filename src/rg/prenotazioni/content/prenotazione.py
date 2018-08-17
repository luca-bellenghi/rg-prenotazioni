# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer
from rg.prenotazioni import _
from collective import dexteritytextindexer


class IPrenotazione(model.Schema):
    """ Marker interface and Dexterity Python Schema for Prenotazione
    """

    dexteritytextindexer.searchable('email')
    # XXX validator
    email = schema.TextLine(
        title=_(u"email"),
    )
    dexteritytextindexer.searchable('telefono')
    telefono = schema.TextLine(
        title=_(u"Phone number"),
    )
    dexteritytextindexer.searchable('mobile')
    mobile = schema.TextLine(
        title=_("mobile", u"Mobile number"),
    )

    dexteritytextindexer.searchable('tipologia_prenotazione')
    tipologia_prenotazione = schema.Choice(
        title=_(u"booking tipology"),
        vocabulary='rg.prenotazioni.tipologies',
    )

    # XXX visibile solo in view
    data_prenotazione = schema.Datetime(
        title=_(u'Booking date'),
        required=True,
    )

    dexteritytextindexer.searchable('azienda')
    azienda = schema.TextLine(
        title=_(u"Company"),
        description=_(u"Inserisci la denominazione dell'azienda "
                      u"del richiedente"),
    )

    dexteritytextindexer.searchable('gate')
    gate = schema.TextLine(
        title=_(u"Gate"),
        description=_(u"Sportello a cui presentarsi"),
    )

    data_scadenza = schema.Datetime(
        title=_(u'Expiration date booking'),
        required=True,
    )

    dexteritytextindexer.searchable('staff_notes')
    staff_notes = schema.Text(
        required=False,
        title=_('staff_notes_label', u"Staff notes")
    )


@implementer(IPrenotazione)
class Prenotazione(Item):
    """
    """
