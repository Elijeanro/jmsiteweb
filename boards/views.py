from datetime import date

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Board, BoardMembership, Member, Mandate, Doyenne, Parish

def administration(request):
    """
    Affiche la page d'administration des bureaux.
    Par défaut, affiche les membres du bureau diocésain actuel.
    """
    # Récupérer le bureau diocésain actuel (celui sans date de fin ou avec la date de fin la plus récente)
    diocesan_board = Board.objects.filter(
        board_type='diocesan',
        is_current=True
    ).order_by('-end_date').first()

    diocesan_members = []

    if diocesan_board:
        diocesan_members = BoardMembership.objects.filter(
            board=diocesan_board,
            mandate__is_current=True
        ).select_related('member', 'position').order_by('position__order')

    # Récupérer tous les doyennés et paroisses pour les filtres
    doyennes = Doyenne.objects.all().order_by('name')
    parishes = Parish.objects.all().order_by('name')

    context = {
        'diocesan_members': diocesan_members,
        'doyennes': doyennes,
        'parishes': parishes,
        'current_board': diocesan_board,
    }

    return render(request, 'boards/administration.html', context)

def board_history(request):
    """
    Affiche l'historique des bureaux.
    Par défaut, affiche tous les bureaux diocésains.
    """
    # Récupérer tous les bureaux diocésains pour l'historique
    diocesan_boards = Board.objects.filter(
        board_type='diocesan'
    ).prefetch_related('members').order_by('-start_date')

    # Récupérer tous les doyennés et paroisses pour les filtres
    doyennes = Doyenne.objects.all().order_by('name')
    parishes = Parish.objects.all().order_by('name')

    context = {
        'diocesan_boards': diocesan_boards,
        'doyennes': doyennes,
        'parishes': parishes,
    }

    return render(request, 'board_history.html', context)

def get_decanal_members(request):
    """
    Retourne les membres du bureau décanal pour un doyenné donné.
    """
    doyenne_id = request.GET.get('doyenne_id')
    if doyenne_id:
        try:
            doyenne = Doyenne.objects.get(id=doyenne_id)
            board = Board.objects.filter(
                board_type='decanal',
                doyenne=doyenne,
                is_current=True
            ).first()

            if board:
                members = BoardMembership.objects.filter(
                    board=board,
                    mandate__is_current=True
                ).select_related('member', 'position').order_by('position__order')

                html = render_to_string('members_list.html', {'members': members})
                return JsonResponse({'success': True, 'html': html})

            return JsonResponse({'success': False, 'error': 'Aucun bureau décanal actif trouvé pour ce doyenné'})

        except Doyenne.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Doyenné non trouvé'})

    return JsonResponse({'success': False, 'error': 'Requête invalide'})

def get_parish_members(request):
    """
    Retourne les membres du bureau paroissial pour une paroisse donnée.
    """
    parish_id = request.GET.get('parish_id')
    if parish_id:
        try:
            parish = Parish.objects.get(id=parish_id)
            board = Board.objects.filter(
                board_type='parish',
                parish=parish,
                is_current=True
            ).first()

            if board:
                members = BoardMembership.objects.filter(
                    board=board,
                    mandate__is_current=True
                ).select_related('member', 'position').order_by('position__order')

                html = render_to_string('members_list.html', {'members': members})
                return JsonResponse({'success': True, 'html': html})

            return JsonResponse({'success': False, 'error': 'Aucun bureau paroissial actif trouvé pour cette paroisse'})

        except Parish.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Paroisse non trouvée'})

    return JsonResponse({'success': False, 'error': 'Requête invalide'})

