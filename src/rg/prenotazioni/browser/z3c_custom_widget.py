from z3c.form import interfaces
from z3c.form.widget import FieldWidget
from z3c.form.browser.radio import RadioWidget
from z3c.form.interfaces import IRadioWidget
from Products.Five.browser.metaconfigure import ViewMixinForTemplates
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile as VPTF
from z3c.form.widget import FieldWidget
from Products.Five.browser import BrowserView
from plone.memoize.view import memoize
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from plone import api
from zope.i18n import translate
from z3c.form import interfaces, util
import zope


class ICustomRadioFieldWidget(interfaces.IFieldWidget):
    """ """


class ICustomRadioWidget(IRadioWidget):
    """ """


class RenderWidget(ViewMixinForTemplates, BrowserView):
    index = VPTF('templates/tipology_radio_widget.pt')

    @property
    @memoize
    def prenotazione_add(self):
        ''' Returns the prenotazioni_context_state view.

        Everyone should know about this!
        '''
        return api.content.get_view('prenotazione_add',
                                    self.context.context.aq_inner,
                                    self.request).\
            form(
                self.context.context.aq_inner,
                self.request
            )

    @property
    @memoize
    def vocabulary(self):
        voc_name = self.context.field.vocabularyName
        if voc_name:
            return getUtility(IVocabularyFactory, name=voc_name)(
                self.context.context.aq_inner
            )

    @property
    @memoize
    def tipologies_bookability(self):
        ''' Get tipology bookability
        '''
        booking_date = self.prenotazione_add.booking_DateTime.asdatetime()
        prenotazioni = self.prenotazione_add.prenotazioni
        return prenotazioni.tipologies_bookability(booking_date)

    @property
    @memoize
    def unbookable_items(self):
        ''' Get tipology bookability
        '''
        keys = sorted(self.tipologies_bookability['unbookable'])
        keys = [key.decode('utf8') for key in keys]
        return [self.vocabulary.getTerm(key) for key in keys if key in self.context.terms]



@zope.interface.implementer_only(ICustomRadioWidget)
class CustomRadioWidget(RadioWidget):
    """ """
    @property
    @memoize
    def prenotazione_add(self):
        ''' Returns the prenotazioni_context_state view.

        Everyone should know about this!
        '''
        return api.content.get_view(
            'prenotazione_add',
            self.context,
            self.request).form(
                self.context,
                self.request
        )

    @property
    @memoize
    def vocabulary(self):
        voc_name = self.field.vocabularyName
        if voc_name:
            return getUtility(IVocabularyFactory, name=voc_name)(
                self.context
            )

    @property
    @memoize
    def tipologies_bookability(self):
        ''' Get tipology bookability
        '''
        booking_date = self.prenotazione_add.booking_DateTime.asdatetime()
        prenotazioni = self.prenotazione_add.prenotazioni
        return prenotazioni.tipologies_bookability(booking_date)

    @property
    @memoize
    def bookable_items(self):
        ''' Get tipology bookability
        '''
        keys = sorted(self.tipologies_bookability['bookable'])
        keys = [key.decode('utf8') for key in keys]
        return [self.vocabulary.getTerm(key) for key in keys if key in self.terms]

    @property
    def items(self):

        bookable = self.bookable_items

        if not bookable:
            return
        for count, term in enumerate(self.bookable_items):
            checked = self.isChecked(term)
            id = '%s-%i' % (self.id, count)
            if zope.schema.interfaces.ITitledTokenizedTerm.providedBy(term):
                label = translate(term.title, context=self.request,
                                  default=term.title)
            else:
                label = util.toUnicode(term.value)
            yield {'id': id, 'name': self.name, 'value': term.token,
                   'label': label, 'checked': checked}


@zope.component.adapter(zope.schema.interfaces.IField, interfaces.IFormLayer)
@zope.interface.implementer(ICustomRadioFieldWidget)
def CustomRadioFieldWidget(field, request):
    """IFieldWidget factory for RadioWidget."""
    return FieldWidget(field, CustomRadioWidget(request))