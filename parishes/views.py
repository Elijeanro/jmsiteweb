from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Doyenne, Parish

def parish_list(request):
    doyennes_list = Doyenne.objects.prefetch_related('parishes').all().order_by('name')
    paginator = Paginator(doyennes_list, 10)  # Affiche 10 doyennés par page
    page_number = request.GET.get('page')
    doyennes = paginator.get_page(page_number)
    return render(request, 'parishes/list.html', {'doyennes': doyennes})

def doyenne_detail(request, doyenne_id):
    doyenne = get_object_or_404(Doyenne.objects.prefetch_related('parishes'), id=doyenne_id)
    parishes_list = doyenne.parishes.all().order_by('name')
    paginator = Paginator(parishes_list, 10)  # Affiche 10 paroisses par page
    page_number = request.GET.get('page')
    parishes = paginator.get_page(page_number)
    return render(request, 'parishes/detail.html', {'doyenne': doyenne, 'parishes': parishes})
