from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    path('events/', views.manage_events, name='manage_events'),
    path('events/add/', views.add_event, name='add_event'),
    path('events/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('documents/', views.manage_documents, name='manage_documents'),
    path('documents/add/', views.add_document, name='add_document'),
    path('documents/edit/<int:document_id>/', views.edit_document, name='edit_document'),
    path('documents/delete/<int:document_id>/', views.delete_document, name='delete_document'),
    
    path('faustine/', views.manage_faustine, name='manage_faustine'),
    path('faustine/add/', views.add_faustine_content, name='add_faustine_content'),
    path('faustine/edit/<int:content_id>/', views.edit_faustine_content, name='edit_faustine_content'),
    path('faustine/delete/<int:content_id>/', views.delete_faustine_content, name='delete_faustine_content'),
    
    # Gestion des Historiques
    path('histories/', views.manage_histories, name='manage_histories'),
    path('histories/add/', views.add_history, name='add_history'),
    path('histories/edit/<int:history_id>/', views.edit_history, name='edit_history'),
    path('histories/delete/<int:history_id>/', views.delete_history, name='delete_history'),

    # Gestion des EntrÃ©es Historiques
    path('histories/<int:history_id>/entries/', views.manage_history_entries, name='manage_history_entries'),
    path('histories/<int:history_id>/entries/add/', views.add_history_entry, name='add_history_entry'),
    path('histories/<int:history_id>/entries/edit/<int:entry_id>/', views.edit_history_entry, name='edit_history_entry'),
    path('histories/<int:history_id>/entries/delete/<int:entry_id>/', views.delete_history_entry, name='delete_history_entry'),
    
    # Gestion des DoyennÃ©s
    path('doyennes/', views.manage_doyennes, name='manage_doyennes'),
    path('doyennes/add/', views.add_doyenne, name='add_doyenne'),
    path('doyennes/edit/<int:doyenne_id>/', views.edit_doyenne, name='edit_doyenne'),
    path('doyennes/delete/<int:doyenne_id>/', views.delete_doyenne, name='delete_doyenne'),

    # Gestion des Paroisses
    path('parishes/', views.manage_parishes, name='manage_parishes'),
    path('parishes/add/', views.add_parish, name='add_parish'),
    path('parishes/edit/<int:parish_id>/', views.edit_parish, name='edit_parish'),
    path('parishes/delete/<int:parish_id>/', views.delete_parish, name='delete_parish'),

    # Gestion des Types de Bureaux
    path('boards/types/', views.manage_board_types, name='manage_board_types'),
    path('boards/types/add/', views.add_board_type, name='add_board_type'),
    path('boards/types/<int:board_type_id>/edit/', views.edit_board_type, name='edit_board_type'),
    path('boards/types/<int:board_type_id>/delete/', views.delete_board_type, name='delete_board_type'),

    # Gestion des Postes
    path('boards/positions/', views.manage_member_positions, name='manage_member_positions'),
    path('boards/positions/add/', views.add_member_position, name='add_member_position'),
    path('boards/positions/<int:position_id>/edit/', views.edit_member_position, name='edit_member_position'),
    path('boards/positions/<int:position_id>/delete/', views.delete_member_position, name='delete_member_position'),

    # Gestion des Membres
    path('boards/members/', views.manage_members, name='manage_members'),
    path('boards/members/add/', views.add_member, name='add_member'),
    path('boards/members/<int:member_id>/edit/', views.edit_member, name='edit_member'),
    path('boards/members/<int:member_id>/delete/', views.delete_member, name='delete_member'),

    # Gestion des Mandats
    path('boards/mandates/', views.manage_mandates, name='manage_mandates'),
    path('boards/mandates/add/', views.add_mandate, name='add_mandate'),
    path('boards/mandates/<int:mandate_id>/edit/', views.edit_mandate, name='edit_mandate'),
    path('boards/mandates/<int:mandate_id>/delete/', views.delete_mandate, name='delete_mandate'),

    # Gestion des Bureaux
    path('boards/', views.manage_boards, name='manage_boards'),
    path('boards/add/', views.add_board, name='add_board'),
    path('boards/<int:board_id>/edit/', views.edit_board, name='edit_board'),
    path('boards/<int:board_id>/delete/', views.delete_board, name='delete_board'),

    # Gestion des Memberships
    path('boards/memberships/', views.manage_board_memberships, name='manage_board_memberships'),
    path('boards/memberships/add/', views.add_board_membership, name='add_board_membership'),
    path('boards/memberships/<int:membership_id>/edit/', views.edit_board_membership, name='edit_board_membership'),
    path('boards/memberships/<int:membership_id>/delete/', views.delete_board_membership, name='delete_board_membership'),    # Gestion des Programmes
    path('programs/', views.manage_programs, name='manage_programs'),
    path('programs/add/', views.add_program, name='add_program'),
    path('programs/edit/<int:program_id>/', views.edit_program, name='edit_program'),
    path('programs/delete/<int:program_id>/', views.delete_program, name='delete_program'),

    path('programs/files/', views.manage_program_content_file, name='manage_program_content_file'),
    path('programs/files/add/', views.add_program_content_file, name='add_program_content_file'),
    path('programs/files/edit/<int:file_id>/', views.edit_program_content_file, name='edit_program_content_file'),
    path('programs/files/delete/<int:file_id>/', views.delete_program_content_file, name='delete_program_content_file'),

    path('programs/schedules/', views.manage_program_content_schedule, name='manage_program_content_schedule'),
    path('programs/schedules/add/', views.add_program_content_schedule, name='add_program_content_schedule'),
    path('programs/schedules/edit/<int:schedule_id>/', views.edit_program_content_schedule, name='edit_program_content_schedule'),
    path('programs/schedules/delete/<int:schedule_id>/', views.delete_program_content_schedule, name='delete_program_content_schedule'),

    path('programs/schedules/items/', views.manage_program_content_schedule_list, name='manage_program_content_schedule_list'),
    path('programs/schedules/items/add/', views.add_program_content_schedule_list, name='add_program_content_schedule_list'),
    path('programs/schedules/items/edit/<int:item_id>/', views.edit_program_content_schedule_list, name='edit_program_content_schedule_list'),
    path('programs/schedules/items/delete/<int:item_id>/', views.delete_program_content_schedule_list, name='delete_program_content_schedule_list'),
    # Autres URLs
    path('events/delete-image/<int:event_id>/<int:image_id>/', views.delete_event_image, name='delete_event_image'),
]
