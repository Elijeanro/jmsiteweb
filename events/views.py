from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event
from django.core.paginator import Paginator

def event_list(request):
    events_list = Event.objects.all().order_by('-date')
    paginator = Paginator(events_list, 10)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)
    return render(request, 'events/list.html', {'events': events})

def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'events/detail.html', {'event': event})
