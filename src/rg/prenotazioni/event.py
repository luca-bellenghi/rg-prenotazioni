# -*- coding: utf-8 -*-
from rg.prenotazioni.adapters.booker import IBooker


def reallocate_gate(obj):
    '''
    We have to reallocate the gate for this object

    Skip this step if we have a form.gate parameter in the request
    '''
    context = obj.object

    if context.REQUEST.form.get('form.gate', '') and context.getGate():
        return

    container = context.getPrenotazioniFolder()
    booking_date = context.getData_prenotazione()
    new_gate = IBooker(container).get_available_gate(booking_date)
    context.setGate(new_gate)


def reallocate_container(obj):
    '''
    If we moved Prenotazione to a new week we should move it
    '''
    container = obj.object.getPrenotazioniFolder()
    IBooker(container).fix_container(obj.object)
