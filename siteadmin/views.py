from django.forms import formset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.models import Event, EventImage
from events.forms import EventForm, EventImageForm
from documents.models import Document
from documents.forms import DocumentForm
from faustine.models import FaustineContent
from faustine.forms import FaustineContentForm
from parishes.models import Doyenne, Parish
from parishes.forms import DoyenneForm, ParishForm
from .models import AdminActivityLog
from histories.models import Histories, HistoryEntry
from histories.forms import HistoriesForm, HistoryEntryForm
from boards.models import Board, BoardType, Member, MemberPosition, Mandate, BoardMembership
from boards.forms import BoardForm, BoardTypeForm, MemberForm, MemberPositionForm, MandateForm, BoardMembershipForm

# Vue pour la page de connexion
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'siteadmin/login.html')

# Vue pour la page de déconnexion
@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# Vue pour le tableau de bord
@login_required
def admin_dashboard(request):
    return render(request, 'siteadmin/dashboard.html')

# Vues pour gérer les événements
@login_required
def manage_events(request):
    events_list = Event.objects.all().order_by('-created_at')
    paginator = Paginator(events_list, 10)  # Affiche 10 événements par page
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)
    return render(request, 'siteadmin/events/manage_events.html', {'events': events})

@login_required
def add_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        image_form = EventImageForm(request.POST, request.FILES)

        if event_form.is_valid():
            event = event_form.save()

            # Gestion des images
            images = request.FILES.getlist('images')
            for image in images:
                EventImage.objects.create(event=event, image=image)

            AdminActivityLog.objects.create(
                user=request.user,
                action="Création d'un événement",
                model_name="Event",
                object_id=event.id,
                details=f"Événement créé : {event.title}"
            )
            messages.success(request, 'Événement ajouté avec succès.')
            return redirect('add_event')  # Reste sur la même page pour ajouter plusieurs événements rapidement
    else:
        event_form = EventForm()
        image_form = EventImageForm()

    return render(request, 'siteadmin/events/add_event.html', {'event_form': event_form, 'image_form': image_form})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=event)
        image_form = EventImageForm(request.POST, request.FILES)

        if event_form.is_valid():
            event_form.save()

            # Gestion des images
            images = request.FILES.getlist('images')
            for image in images:
                EventImage.objects.create(event=event, image=image)

            messages.success(request, 'Événement mis à jour avec succès.')
            return redirect('manage_events')
    else:
        event_form = EventForm(instance=event)
        image_form = EventImageForm()

    return render(request, 'siteadmin/events/edit_event.html', {'event_form': event_form, 'image_form': image_form, 'event': event})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, 'Événement supprimé avec succès.')
    return redirect('manage_events')

@login_required
def delete_event_image(request, event_id, image_id):
    image = get_object_or_404(EventImage, id=image_id, event_id=event_id)
    image.delete()
    messages.success(request, 'Image supprimée avec succès.')
    return redirect('edit_event', event_id=event_id)

# Vues pour gérer les documents
@login_required
def manage_documents(request):
    documents_list = Document.objects.all().order_by('-created_at')
    paginator = Paginator(documents_list, 10)  # Affiche 10 documents par page
    page_number = request.GET.get('page')
    documents = paginator.get_page(page_number)
    return render(request, 'siteadmin/documents/manage_documents.html', {'documents': documents})

@login_required
def add_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document ajouté avec succès.')
            return redirect('add_document')  # Reste sur la même page pour ajouter plusieurs documents rapidement
    else:
        form = DocumentForm()
    return render(request, 'siteadmin/documents/add_document.html', {'form': form})

@login_required
def edit_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document mis à jour avec succès.')
            return redirect('manage_documents')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'siteadmin/documents/edit_document.html', {'form': form})

@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.delete()
    messages.success(request, 'Document supprimé avec succès.')
    return redirect('manage_documents')

# Vues pour gérer le contenu de Faustine
@login_required
def manage_faustine(request):
    contents_list = FaustineContent.objects.all().order_by('-created_at')
    paginator = Paginator(contents_list, 10)  # Affiche 10 contenus par page
    page_number = request.GET.get('page')
    contents = paginator.get_page(page_number)
    return render(request, 'siteadmin/manage_faustine.html', {'contents': contents})

@login_required
def add_faustine_content(request):
    if request.method == 'POST':
        form = FaustineContentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contenu ajouté avec succès.')
            return redirect('manage_faustine')
    else:
        form = FaustineContentForm()
    return render(request, 'siteadmin/add_faustine_content.html', {'form': form})

@login_required
def edit_faustine_content(request, content_id):
    content = get_object_or_404(FaustineContent, id=content_id)
    if request.method == 'POST':
        form = FaustineContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contenu mis à jour avec succès.')
            return redirect('manage_faustine')
    else:
        form = FaustineContentForm(instance=content)
    return render(request, 'siteadmin/edit_faustine_content.html', {'form': form})

