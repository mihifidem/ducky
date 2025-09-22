from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/create/', views.course_create, name='course_create'),
    path('module/<int:pk>/', views.module_detail, name='module_detail'),
    path('unit/<int:pk>/', views.unit_detail, name='unit_detail'),

    path('units/create/', views.unit_create, name='unit_create'),
    path('units/pdf/', views.unit_pdf_upload, name='unit_pdf_upload'),
# path('units/create/<int:course_id>/<int:module_id>/', views.UnitCreateView.as_view(), name='unit_create2'),
path('units/create/<int:course_id>/<int:module_id>/', views.create_unit_with_files, name='unit_create2'),

      # Módulos
    path('modules/', views.module_list, name='module_list'),
    path('modules/create/', views.module_create, name='module_create'),
        path('modules/create/<int:course_id>/', views.ModuleCreateView.as_view(), name='module_create2'),

    # Unidades
    path('units/', views.unit_list, name='unit_list'),
    
        path('course/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_update'),
    path('course/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    path('module/<int:pk>/edit/', views.ModuleUpdateView.as_view(), name='module_update'),
    path('module/<int:pk>/delete/', views.ModuleDeleteView.as_view(), name='module_delete'),

    path('unit/<int:pk>/edit/', views.UnitUpdateView.as_view(), name='unit_update'),
    path('unit/<int:pk>/delete/', views.UnitDeleteView.as_view(), name='unit_delete'),

  path('unit/<int:unit_id>/add-pdf/', views.UnitPDFCreateView.as_view(), name='add_pdf'),
    path('unit/<int:unit_id>/add-cheatsheet/', views.UnitCheatsheetCreateView.as_view(), name='add_cheatsheet'),
    path('unit/<int:unit_id>/add-extra/', views.UnitExtraDocumentCreateView.as_view(), name='add_extra'),
    path('unit/<int:unit_id>/add-image/', views.UnitImageCreateView.as_view(), name='add_image'),
    
    path('unit/<int:pk>/', views.unit_detail_view, name='unit_detail'),

]

