from django.urls import path
from . import views

urlpatterns = [
    path('', views.history_list, name='histories'),
    path('<int:history_id>/', views.history_detail, name='history_detail'),
]