@login_required
def delete_faustine_content(request, content_id):
    content = get_object_or_404(FaustineContent, id=content_id)
    content.delete()
    messages.success(request, 'Contenu supprimé avec succès.')
    return redirect('manage_faustine')

# Gestion des Historiques
@login_required
def manage_histories(request):
    histories_list = Histories.objects.all().order_by('-created_at')
    paginator = Paginator(histories_list, 10)  # Affiche 10 historiques par page
    page_number = request.GET.get('page')
    histories = paginator.get_page(page_number)
    return render(request, 'siteadmin/histories/manage_histories.html', {'histories': histories})

@login_required
def add_history(request):
    if request.method == 'POST':
        form = HistoriesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Historique ajouté avec succès.')
            return redirect('add_history')
    else:
        form = HistoriesForm()
    return render(request, 'siteadmin/histories/add_history.html', {'form': form})

@login_required
def edit_history(request, history_id):
    history = get_object_or_404(Histories, id=history_id)
    if request.method == 'POST':
        form = HistoriesForm(request.POST, instance=history)
        if form.is_valid():
            form.save()
            messages.success(request, 'Historique mis à jour avec succès.')
            return redirect('manage_histories')
    else:
        form = HistoriesForm(instance=history)
    return render(request, 'siteadmin/histories/edit_history.html', {'form': form})

@login_required
def delete_history(request, history_id):
    history = get_object_or_404(Histories, id=history_id)
    history.delete()
    messages.success(request, 'Historique supprimé avec succès.')
    return redirect('manage_histories')

@login_required
def manage_history_entries(request, history_id):
    history = get_object_or_404(Histories, id=history_id)
    entries_list = history.entries.all().order_by('date')
    paginator = Paginator(entries_list, 10)  # Affiche 10 entrées historiques par page
    page_number = request.GET.get('page')
    entries = paginator.get_page(page_number)
    return render(request, 'siteadmin/histories/manage_history_entries.html', {'history': history, 'entries': entries})

@login_required
def add_history_entry(request, history_id):
    history = get_object_or_404(Histories, id=history_id)

    if request.method == 'POST':
        form = HistoryEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.title = history
            entry.save()
            messages.success(request, 'Entrée historique ajoutée avec succès.')
            return redirect('add_history_entry', history_id=history.id)  # Reste sur la même page
    else:
        form = HistoryEntryForm()

    # Récupère toutes les entrées existantes pour cette histoire
    entries = HistoryEntry.objects.filter(title=history).order_by('date')

    return render(request, 'siteadmin/histories/add_history_entry.html', {
        'form': form,
        'history': history,
        'entries': entries
    })

@login_required
def edit_history_entry(request, history_id, entry_id):
    entry = get_object_or_404(HistoryEntry, id=entry_id)
    if request.method == 'POST':
        form = HistoryEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entrée historique mise à jour avec succès.')
            return redirect('manage_history_entries', history_id=history_id)
    else:
        form = HistoryEntryForm(instance=entry)
    return render(request, 'siteadmin/histories/edit_history_entry.html', {'form': form, 'history_id': history_id})

@login_required
def delete_history_entry(request, history_id, entry_id):
    entry = get_object_or_404(HistoryEntry, id=entry_id)
    entry.delete()
    messages.success(request, 'Entrée historique supprimée avec succès.')
    return redirect('manage_history_entries', history_id=history_id)

# Gestion des Doyennés
@login_required
def manage_doyennes(request):
    doyennes_list = Doyenne.objects.all().order_by('name')
    paginator = Paginator(doyennes_list, 10)  # Affiche 10 doyennés par page
    page_number = request.GET.get('page')
    doyennes = paginator.get_page(page_number)
    return render(request, 'siteadmin/parishes/manage_doyennes.html', {'doyennes': doyennes})

@login_required
def add_doyenne(request):
    if request.method == 'POST':
        form = DoyenneForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doyenné ajouté avec succès.')
            return redirect('add_doyenne')  # Reste sur la même page pour ajouter plusieurs doyennés rapidement
    else:
        form = DoyenneForm()
    return render(request, 'siteadmin/parishes/add_doyenne.html', {'form': form})

@login_required
def edit_doyenne(request, doyenne_id):
    doyenne = get_object_or_404(Doyenne, id=doyenne_id)
    if request.method == 'POST':
        form = DoyenneForm(request.POST, instance=doyenne)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doyenné mis à jour avec succès.')
            return redirect('manage_doyennes')
    else:
        form = DoyenneForm(instance=doyenne)
    return render(request, 'siteadmin/parishes/edit_doyenne.html', {'form': form})

