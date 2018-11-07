# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class ExchangeCurrencies(models.Model):
    """
        Model to save the currencies that we are checking
    """

    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    currencies = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = _('Exchange Currencies Pair')
        verbose_name_plural = _('Exchange Currencies Pairs')

    def __unicode__(self):
        return self.currencies

    def last_price(self):
        try:
            return self.exchangerates_set.order_by('created').last().price
        except AttributeError:
            return 0


class ExchangeRates(models.Model):
    """
        Model to save the currencies exchange rates
    """

    created = models.DateTimeField(auto_now_add=True)

    currencies = models.ForeignKey(ExchangeCurrencies)
    price = models.FloatField()

    class Meta:
        verbose_name = _('Exchange rate')
        verbose_name_plural = _('Exchange rates')

    def __unicode__(self):
        return u'%s : %s - %s' % (self.currencies, self.created, self.price)

