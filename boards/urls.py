from django.urls import path
from . import views

urlpatterns = [
    path('administration/', views.administration, name='administration'),
    path('board-history/', views.board_history, name='board_history'),
    path('get-decanal-members/', views.get_decanal_members, name='get_decanal_members'),
    path('get-parish-members/', views.get_parish_members, name='get_parish_members'),
    path('get-history-decanal-members/', views.get_history_decanal_members, name='get_history_decanal_members'),
    path('get-history-parish-members/', views.get_history_parish_members, name='get_history_parish_members'),
]