@login_required
def delete_doyenne(request, doyenne_id):
    doyenne = get_object_or_404(Doyenne, id=doyenne_id)
    doyenne.delete()
    messages.success(request, 'Doyenné supprimé avec succès.')
    return redirect('manage_doyennes')

# Gestion des Paroisses
@login_required
def manage_parishes(request):
    parishes_list = Parish.objects.all().order_by('name')
    paginator = Paginator(parishes_list, 10)  # Affiche 10 paroisses par page
    page_number = request.GET.get('page')
    parishes = paginator.get_page(page_number)
    return render(request, 'siteadmin/parishes/manage_parishes.html', {'parishes': parishes})

@login_required
def add_parish(request):
    if request.method == 'POST':
        form = ParishForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paroisse ajoutée avec succès.')
            return redirect('add_parish')
    else:
        form = ParishForm()
        # Pré-remplir le champ doyenne si un paramètre doyenne est passé dans l'URL
        if 'doyenne' in request.GET:
            doyenne_id = request.GET.get('doyenne')
            form.fields['doyenne'].initial = doyenne_id

    return render(request, 'siteadmin/parishes/add_parish.html', {'form': form})

@login_required
def edit_parish(request, parish_id):
    parish = get_object_or_404(Parish, id=parish_id)
    if request.method == 'POST':
        form = ParishForm(request.POST, request.FILES, instance=parish)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paroisse mise à jour avec succès.')
            return redirect('manage_parishes')
    else:
        form = ParishForm(instance=parish)
    return render(request, 'siteadmin/parishes/edit_parish.html', {'form': form})

@login_required
def delete_parish(request, parish_id):
    parish = get_object_or_404(Parish, id=parish_id)
    parish.delete()
    messages.success(request, 'Paroisse supprimée avec succès.')
    return redirect('manage_parishes')

# Importations supplémentaires pour les vues boards
# Vues pour gérer les types de bureaux
@login_required
def manage_board_types(request):
    board_type_list = BoardType.objects.all().order_by('name')
    paginator = Paginator(board_type_list, 10)  # Affiche 10 types de bureaux par page
    page_number = request.GET.get('page')
    board_types = paginator.get_page(page_number)
    return render(request, 'siteadmin/boards/manage_board_types.html', {'board_types': board_types})

@login_required
def add_board_type(request):
    if request.method == 'POST':
        form = BoardTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Type de bureau ajouté avec succès.')
            return redirect('add_board_type')  # Reste sur la même page pour ajouter plusieurs types de bureaux rapidement
    else:
        form = BoardTypeForm()
    return render(request, 'siteadmin/boards/add_board_type.html', {'form': form})

