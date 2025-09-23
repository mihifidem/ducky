from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Module, Unit
from .forms import CourseForm, ModuleForm, UnitForm, UnitPDFForm
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView
from .models import Unit, UnitPDF, UnitCheatsheet, UnitExtraDocument, UnitImage
from .forms import UnitPDFForm, UnitCheatsheetForm, UnitExtraDocumentForm, UnitImageForm
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Unit
from .forms import UnitPDFForm, UnitCheatsheetForm, UnitExtraDocumentForm, UnitImageForm
# views.py
from .forms import UnitForm, UnitPDFForm, UnitCheatsheetForm, UnitExtraDocumentForm, UnitImageForm

def create_unit_with_files(request, course_id, module_id):
    module = get_object_or_404(Module, pk=module_id)

    if request.method == 'POST':
        unit_form = UnitForm(request.POST)
        pdf_form = UnitPDFForm(request.POST, request.FILES, prefix='pdf')
        cheatsheet_form = UnitCheatsheetForm(request.POST, request.FILES, prefix='cheat')
        extra_form = UnitExtraDocumentForm(request.POST, request.FILES, prefix='extra')
        image_form = UnitImageForm(request.POST, request.FILES, prefix='img')

        if unit_form.is_valid():
            unit = unit_form.save(commit=False)
            unit.module = module
            unit.save()

            # Guardar si hay archivos
            if pdf_form.is_valid() and pdf_form.cleaned_data.get('file'):
                pdf = pdf_form.save(commit=False)
                pdf.unit = unit
                pdf.save()

            if cheatsheet_form.is_valid() and cheatsheet_form.cleaned_data.get('file'):
                cheat = cheatsheet_form.save(commit=False)
                cheat.unit = unit
                cheat.save()

            if extra_form.is_valid() and extra_form.cleaned_data.get('file'):
                extra = extra_form.save(commit=False)
                extra.unit = unit
                extra.save()

            if image_form.is_valid() and image_form.cleaned_data.get('image'):
                img = image_form.save(commit=False)
                img.unit = unit
                img.save()

            return redirect('unit_detail', pk=unit.pk)

    else:
        unit_form = UnitForm()
        pdf_form = UnitPDFForm(prefix='pdf')
        cheatsheet_form = UnitCheatsheetForm(prefix='cheat')
        extra_form = UnitExtraDocumentForm(prefix='extra')
        image_form = UnitImageForm(prefix='img')

    context = {
        'unit_form': unit_form,
        'pdf_form': pdf_form,
        'cheatsheet_form': cheatsheet_form,
        'extra_form': extra_form,
        'image_form': image_form,
        'module': module,
    }
    return render(request, 'duckyAcademy/unit_create.html', context)

def unit_detail_view(request, pk):
    unit = get_object_or_404(Unit, pk=pk)

    if request.method == 'POST':
        if 'upload_pdf' in request.POST:
            form = UnitPDFForm(request.POST, request.FILES)
            if form.is_valid():
                pdf = form.save(commit=False)
                pdf.unit = unit
                pdf.save()
                return redirect('unit_detail', pk=pk)

        elif 'upload_cheatsheet' in request.POST:
            form = UnitCheatsheetForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.unit = unit
                obj.save()
                return redirect('unit_detail', pk=pk)

        elif 'upload_extra' in request.POST:
            form = UnitExtraDocumentForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.unit = unit
                obj.save()
                return redirect('unit_detail', pk=pk)

        elif 'upload_image' in request.POST:
            form = UnitImageForm(request.POST, request.FILES)
            if form.is_valid():
                img = form.save(commit=False)
                img.unit = unit
                img.save()
                return redirect('unit_detail', pk=pk)

    context = {
        'unit': unit,
        'pdf_form': UnitPDFForm(),
        'cheatsheet_form': UnitCheatsheetForm(),
        'extra_form': UnitExtraDocumentForm(),
        'image_form': UnitImageForm(),
    }
    return render(request, 'unit_detail.html', context)

class UnitListView(ListView):
    model = Unit
    template_name = 'unit_list.html'
    context_object_name = 'units'

    def get_queryset(self):
        return Unit.objects.prefetch_related('pdfs', 'cheatsheets', 'extras', 'images')

