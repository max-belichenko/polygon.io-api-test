from django import forms
from django.conf import settings


class SymbolSelectionForm(forms.Form):
    """
    Form to set properties for chart display
    """
    symbol = forms.ChoiceField(
        choices=(
            ('MSFT', 'MSFT'),
            ('COST', 'COST'),
            ('EBAY', 'EBAY'),
            ('WMT', 'WMT'),
            ('GOOGL', 'GOOGL'),
        )
    )
    timespan = forms.ChoiceField(choices=settings.CHART_SETTINGS['TIMESPAN_CHOICE'])
    timespan_multiplier = forms.IntegerField(min_value=1)
    from_date = forms.DateField()
    to_date = forms.DateField()
    limit = forms.IntegerField(min_value=1, max_value=50000)
