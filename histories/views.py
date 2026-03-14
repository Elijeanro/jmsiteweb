from django.shortcuts import render, get_object_or_404
from .models import Histories
from django.core.paginator import Paginator

def history_list(request):
    histories_list = Histories.objects.all().order_by('-created_at')
    paginator = Paginator(histories_list, 10)
    page_number = request.GET.get('page')
    histories = paginator.get_page(page_number)
    return render(request, 'history/list.html', {'histories': histories})

def history_detail(request, history_id):
    history = get_object_or_404(Histories, id=history_id)
    return render(request, 'history/detail.html', {'history': history})
