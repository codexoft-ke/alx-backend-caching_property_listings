from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('no-page-cache/', views.property_list_no_page_cache, name='property_list_no_page_cache'),
]
