from django.conf.urls import url

from base.views import collection_view, index, db_view, get_csv

urlpatterns = [
    url(r'^$', index),
    url(r'^(?P<db_name>[\w\-.]+)/$', db_view, name='db_view'),
    url(r'^(?P<db_name>[\w\-.]+)/(?P<collection_name>[\w\-.]+)/$', collection_view, name='collection_view'),
    url(r'^(?P<db_name>[\w\-.]+)/(?P<collection_name>[\w\-.]+)/csv$', get_csv, name='get_csv'),
]