@login_required
def edit_board_type(request, board_type_id):
    board_type = get_object_or_404(BoardType, id=board_type_id)
    if request.method == 'POST':
        form = BoardTypeForm(request.POST, instance=board_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Type de bureau mis à jour avec succès.')
            return redirect('manage_board_types')
    else:
        form = BoardTypeForm(instance=board_type)
    return render(request, 'siteadmin/boards/edit_board_type.html', {'form': form})

@login_required
def delete_board_type(request, board_type_id):
    board_type = get_object_or_404(BoardType, id=board_type_id)
    board_type.delete()
    messages.success(request, 'Type de bureau supprimé avec succès.')
    return redirect('manage_board_types')

# Vues pour gérer les postes
@login_required
def manage_member_positions(request):
    positions_list = MemberPosition.objects.all().order_by('order')
    paginator = Paginator(positions_list, 10)  # Affiche 10 postes par page
    page_number = request.GET.get('page')
    positions = paginator.get_page(page_number)
    return render(request, 'siteadmin/boards/manage_member_positions.html', {'positions': positions})

@login_required
def add_member_position(request):
    if request.method == 'POST':
        form = MemberPositionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Poste ajouté avec succès.')
            return redirect('add_member_position')  # Reste sur la même page pour ajouter plusieurs postes rapidement
    else:
        form = MemberPositionForm()
    return render(request, 'siteadmin/boards/add_member_position.html', {'form': form})

@login_required
def edit_member_position(request, position_id):
    position = get_object_or_404(MemberPosition, id=position_id)
    if request.method == 'POST':
        form = MemberPositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            messages.success(request, 'Poste mis à jour avec succès.')
            return redirect('manage_member_positions')
    else:
        form = MemberPositionForm(instance=position)
    return render(request, 'siteadmin/boards/edit_member_position.html', {'form': form})

@login_required
def delete_member_position(request, position_id):
    position = get_object_or_404(MemberPosition, id=position_id)
    position.delete()
    messages.success(request, 'Poste supprimé avec succès.')
    return redirect('manage_member_positions')

# Vues pour gérer les membres
@login_required
def manage_members(request):
    members_list = Member.objects.all().select_related('position', 'parish').order_by('position__order', 'last_name')
    paginator = Paginator(members_list, 10)  # Affiche 10 membres par page
    page_number = request.GET.get('page')
    members = paginator.get_page(page_number)
    return render(request, 'siteadmin/boards/manage_members.html', {'members': members})

@login_required
def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membre ajouté avec succès.')
            return redirect('add_member')  # Reste sur la même page pour ajouter plusieurs membres rapidement
    else:
        form = MemberForm()
    return render(request, 'siteadmin/boards/add_member.html', {'form': form})

@login_required
def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membre mis à jour avec succès.')
            return redirect('manage_members')
    else:
        form = MemberForm(instance=member)
    return render(request, 'siteadmin/boards/edit_member.html', {'form': form, 'member': member})

@login_required
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.delete()
    messages.success(request, 'Membre supprimé avec succès.')
    return redirect('manage_members')

# Vues pour gérer les mandats
@login_required
def manage_mandates(request):
    mandates_list = Mandate.objects.all().select_related('member').order_by('-start_date')
    paginator = Paginator(mandates_list, 10)  # Affiche 10 mandats par page
    page_number = request.GET.get('page')
    mandates = paginator.get_page(page_number)
    return render(request, 'siteadmin/boards/manage_mandates.html', {'mandates': mandates})

@login_required
def add_mandate(request):
    if request.method == 'POST':
        form = MandateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mandat ajouté avec succès.')
            return redirect('add_mandate')
    else:
        form = MandateForm()
    return render(request, 'siteadmin/boards/add_mandate.html', {'form': form})

@login_required
def edit_mandate(request, mandate_id):
    mandate = get_object_or_404(Mandate, id=mandate_id)
    if request.method == 'POST':
        form = MandateForm(request.POST, instance=mandate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mandat mis à jour avec succès.')
            return redirect('manage_mandates')
    else:
        form = MandateForm(instance=mandate)
    return render(request, 'siteadmin/boards/edit_mandate.html', {'form': form, 'mandate': mandate})

@login_required
def delete_mandate(request, mandate_id):
    mandate = get_object_or_404(Mandate, id=mandate_id)
    mandate.delete()
    messages.success(request, 'Mandat supprimé avec succès.')
    return redirect('manage_mandates')

# Vues pour gérer les bureaux
@login_required
def manage_boards(request):
    boards_list = Board.objects.all().select_related('doyenne', 'parish').order_by('-is_current', 'name')
    paginator = Paginator(boards_list, 10)  # Affiche 10 bureaux par page
    page_number = request.GET.get('page')
    boards = paginator.get_page(page_number)
    return render(request, 'siteadmin/boards/manage_boards.html', {'boards': boards})

@login_required
def add_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bureau ajouté avec succès.')
            return redirect('add_board')
    else:
        form = BoardForm()
    return render(request, 'siteadmin/boards/add_board.html', {'form': form})

@login_required
def edit_board(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bureau mis à jour avec succès.')
            return redirect('manage_boards')
    else:
        form = BoardForm(instance=board)
    return render(request, 'siteadmin/boards/edit_board.html', {'form': form, 'board': board})

@login_required
def delete_board(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    board.delete()
    messages.success(request, 'Bureau supprimé avec succès.')
    return redirect('manage_boards')

# Vues pour gérer les memberships
@login_required
def manage_board_memberships(request):
    memberships_list = BoardMembership.objects.all().select_related('board', 'member', 'position', 'mandate')
    paginator = Paginator(memberships_list, 10)  # Affiche 10 memberships par page
    page_number = request.GET.get('page')
    memberships = paginator.get_page(page_number)
    return render(request, 'siteadmin/boards/manage_board_memberships.html', {'memberships': memberships})

@login_required
def add_board_membership(request):
    if request.method == 'POST':
        form = BoardMembershipForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membership ajouté avec succès.')
            return redirect('add_board_membership')
    else:
        form = BoardMembershipForm()
    return render(request, 'siteadmin/boards/add_board_membership.html', {'form': form})

@login_required
def edit_board_membership(request, membership_id):
    membership = get_object_or_404(BoardMembership, id=membership_id)
    if request.method == 'POST':
        form = BoardMembershipForm(request.POST, instance=membership)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membership mis à jour avec succès.')
            return redirect('manage_board_memberships')
    else:
        form = BoardMembershipForm(instance=membership)
    return render(request, 'siteadmin/boards/edit_board_membership.html', {'form': form, 'membership': membership})

@login_required
def delete_board_membership(request, membership_id):
    membership = get_object_or_404(BoardMembership, id=membership_id)
    membership.delete()
    messages.success(request, 'Membership supprimé avec succès.')
    return redirect('manage_board_memberships')