class UnitPDFCreateView(CreateView):
    model = UnitPDF
    form_class = UnitPDFForm

    def form_valid(self, form):
        form.instance.unit_id = self.kwargs['unit_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('unit_detail', kwargs={'pk': self.kwargs['unit_id']})

class UnitCheatsheetCreateView(CreateView):
    model = UnitCheatsheet
    form_class = UnitCheatsheetForm

    def form_valid(self, form):
        form.instance.unit_id = self.kwargs['unit_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('unit_detail', kwargs={'pk': self.kwargs['unit_id']})

class UnitExtraDocumentCreateView(CreateView):
    model = UnitExtraDocument
    form_class = UnitExtraDocumentForm

    def form_valid(self, form):
        form.instance.unit_id = self.kwargs['unit_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('unit_detail', kwargs={'pk': self.kwargs['unit_id']})

class UnitImageCreateView(CreateView):
    model = UnitImage
    form_class = UnitImageForm

    def form_valid(self, form):
        form.instance.unit_id = self.kwargs['unit_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('unit_detail', kwargs={'pk': self.kwargs['unit_id']})

class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='teacher').exists()


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'duckyAcademy/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'duckyAcademy/course_detail.html', {'course': course})

@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'duckyAcademy/course_form.html', {'form': form})

def module_detail(request, pk):
    module = get_object_or_404(Module, pk=pk)
    return render(request, 'duckyAcademy/module_detail.html', {'module': module})

def unit_detail(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    return render(request, 'duckyAcademy/unit_detail.html', {'unit': unit})

def module_create(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')  # Redirige según tu estructura
    else:
        form = ModuleForm()
    return render(request, 'duckyAcademy/module_form.html', {'form': form})

def unit_create(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = UnitForm()
    return render(request, 'duckyAcademy/unit_form.html', {'form': form})

def unit_pdf_upload(request):
    if request.method == 'POST':
        form = UnitPDFForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = UnitPDFForm()
    return render(request, 'duckyAcademy/upload_form.html', {'form': form, 'title': 'Subir PDF'})

def module_list(request):
    modules = Module.objects.all()
    return render(request, 'duckyAcademy/module_list.html', {
        'modules': modules
    })

def unit_list(request):
    units = Unit.objects.select_related('module').all()
    return render(request, 'duckyAcademy/unit_list.html', {
        'units': units
    })

class CourseUpdateView(TeacherRequiredMixin, UpdateView):
    model = Course
    fields = ['title', 'description']
    template_name = 'duckyAcademy/course_update.html'
    success_url = reverse_lazy('course_list')

class CourseDeleteView(TeacherRequiredMixin, DeleteView):
    model = Course
    template_name = 'duckyAcademy/course_delete.html'
    success_url = reverse_lazy('course_list')

class ModuleUpdateView(TeacherRequiredMixin, UpdateView):
    model = Module
    fields = ['title', 'description', 'course']
    template_name = 'duckyAcademy/module_update.html'
    success_url = reverse_lazy('course_list')

class ModuleDeleteView(TeacherRequiredMixin, DeleteView):
    model = Module
    template_name = 'duckyAcademy/module_delete.html'
    success_url = reverse_lazy('course_list')

class UnitUpdateView(TeacherRequiredMixin, UpdateView):
    model = Unit
    fields = ['title','description' ,'module']
    template_name = 'duckyAcademy/unit_update.html'
    success_url = reverse_lazy('course_list')


class UnitDeleteView(TeacherRequiredMixin, DeleteView):
    model = Unit
    template_name = 'duckyAcademy/unit_delete.html'
    success_url = reverse_lazy('course_list')

class ModuleCreateView(TeacherRequiredMixin, CreateView):
    model = Module
    fields = ['title', 'description']
    template_name = 'duckyAcademy/module_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Course, pk=kwargs['course_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.course = self.course
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('course_list')


class UnitCreateView(TeacherRequiredMixin, CreateView):
    model = Unit
    fields = ['title', 'description']
    template_name = 'duckyAcademy/unit_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.module = get_object_or_404(Module, pk=kwargs['module_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.module = self.module
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('course_list')
