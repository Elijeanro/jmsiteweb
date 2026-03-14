from django.shortcuts import render
from .models import Document
from django.core.paginator import Paginator

def document_list(request):
    documents = Document.objects.all().order_by('-created_at')
    paginator = Paginator(documents, 10)
    page_number = request.GET.get('page')
    documents = paginator.get_page(page_number)
    return render(request, 'documents/list.html', {'documents': documents})

def document_detail(request, document_id):
    document = Document.objects.get(id=document_id)
    return render(request, 'documents/detail.html', {'document': document})