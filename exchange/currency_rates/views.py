# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.edit import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

import models
from utilities import check_exchange_currencies
# Create your views here.


class ExchangeRates(View):
    """
        Home page where exchange rates are shown
    """
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        context = dict()

        context['exchange_rates'] = models.ExchangeCurrencies.objects.filter(active=True)

        return render(request, self.template_name, context)


class AddExchangeCurrency(LoginRequiredMixin, View):
    """
        Page for user to add new currency pairs to monitor
    """

    template_name = "new_exchange.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        first = request.POST.get("first_currency", "").lower()
        second = request.POST.get("second_currency", "").lower()

        if first and second:
            try:
                exch_curr = models.ExchangeCurrencies.objects.get(currencies='%s-%s' % (first, second))
                messages.error(request, _('This exchange currencies are already monitored.'), extra_tags='danger')
            except ObjectDoesNotExist:
                currencies = '%s-%s' % (first, second)
                if check_exchange_currencies(currencies):
                    models.ExchangeCurrencies.objects.create(currencies=currencies)
                    messages.success(request, _('Currencies ware added.'), extra_tags='success')
                    return redirect('home')
                else:
                    messages.success(request, _('Invalid currencies.'), extra_tags='danger')

        return render(request, self.template_name)
