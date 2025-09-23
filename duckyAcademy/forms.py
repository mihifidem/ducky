
from .models import Course, Module, Unit, UnitPDF, UnitCheatsheet, UnitExtraDocument, UnitImage
from django import forms
from django import forms
from .models import Unit, UnitPDF, UnitCheatsheet, UnitExtraDocument, UnitImage

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['title', 'description', 'order']

class UnitPDFForm(forms.ModelForm):
    class Meta:
        model = UnitPDF
        fields = ['file', 'description']

class UnitCheatsheetForm(forms.ModelForm):
    class Meta:
        model = UnitCheatsheet
        fields = ['file', 'description']

class UnitExtraDocumentForm(forms.ModelForm):
    class Meta:
        model = UnitExtraDocument
        fields = ['file', 'description']

class UnitImageForm(forms.ModelForm):
    class Meta:
        model = UnitImage
        fields = ['image', 'description']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = '__all__'

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'

class UnitPDFForm(forms.ModelForm):
    class Meta:
        model = UnitPDF
        fields = ['unit', 'file', 'description']

class UnitCheatsheetForm(forms.ModelForm):
    class Meta:
        model = UnitCheatsheet
        fields = ['unit', 'file', 'description']

class UnitExtraDocumentForm(forms.ModelForm):
    class Meta:
        model = UnitExtraDocument
        fields = ['unit', 'file', 'description']

class UnitImageForm(forms.ModelForm):
    class Meta:
        model = UnitImage
        fields = ['unit', 'image', 'description']


