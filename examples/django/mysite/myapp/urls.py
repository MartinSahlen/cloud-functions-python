from django.conf.urls import url
from .views import data_view

urlpatterns = [
    url(r'^data', data_view),
    ]