def get_history_decanal_members(request):
    """
    Retourne l'historique des bureaux décanaux pour un doyenné donné.
    """
    doyenne_id = request.GET.get('doyenne_id')
    if doyenne_id:
        try:
            doyenne = Doyenne.objects.get(id=doyenne_id)
            boards = Board.objects.filter(
                board_type='decanal',
                doyenne=doyenne
            ).order_by('-start_date')

            html = ''
            if boards.exists():
                for board in boards:
                    members = BoardMembership.objects.filter(
                        board=board
                    ).select_related('member', 'position').order_by('position__order')

                    html += f'<div class="card mb-4">'
                    html += f'<div class="card-header bg-primary text-white">'
                    html += f'<h3 class="mb-0">{board.name}</h3>'
                    html += f'</div>'
                    html += f'<div class="card-body">'
                    html += f'<p class="text-muted mb-3">'
                    html += f'<strong>Période:</strong> {board.start_date|date:"d/m/Y"} - '
                    html += f'{board.end_date|date:"d/m/Y" if board.end_date else "en cours"}' 
                    html += f'</p>'

                    if members.exists():
                        html += '<div class="row">'
                        for membership in members:
                            html += '<div class="col-md-6 col-lg-4 mb-3">'
                            html += '<div class="card h-100">'
                            if membership.member.photo:
                                html += f'<img src="{membership.member.photo.url}" class="card-img-top" alt="{membership.member}">'
                            html += '<div class="card-body">'
                            html += f'<h5 class="card-title">{membership.member.first_name} {membership.member.last_name}</h5>'
                            html += f'<h6 class="card-subtitle mb-2 text-primary">{membership.position}</h6>'
                            html += '</div>'
                            html += '</div>'
                            html += '</div>'
                        html += '</div>'
                    else:
                        html += '<div class="alert alert-info">Aucun membre trouvé pour ce bureau.</div>'

                    html += '</div>'
                    html += '</div>'
            else:
                html = '<div class="alert alert-info">Aucun bureau décanal trouvé pour ce doyenné.</div>'

            return JsonResponse({'success': True, 'html': html})

        except Doyenne.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Doyenné non trouvé'})

    return JsonResponse({'success': False, 'error': 'Requête invalide'})

def get_history_parish_members(request):
    """
    Retourne l'historique des bureaux paroissiaux pour une paroisse donnée.
    """
    parish_id = request.GET.get('parish_id')
    if parish_id:
        try:
            parish = Parish.objects.get(id=parish_id)
            boards = Board.objects.filter(
                board_type='parish',
                parish=parish
            ).order_by('-start_date')

            html = ''
            if boards.exists():
                for board in boards:
                    members = BoardMembership.objects.filter(
                        board=board
                    ).select_related('member', 'position').order_by('position__order')

                    html += f'<div class="card mb-4">'
                    html += f'<div class="card-header bg-primary text-white">'
                    html += f'<h3 class="mb-0">{board.name}</h3>'
                    html += f'</div>'
                    html += f'<div class="card-body">'
                    html += f'<p class="text-muted mb-3">'
                    html += f'<strong>Période:</strong> {board.start_date|date:"d/m/Y"} - '
                    html += f'{board.end_date|date:"d/m/Y" if board.end_date else "en cours"}' 
                    html += f'</p>'

                    if members.exists():
                        html += '<div class="row">'
                        for membership in members:
                            html += '<div class="col-md-6 col-lg-4 mb-3">'
                            html += '<div class="card h-100">'
                            if membership.member.photo:
                                html += f'<img src="{membership.member.photo.url}" class="card-img-top" alt="{membership.member}">'
                            html += '<div class="card-body">'
                            html += f'<h5 class="card-title">{membership.member.first_name} {membership.member.last_name}</h5>'
                            html += f'<h6 class="card-subtitle mb-2 text-primary">{membership.position}</h6>'
                            html += '</div>'
                            html += '</div>'
                            html += '</div>'
                        html += '</div>'
                    else:
                        html += '<div class="alert alert-info">Aucun membre trouvé pour ce bureau.</div>'

                    html += '</div>'
                    html += '</div>'
            else:
                html = '<div class="alert alert-info">Aucun bureau paroissial trouvé pour cette paroisse.</div>'

            return JsonResponse({'success': True, 'html': html})

        except Parish.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Paroisse non trouvée'})

    return JsonResponse({'success': False, 'error': 'Requête invalide'})
