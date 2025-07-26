"""
URL Configuration for Timetable Management System
Developed by TEAM SPIDERMERN (SANJAY B, YASWANTH ST, ABISHECK AM)
"""

from django.urls import path
from . import views

urlpatterns = [
    # Home and Dashboard
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Staff Management
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/create/', views.staff_create, name='staff_create'),
    path('staff/edit/<str:staff_id>/', views.staff_edit, name='staff_edit'),
    
    # Subject Management
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/create/', views.subject_create, name='subject_create'),
    
    # Class Management
    path('classes/', views.class_list, name='class_list'),
    path('classes/create/', views.class_create, name='class_create'),
    
    # Room Management
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/create/', views.room_create, name='room_create'),
    
    # Timetable Generation and Viewing
    path('timetable/generate/', views.timetable_generate, name='timetable_generate'),
    path('timetable/view/<str:academic_year>/', views.timetable_view, name='timetable_view'),
    
    # Substitution Management
    path('substitutions/', views.substitution_list, name='substitution_list'),
    path('substitutions/create/', views.substitution_create, name='substitution_create'),
    path('substitutions/approve/<int:substitution_id>/', views.substitution_approve, name='substitution_approve'),
    
    # API Endpoints
    path('api/conflict-resolution/', views.api_conflict_resolution, name='api_conflict_resolution'),
    path('api/timetable-export/', views.api_timetable_export, name='api_timetable_export'),
    path('api/statistics/', views.api_statistics, name='api_statistics'),
]