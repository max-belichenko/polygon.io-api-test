from datetime import datetime

import requests
import urllib

from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from charts.forms import SymbolSelectionForm

from charts.models import Bar, Ticker


def get_data_from_api(ticker: str, timespan: str, timespan_multiplier: int, from_date: datetime.date, to_date: datetime.date, limit: int):
    """
    Sends GET request to Polygon.io API to get Aggregates (Bars) by given parameters.

    :param ticker:  The ticker symbol of the stock/equity
    :param timespan:    The size of the time window ('minute', 'hour', 'day', 'week', 'month', 'quarter', 'year')
    :param timespan_multiplier: The size of the timespan multiplier.
    :param from_date:   The start of the aggregate time window
    :param to_date:     The end of the aggregate time window.
    :param limit:
    :return:
    """
    base_url = settings.CHART_SETTINGS['API base URL']
    params = {
        'apiKey': settings.CHART_SETTINGS['apiKey'],
        'unadjusted': settings.CHART_SETTINGS['unadjusted'],
        'sort': settings.CHART_SETTINGS['sort'],
        'limit': limit,
    }

    # Convert date to ISO format
    from_date_str = from_date.strftime("%Y-%m-%d")
    to_date_str = to_date.strftime("%Y-%m-%d")

    # Assemble full URL
    url = urllib.parse.urljoin(base_url,
                               f'{ticker}/range/{timespan_multiplier}/{timespan}/{from_date_str}/{to_date_str}')

    # Send request
    response = requests.get(url=url, params=params)

    return response


def save_charts_data(ticker, timespan, timespan_multiplier, results):
    """
    Saves charts received from Polygon.io API to database.

    :param ticker:
    :param timespan:
    :param timespan_multiplier:
    :param results: List of chart values
    :return:    List of Bar instances
    """
    result_objects = []

    # Get Ticker instance with given symbol, or create it if one does not exist
    ticker_instance, is_created = Ticker.objects.get_or_create(symbol=ticker)

    # Map results to Bar model fields
    if results:
        charts = [{
            'ticker': ticker_instance,
            'timespan': timespan,
            'multiplier': timespan_multiplier,
            'timestamp': item.get('t'),
            'number_of_transactions': item.get('n'),
            'open_price': item.get('o'),
            'highest_price': item.get('h'),
            'lowest_price': item.get('l'),
            'close_price': item.get('c'),
            'trading_volume': item.get('v'),
            'volume_weighted_average_price': item.get('vw'),
        } for item in results]
    else:
        charts = []

    # Make ORM objects from mapped fields
    bars = [Bar(**item) for item in charts]

    # Check for already existing bars in database
    new_bars = []
    while bars:
        bar = bars.pop()

        try:
            existing_bar = Bar.objects.get(
                    ticker=bar.ticker,
                    timespan=bar.timespan,
                    multiplier=bar.multiplier,
                    timestamp=bar.timestamp,
            )

        except Bar.DoesNotExist:
            existing_bar = None

        if not existing_bar:
            # If Bar does not exist, it will be created
            new_bars.append(bar)
        else:
            # If Bar already exist, append it to result directly
            result_objects.append(existing_bar)

    # Create bulk of objects in database with single SQL query
    try:
        result_objects.extend(Bar.objects.bulk_create(new_bars))
    except IntegrityError as e:
        raise IntegrityError('Unexpected DB error:', e)

    return result_objects


def get_charts(ticker, timespan, timespan_multiplier, from_date, to_date, limit=None):
    """
    Get charts data from database.

    :param limit:
    :param ticker:
    :param timespan:
    :param timespan_multiplier:
    :param from_date:
    :param to_date:
    :return:
    """
    # Get Ticker object
    ticker_object = Ticker.objects.get(symbol=ticker)

    # Convert date to Unix MSec timestamp
    from_date_timestamp = datetime.combine(from_date, datetime.min.time()).timestamp() * 1000
    to_date_timestamp = datetime.combine(to_date, datetime.max.time()).timestamp() * 1000

    data = Bar.objects.filter(
        ticker=ticker_object,
        timespan=timespan,
        multiplier=timespan_multiplier,
        timestamp__gte=from_date_timestamp,
        timestamp__lte=to_date_timestamp,
    )

    if limit:
        return data[:limit]
    else:
        return data


def charts_view(request):
    if request.method == 'POST':
        # Create form and fill it with previously inputted data
        form = SymbolSelectionForm(data=request.POST)

        if form.is_valid():     # If all fields are filled in correctly
            # Get fields' values
            ticker = form.cleaned_data['symbol']
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            timespan = form.cleaned_data['timespan']
            timespan_multiplier = form.cleaned_data['timespan_multiplier']
            limit = form.cleaned_data['limit']

            # Send request to Polygin.io API
            response = get_data_from_api(
                ticker=ticker,
                from_date=from_date,
                to_date=to_date,
                timespan=timespan,
                timespan_multiplier=timespan_multiplier,
                limit=limit,
            )

            if response.status_code == 200:     # 200 OK
                # Convert response to Python Dict
                try:
                    data = response.json()
                except ValueError:
                    data = {}

                # Save new bars to database
                save_charts_data(
                    ticker=data.get('ticker'),
                    timespan=timespan,
                    timespan_multiplier=timespan_multiplier,
                    results=data.get('results'),
                )

                # Get Bars from DB by given parameters
                data = get_charts(
                    ticker=ticker,
                    timespan=timespan,
                    timespan_multiplier=timespan_multiplier,
                    from_date=from_date,
                    to_date=to_date,
                    limit=limit,
                )

                return render(
                    request=request,
                    template_name='charts/charts.html',
                    context={
                        'form': form,
                        'data': data,
                    },
                )

            else:
                return HttpResponse(f'Error code from Polygon.io: {response.status_code}')

    else:
        form = SymbolSelectionForm(initial={'timespan': 'minute', 'timespan_multiplier': 1, 'limit': 120})

    return render(
        request=request,
        template_name='charts/charts.html',
        context={'form': form},
    )
