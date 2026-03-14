from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Program


def program_list(request):
    programs_list = Program.objects.filter(is_active=True).order_by('-created_at')
    paginator = Paginator(programs_list, 10)
    page_number = request.GET.get('page')
    programs = paginator.get_page(page_number)
    return render(request, 'programs/list.html', {'programs': programs})


def program_detail(request, pk: int):
    program = get_object_or_404(
        Program.objects.prefetch_related('files', 'schedules__items'),
        pk=pk,
        is_active=True,
    )
    return render(request, 'programs/detail.html', {'program': program})
