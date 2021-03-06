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
from collective.z3cform.datagridfield import BlockDataGridFieldFactory


class ISettimanaTipoRow(model.Schema):

    giorno = schema.TextLine(
        title=_(u"Giorno"),
        required=False
    )
    inizio_m = schema.Choice(
        title=_(u"Ora inizio mattina"),
        vocabulary="rg.prenotazioni.VocOreInizio",
        required=False,
    )
    end_m = schema.Choice(
        title=_(u"Ora fine mattina"),
        vocabulary="rg.prenotazioni.VocOreInizio",
        required=False,
    )

    inizio_p = schema.Choice(
        title=_(u"Ora inizio pomeriggio"),
        vocabulary="rg.prenotazioni.VocOreInizio",
        required=False,
    )

    end_p = schema.Choice(
        title=_(u"Ora fine pomeriggio"),
        vocabulary="rg.prenotazioni.VocOreInizio",
        required=False,
    )


class ITipologiaRow(Interface):
    name = schema.TextLine(
        title=_(u"Typology name"),
        required=True,
    )
    duration = schema.Choice(
        title=_(u"Duration value"),
        required=True,
        vocabulary="rg.prenotazioni.VocDurataIncontro"
    )


class IPrenotazioniFolder(model.Schema):
    """ Marker interface and Dexterity Python Schema for PrenotazioniFolder
    """

    dexteritytextindexer.searchable('descriptionAgenda')
    descriptionAgenda = RichText(
        required=False,
        title=_(u'Descrizione Agenda', default=u'Descrizione Agenda'),
        description=(u"Inserire il testo di presentazione "
                     u"dell'agenda corrente"),

    )

    daData = schema.Date(
        title=_(u'Data inizio validità'),
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
        ),
        default = [
            {'giorno': u'Lunedì', 'inizio_m': None, 'inizio_p': None, 'end_m': None, 'end_p': None},
            {'giorno': u'Martedì', 'inizio_m': None, 'inizio_p': None, 'end_m': None, 'end_p': None},
            {'giorno': u'Mercoledì', 'inizio_m': None, 'inizio_p': None, 'end_m': None, 'end_p': None},
            {'giorno': u'Giovedì', 'inizio_m': None, 'inizio_p': None, 'end_m': None, 'end_p': None},
            {'giorno': u'Venerdì', 'inizio_m': None, 'inizio_p': None, 'end_m': None, 'end_p': None},
            {'giorno': u'Sabato', 'inizio_m': None, 'inizio_p': None, 'end_m': None, 'end_p': None},
            {'giorno': u'Domenica', 'inizio_m': None, 'inizio_p': None, 'end_m': None, 'end_p': None},
        ]
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
        required=False,
        value_type=schema.TextLine(),
        default=[]
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

    tipologia = schema.List(
        title=_(u"Tipologie di richiesta"),
        description=_('tipologia_help',
                      default=u"Put booking types there (one per line).\n"
                              u"If you do not provide this field, "
                              u"not type selection will be available"),
        value_type=DictRow(
            schema=ITipologiaRow
        )

    )
    form.widget(tipologia=DataGridFieldFactory)

    gates = schema.List(
        title=_('gates_label', "Gates"),
        description=_('gates_help',
                      default=u"Put gates here (one per line). "
                              u"If you do not fill this field, "
                              u"one gate is assumed"),
        required=False,
        value_type=schema.TextLine(),
        default=[]
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
        value_type=schema.TextLine(),
        default=[]
    )

    # XXX validate email
    email_responsabile = schema.TextLine(
        title=_(u'Email del responsabile'),
        description=_(u"Inserisci l'indirizzo email del responsabile "
                      "delle prenotazioni"),
        required=False,
    )



@implementer(IPrenotazioniFolder)
class PrenotazioniFolder(Container):
    """
    """

    def getDescriptionAgenda(self):
        return self.descriptionAgenda

    def getSettimana_tipo(self):
        return self.settimana_tipo

    def getGates(self):
        return self.gates

    def getUnavailable_gates(self):
        return self.unavailable_gates

    def getDaData(self):
        return self.daData

    def getAData(self):
        return self.aData

    def getTipologia(self):
        return self.tipologia

    def getFestivi(self):
        return self.festivi

    def getFutureDays(self):
        return self.futureDays

    def getNotBeforeDays(self):
        return self.notBeforeDays
