# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone import api
from plone.memoize.view import memoize
from rg.prenotazioni.config import MIN_IN_DAY
from rg.prenotazioni.utilities.urls import urlify


class PrenotazioneView(BrowserView):
    """View for Prenotazione"""

    @property
    @memoize
    def prenotazioni_folder(self):
        ''' The parent prenotazioni folder
        '''
        return self.context.getPrenotazioniFolder()

    @property
    @memoize
    def prenotazioni(self):
        ''' The context state of the parent prenotazioni folder
        '''
        return api.content.get_view('prenotazioni_context_state',
                                    self.prenotazioni_folder,
                                    self.request)

    @property
    def booking_date(self):
        ''' The parent prenotazioni folder
        '''
        return self.context.getData_prenotazione()

    @property
    @memoize
    def back_url(self):
        ''' Go back parent prenotazioni folder in the right day
        '''
        booking_date = self.booking_date
        target = self.prenotazioni_folder.absolute_url()
        if booking_date:
            qs = {'data': booking_date.strftime('%d/%m/%Y')}
            target = urlify(target, params=qs)
        return target

    @property
    @memoize
    def move_url(self):
        ''' move this booking visiting this url
        '''
        booking_date = self.booking_date
        target = '/'.join((self.context.absolute_url(), 'prenotazione_move'))
        if booking_date:
            qs = {'data': booking_date.strftime('%d/%m/%Y')}
            target = urlify(target, params=qs)
        return target

    @property
    @memoize
    def review_state(self):
        ''' The review_state of this object
        '''
        return self.prenotazioni.get_state(self.context)


class ResetDuration(PrenotazioneView):
    ''' Reset data scadenza prenotazione: sometime is needed :p
    '''
    def reset_duration(self):
        ''' Reset the duration for this booking object

        Tries to get the duration information from the request,
        fallbacks to the tipology, and finally to 1 minute
        '''
        tipology = self.context.getTipologia_prenotazione()
        duration = self.request.form.get('duration', 0)
        if not duration:
            duration = self.prenotazioni.get_tipology_duration(tipology)
        duration = (float(duration) / MIN_IN_DAY)
        self.context.setData_scadenza(self.booking_date + duration)

    def __call__(self):
        ''' Reset the dates
        '''
        self.reset_duration()
        return self.request.response.redirect(self.back_url)
