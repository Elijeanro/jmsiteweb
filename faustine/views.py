from django.shortcuts import render
from .models import FaustineContent

def faustine_list(request):
    contents = FaustineContent.objects.all().order_by('created_at')
    return render(request, 'faustine/list.html', {'contents': contents})
