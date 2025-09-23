from django.contrib import admin
from .models import (
    Course, Module, Unit,
    UnitPDF, UnitCheatsheet, UnitExtraDocument, UnitImage
)

class UnitPDFInline(admin.TabularInline):
    model = UnitPDF
    extra = 1

class UnitCheatsheetInline(admin.TabularInline):
    model = UnitCheatsheet
    extra = 1

class UnitExtraDocumentInline(admin.TabularInline):
    model = UnitExtraDocument
    extra = 1

class UnitImageInline(admin.TabularInline):
    model = UnitImage
    extra = 1

class UnitAdmin(admin.ModelAdmin):
    inlines = [UnitPDFInline, UnitCheatsheetInline, UnitExtraDocumentInline, UnitImageInline]
    list_display = ['title', 'module']
    list_filter = ['module']

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]
    list_display = ['title', 'teacher', 'price', 'is_free_for_premium']
    list_filter = ['is_free_for_premium']

admin.site.register(Course, CourseAdmin)
admin.site.register(Module)
admin.site.register(Unit, UnitAdmin)
admin.site.register(UnitPDF)
admin.site.register(UnitCheatsheet)
admin.site.register(UnitImage)