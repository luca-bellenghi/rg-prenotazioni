# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from plone.autoform import directives as form
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer, Interface
from collective import dexteritytextindexer
from rg.prenotazioni import _
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow


class ISettimanaTipoRow(Interface):
    giorno = schema.TextLine(
        title=_("ciccia")
    )
    inizio_m = schema.Choice(
        title=_(u"Ora inizio mattina"),
        vocabulary="vocOreInizio",
    )
    fine_m = schema.Choice(
        title=_(u"Ora fine mattina"),
        vocabulary="vocOreInizio",
    )

    inizio_p = schema.Choice(
        title=_(u"Ora inizio pomeriggio"),
        vocabulary="vocOreInizio",
    )

    fine_p = schema.Choice(
        title=_(u"Ora fine pomeriggio"),
        vocabulary="vocOreInizio",
    )



class IPrenotazioniFolder(model.Schema):
    """ Marker interface and Dexterity Python Schema for PrenotazioniFolder
    """

    dexteritytextindexer.searchable('descriptionAgenda')
    descriptionAgenda = RichText(
        required=False,
        title=_(u'Descrizione Agenda', default=u''),
        description=(u"Inserire il testo di presentazione "
                     u"dell'agenda corrente"),

    )

    daData = schema.Date(
        title=_(u'Data inizio validità'),
        description=_(u""),
    )

    aData = schema.Date(
        title=_(u'Data fine validità'),
        description=_("aData_help",
                      default=u"Leave empty, and this Booking Folder will never expire"),  # noqa
        required=False
    )

    settimana_tipo = schema.List(
        title=_(u"Settimana Tipo"),
        description=_(u"Indicare la composizione della settimana tipo"),
        required=True,
        value_type=DictRow(
            schema=ISettimanaTipoRow
        )
    )
    form.widget(settimana_tipo=DataGridFieldFactory)

    festivi = schema.List(
        title=_(u"Giorni festivi"),
        description=_(
            'help_holidays',
            u"Indicare i giorni festivi (uno per riga) "
            u"nel formato GG/MM/AAAA. Al posto dell'anno puoi mettere un "
            u"asterisco per indicare un evento che ricorre annualmente."
        ),
        required=False
    )

    futureDays = schema.Int(
        default=0,
        title=_(u'Max days in the future'),
        description=_('futureDays',
                      default=u"Limit booking in the future to an amount "
                              u"of days in the future starting from "
                              u"the current day. \n"
                              u"Keep 0 to give no limits."),
    )

    notBeforeDays = schema.Int(
        default=2,
        title=_(u'Days booking is not allowed before'),
        description=_('notBeforeDays',
                      default=u"Booking is not allowed before the amount "
                              u"of days specified. \n"
                              u"Keep 0 to give no limits."),
    )

    # tipologia

    gates = schema.List(
        title=_('gates_label', "Gates"),
        description=_('gates_help',
                      default=u"Put gates here (one per line). "
                              u"If you do not fill this field, "
                              u"one gate is assumed"),
        required=False,
    )

    unavailable_gates = schema.List(
        title=_('unavailable_gates_label', "Unavailable gates"),
        description=_('unavailable_gates_help',
                      default=u'Add a gate here (one per line) if, '
                              u'for some reason, '
                              u'it is not be available.'
                              u'The specified gate will not be taken in to '  # noqa
                              u'account for slot allocation. '
                              u'Each line should match a corresponding '
                              u'line in the "Gates" field'
                          ),
        required=False,
    )

    email_responsabile = schema.TextLine(
        title=_(u'Email del responsabile'),
        description=_(u"Inserisci l'indirizzo email del responsabile "
                      "delle prenotazioni"),
    )



@implementer(IPrenotazioniFolder)
class PrenotazioniFolder(Container):
    """
    """
