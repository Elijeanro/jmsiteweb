from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='events'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
]
