from django.shortcuts import render

# Create your views here.

def forum_home(request):
    return render(request, 'forum/forum_home.html')

def pregunta_detail(request, pk):
    return render(request, 'forum/pregunta_detail.html', {'pk': pk})

def pregunta_create_private(request):
    return render(request, 'forum/pregunta_create_private.html')

def pregunta_create_public(request):
    return render(request, 'forum/pregunta_create_public.html')

def pregunta_edit(request, pk):
    return render(request, 'forum/pregunta_edit.html', {'pk': pk})

def pregunta_delete(request, pk):
    return render(request, 'forum/pregunta_delete.html', {'pk': pk})

def respuesta_create(request, pk):
    return render(request, 'forum/respuesta_create.html', {'pk': pk})

def respuesta_edit(request, pk):
    return render(request, 'forum/respuesta_edit.html', {'pk': pk})

def respuesta_delete(request, pk):  
    return render(request, 'forum/respuesta_delete.html', {'pk': pk})