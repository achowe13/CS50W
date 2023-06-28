from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_entry/', views.new_entry, name='new_entry'),
    path('wiki/<str:title>', views.Entry, name='Entry'),
    path('search/', views.search, name='search'),
    path('error/', views.Error, name='Error'),
    path('random/', views.random_page, name='random_page'),
    path('edit/<str:title>', views.Edit, name='Edit')
]
