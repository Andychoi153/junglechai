from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^not_found$', views.not_found, name='not_found'),
    url(r'^delete', views.delete, name='delete'),

]

