from django.shortcuts import render, redirect
from .models import Pregunta, Profesional, Respuesta
from .forms import PreguntaFormPublic, RespuestaForm, PreguntaFormPrivate
# Create your views here.

def forum_home(request):
    preguntas = Pregunta.objects.filter(is_public=True).order_by('-date_at')
    respuestas = Respuesta.objects.filter(question__in=preguntas).order_by('-date_at')
    return render(request, 'forum/forum_home.html', {'preguntas': preguntas, 'respuestas': respuestas})

def pregunta_detail(request, pk):
    pregunta = Pregunta.objects.get(pk=pk)
    respuestas = Respuesta.objects.filter(question=pregunta).order_by('-date_at')
    return render(request, 'forum/pregunta_detail.html', {'pregunta': pregunta, 'respuestas': respuestas})

def pregunta_create_private(request):
    if request.method == 'POST':
        form = PreguntaFormPrivate(request.POST)
        if form.is_valid():
            pregunta = form.save(commit=False)
            pregunta.user_question = request.user
            pregunta.is_public = False
            pregunta.save()
            return redirect('pregunta_detail', pk=pregunta.pk)
    else:
        form = PreguntaFormPrivate()
    return render(request, 'forum/pregunta_create_private.html', {'form': form})

def pregunta_create_public(request):
    if request.method == 'POST':
        form = PreguntaFormPublic(request.POST)
        if form.is_valid():
            pregunta = form.save(commit=False)
            pregunta.user_question = request.user
            pregunta.is_public = True
            pregunta.save()
            return redirect('pregunta_detail', pk=pregunta.pk)
    else:
        form = PreguntaFormPublic()
    return render(request, 'forum/pregunta_create_public.html', {'form': form})

def pregunta_edit(request, pk):
    return render(request, 'forum/pregunta_edit.html', {'pk': pk})

def pregunta_delete(request, pk):
    return render(request, 'forum/pregunta_delete.html', {'pk': pk})

def respuesta_create(request, pk):
    pregunta = Pregunta.objects.get(pk=pk)
    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.question = pregunta
            respuesta.user_answer = request.user
            respuesta.save()
            return redirect('pregunta_detail', pk=pregunta.pk)
    else:
        form = RespuestaForm()
    return render(request, 'forum/respuesta_create.html', {'pk': pk, 'form': form})

def respuesta_edit(request, pk):
    return render(request, 'forum/respuesta_edit.html', {'pk': pk})

def respuesta_delete(request, pk):  
    return render(request, 'forum/respuesta_delete.html', {'pk': pk})