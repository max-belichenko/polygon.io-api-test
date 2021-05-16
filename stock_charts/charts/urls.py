from django.urls import path

from charts.views import *


urlpatterns = [
    path('', charts_view, name='charts'),
]
