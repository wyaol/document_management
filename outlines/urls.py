from django.urls import path

from .api import *

urlpatterns = [
    path('test', test),
    path('ready', get_one_ready_outline),
]
