from datetime import datetime

from django.conf import settings
from django.db import models


class Ticker(models.Model):
    symbol = models.CharField(verbose_name='The ticker symbol of the stock/equity', max_length=10, db_index=True)

    class Meta:
        ordering = ('symbol',)
        verbose_name = 'The ticker symbol of the stock/equity'
        verbose_name_plural = 'The ticker symbols of the stock/equity'

    def __str__(self):
        return str(self.symbol)


class Bar(models.Model):
    ticker = models.ForeignKey(verbose_name='The exchange symbol that this item is traded under', to=Ticker, on_delete=models.CASCADE)
    timespan = models.CharField(verbose_name='The size of the time window', max_length=255, choices=settings.CHART_SETTINGS['TIMESPAN_CHOICE'], )
    multiplier = models.IntegerField(verbose_name='The size of the timespan multiplier', )

    timestamp = models.BigIntegerField(verbose_name='The Unix Msec timestamp for the start of the aggregate window')
    number_of_transactions = models.IntegerField(verbose_name='The number of transactions in the aggregate window')

    open_price = models.DecimalField(verbose_name='The open price for the symbol in the given time period', max_digits=14, decimal_places=4)
    highest_price = models.DecimalField(verbose_name='The highest price for the symbol in the given time period', max_digits=14, decimal_places=4)
    lowest_price = models.DecimalField(verbose_name='The lowest price for the symbol in the given time period', max_digits=14, decimal_places=4)
    close_price = models.DecimalField(verbose_name='The close price for the symbol in the given time period', max_digits=14, decimal_places=4)

    trading_volume = models.BigIntegerField(verbose_name='The trading volume of the symbol in the given time period')
    volume_weighted_average_price = models.DecimalField(verbose_name='The volume weighted average price', max_digits=14, decimal_places=4)

    @property
    def dt(self):
        """Converts Unix Msec timestamp to formatted date """
        if self.timestamp:
            try:
                seconds = int(self.timestamp / 1000)
                dt = datetime.fromtimestamp(seconds).strftime('%Y-%m-%d %H:%M')
            except (TypeError, ValueError):
                dt = None
        else:
            dt = None

        return dt

    class Meta:
        ordering = ('ticker', 'timestamp', )
        verbose_name = 'Aggregate bar for a stock'
        verbose_name_plural = 'Aggregate bars for a stock'

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'ticker',
                    'timespan',
                    'multiplier',
                    'timestamp',
                ],
                name="unique_bar"
            )
        ]

    def __str__(self):
        return f'[{self.ticker}] {self.dt}: ' \
               f'o={self.open_price}\th={self.highest_price}\tl={self.lowest_price}\tc={self.close_price}'
