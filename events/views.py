from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event

def event_list(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'events/list.html', {'events': events})

def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'events/detail.html', {'event': event})
