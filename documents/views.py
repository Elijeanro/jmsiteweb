from django.shortcuts import render
from .models import Document

def document_list(request):
    documents = Document.objects.all().order_by('-created_at')
    return render(request, 'documents/list.html', {'documents': documents})

def document_detail(request, document_id):
    document = Document.objects.get(id=document_id)
    return render(request, 'documents/detail.html', {'document': document})