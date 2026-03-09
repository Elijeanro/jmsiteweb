from django.shortcuts import render, get_object_or_404
from .models import Histories

def history_list(request):
    histories = Histories.objects.all().order_by('-created_at')
    return render(request, 'history/list.html', {'histories': histories})

def history_detail(request, history_id):
    history = get_object_or_404(Histories, id=history_id)
    return render(request, 'history/detail.html', {'history': history})
