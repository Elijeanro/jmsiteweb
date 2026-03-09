from django.urls import path
from . import views

urlpatterns = [
    path('', views.faustine_list, name='faustine'),
]
