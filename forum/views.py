from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  
from .models import Pregunta, Profesional, Respuesta
from .forms import PreguntaFormPublic, RespuestaForm, PreguntaFormPrivate
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, DetailView, ListView
from django.http import JsonResponse
# Create your views here.

def forum_home(request):
    preguntas = Pregunta.objects.filter(is_public=True).order_by('-date_at')
    respuestas = Respuesta.objects.filter(question__in=preguntas).order_by('-date_at')
    
    for pregunta in preguntas:
        pregunta.is_active_status = pregunta.is_active()
        
    return render(request, 'forum/forum_home.html', {'preguntas': preguntas, 'respuestas': respuestas})



def cargar_profesionales(request):
    sector_id = request.GET.get('sector')
    profesionales = Profesional.objects.filter(sector=sector_id).values('id', 'nombre')
    return JsonResponse(list(profesionales), safe=False)

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

class PreguntaDetailView(DetailView):
    model = Pregunta
    template_name = 'forum/pregunta_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['respuestas'] = Respuesta.objects.filter(question=self.object).order_by('-date_at')
        context['is_active'] = self.object.is_active()
        context['form'] = RespuestaForm()  
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if not self.object.is_active():
            messages.error(request, "Esta pregunta ya no acepta respuestas porque ha expirado.")
            return redirect('pregunta_detail', pk=self.object.pk)
        
        form = RespuestaForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.question = self.object
            respuesta.user_answer = request.user
            respuesta.save()
            return redirect('pregunta_detail', pk=self.object.pk)


def respuesta_create(request, pk):
    pregunta = Pregunta.objects.get(pk=pk)

    if not pregunta.is_active():
        messages.error(request, "Esta pregunta ya no acepta respuestas porque ha expirado.")
        return redirect('pregunta_detail', pk=pregunta.pk)
        
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

class PreguntaUpdateView(UpdateView):
    model = Pregunta
    form_class = PreguntaFormPublic
    template_name = 'forum/pregunta_edit.html'
    success_url = reverse_lazy('forum_home')

    def get_question(self):
        return Pregunta.objects.filter(user_question=self.request.user)
    
class PreguntaDeleteView(DeleteView):
    model = Pregunta
    template_name = 'forum/pregunta_delete.html'
    success_url = reverse_lazy('forum_home')

    def get_question(self):
        return Pregunta.objects.filter(user_question=self.request.user)
    
class RespuestaUpdateView(UpdateView):
    model = Respuesta
    form_class = RespuestaForm
    template_name = 'forum/respuesta_edit.html'
    success_url = reverse_lazy('forum_home')

    def get_question(self):
        return Respuesta.objects.filter(user_answer=self.request.user)

class RespuestaDeleteView(DeleteView):
    model = Respuesta
    template_name = 'forum/respuesta_delete.html'
    success_url = reverse_lazy('forum_home')

    def get_question(self):
        return Respuesta.objects.filter(user_answer=self.request.user)
    

def mail_list(request):
    preguntas = Pregunta.objects.filter(is_public=False, user_question=request.user).order_by('-date_at')
    respuestas = Respuesta.objects.filter(question__in=preguntas).order_by('-date_at')
    return render(request, 'forum/mail_list.html', {'preguntas': preguntas, 'respuestas': respuestas})

def mail_recibido(request):
    preguntas = Pregunta.objects.filter(is_public=False, professional_user__user=request.user).order_by('-date_at')
    respuestas = Respuesta.objects.filter(question__in=preguntas).order_by('-date_at')
    return render(request, 'forum/mail_recibido.html', {'preguntas': preguntas, 'respuestas': respuestas})

def editar_respuesta(request, respuesta_id):
    respuesta = get_object_or_404(Respuesta, id=respuesta_id)
    if request.method == 'POST':
        form = RespuestaForm(request.POST, instance=respuesta)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.editado = True  # marcamos que fue editada
            respuesta.save()
            return redirect('detalle_pregunta', pk=respuesta.pregunta.id)
    else:
        form = RespuestaForm(instance=respuesta)
    return render(request, 'editar_respuesta.html', {'form': form})
