from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'teacher'})
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    is_free_for_premium = models.BooleanField(default=False)
    image = models.ImageField(upload_to='courses/images/', blank=True, null=True)

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)  # <-- Asegúrate de tener esto


    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Unit(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='units')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)  # <-- Asegúrate de tener esto
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"

class UnitPDF(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='pdfs')
    file = models.FileField(upload_to='units/pdfs/')
    description = models.CharField(max_length=255, blank=True)

class UnitCheatsheet(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='cheatsheets')
    file = models.FileField(upload_to='units/cheatsheets/')
    description = models.CharField(max_length=255, blank=True)

class UnitExtraDocument(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='extras')
    file = models.FileField(upload_to='units/extras/')
    description = models.CharField(max_length=255, blank=True)

class UnitImage(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='units/images/')
    description = models.CharField(max_length=255, blank=True)
