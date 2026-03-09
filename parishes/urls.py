from django.urls import path
from . import views

urlpatterns = [
    path('', views.parish_list, name='parishes'),
    path('doyenne/<int:doyenne_id>/', views.doyenne_detail, name='doyenne_detail'),
]
