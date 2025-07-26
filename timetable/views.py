"""
Django Views for Timetable Management System
Developed by TEAM SPIDERMERN (SANJAY B, YASWANTH ST, ABISHECK AM)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator
from datetime import datetime, date, time, timedelta
import json
import logging
from typing import Dict, List

from .models import (
    Staff, Subject, ClassSection, Room, Timetable, 
    Elective, Substitution, TimetableGeneration
)
from .genetic_algorithm import GeneticAlgorithmScheduler
from .substitution_engine import SubstitutionEngine
from .mongodb import mongo_collections

logger = logging.getLogger(__name__)

# Home and Dashboard Views
def index(request):
    """Main dashboard view"""
    context = {
        'total_staff': Staff.objects.count(),
        'total_subjects': Subject.objects.count(),
        'total_classes': ClassSection.objects.count(),
        'total_rooms': Room.objects.filter(is_active=True).count(),
        'total_timetables': Timetable.objects.count(),
        'team_info': {
            'developed_by': 'TEAM SPIDERMERN',
            'members': ['SANJAY B', 'YASWANTH ST', 'ABISHECK AM'],
            'project': 'Smart Timetable Generation System'
        }
    }
    return render(request, 'timetable/index.html', context)

def dashboard(request):
    """Enhanced dashboard with statistics"""
    
    # Recent activity
    recent_generations = TimetableGeneration.objects.order_by('-created_at')[:5]
    recent_substitutions = Substitution.objects.order_by('-created_at')[:5]
    
    # Statistics
    total_slots = 0
    occupied_slots = Timetable.objects.count()
    
    for class_section in ClassSection.objects.all():
        total_slots += class_section.working_days_per_week * class_section.slots_per_day
    
    utilization_rate = (occupied_slots / total_slots * 100) if total_slots > 0 else 0
    
    context = {
        'stats': {
            'total_staff': Staff.objects.count(),
            'total_subjects': Subject.objects.count(),
            'total_classes': ClassSection.objects.count(),
            'total_rooms': Room.objects.filter(is_active=True).count(),
            'utilization_rate': round(utilization_rate, 2),
            'pending_substitutions': Substitution.objects.filter(is_approved=False).count(),
        },
        'recent_generations': recent_generations,
        'recent_substitutions': recent_substitutions,
    }
    return render(request, 'timetable/dashboard.html', context)

# Staff Management Views
def staff_list(request):
    """List all staff members"""
    staff_members = Staff.objects.all().order_by('name')
    paginator = Paginator(staff_members, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_staff': staff_members.count()
    }
    return render(request, 'timetable/staff_list.html', context)

def staff_create(request):
    """Create new staff member"""
    if request.method == 'POST':
        try:
            staff_data = {
                'staff_id': request.POST.get('staff_id'),
                'name': request.POST.get('name'),
                'designation': request.POST.get('designation'),
                'department': request.POST.get('department'),
                'email': request.POST.get('email'),
                'max_sessions_per_week': int(request.POST.get('max_sessions_per_week', 20)),
                'max_sessions_per_day': int(request.POST.get('max_sessions_per_day', 6)),
                'subjects_handled': json.loads(request.POST.get('subjects_handled', '[]')),
                'labs_handled': json.loads(request.POST.get('labs_handled', '[]')),
                'electives_handled': json.loads(request.POST.get('electives_handled', '[]')),
                'leave_dates': json.loads(request.POST.get('leave_dates', '[]')),
            }
            
            staff = Staff.objects.create(**staff_data)
            messages.success(request, f'Staff member {staff.name} created successfully!')
            return redirect('staff_list')
            
        except Exception as e:
            messages.error(request, f'Error creating staff: {str(e)}')
    
    context = {
        'departments': Staff.DEPARTMENT_CHOICES,
        'designations': Staff.DESIGNATION_CHOICES,
        'subjects': Subject.objects.all(),
    }
    return render(request, 'timetable/staff_form.html', context)

def staff_edit(request, staff_id):
    """Edit existing staff member"""
    staff = get_object_or_404(Staff, staff_id=staff_id)
    
    if request.method == 'POST':
        try:
            staff.name = request.POST.get('name')
            staff.designation = request.POST.get('designation')
            staff.department = request.POST.get('department')
            staff.email = request.POST.get('email')
            staff.max_sessions_per_week = int(request.POST.get('max_sessions_per_week', 20))
            staff.max_sessions_per_day = int(request.POST.get('max_sessions_per_day', 6))
            staff.subjects_handled = json.loads(request.POST.get('subjects_handled', '[]'))
            staff.labs_handled = json.loads(request.POST.get('labs_handled', '[]'))
            staff.electives_handled = json.loads(request.POST.get('electives_handled', '[]'))
            staff.leave_dates = json.loads(request.POST.get('leave_dates', '[]'))
            staff.save()
            
            messages.success(request, f'Staff member {staff.name} updated successfully!')
            return redirect('staff_list')
            
        except Exception as e:
            messages.error(request, f'Error updating staff: {str(e)}')
    
    context = {
        'staff': staff,
        'departments': Staff.DEPARTMENT_CHOICES,
        'designations': Staff.DESIGNATION_CHOICES,
        'subjects': Subject.objects.all(),
    }
    return render(request, 'timetable/staff_form.html', context)

# Subject Management Views
def subject_list(request):
    """List all subjects"""
    subjects = Subject.objects.all().order_by('subject_code')
    paginator = Paginator(subjects, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_subjects': subjects.count()
    }
    return render(request, 'timetable/subject_list.html', context)

def subject_create(request):
    """Create new subject"""
    if request.method == 'POST':
        try:
            subject_data = {
                'subject_code': request.POST.get('subject_code'),
                'subject_name': request.POST.get('subject_name'),
                'subject_type': request.POST.get('subject_type'),
                'department': request.POST.get('department'),
                'semester': int(request.POST.get('semester')),
                'credits': int(request.POST.get('credits')),
                'hours_per_week': int(request.POST.get('hours_per_week')),
                'is_lab': request.POST.get('is_lab') == 'on',
                'lab_duration_hours': int(request.POST.get('lab_duration_hours', 2)),
                'prerequisite_subjects': json.loads(request.POST.get('prerequisite_subjects', '[]')),
            }
            
            subject = Subject.objects.create(**subject_data)
            messages.success(request, f'Subject {subject.subject_code} created successfully!')
            return redirect('subject_list')
            
        except Exception as e:
            messages.error(request, f'Error creating subject: {str(e)}')
    
    context = {
        'departments': Staff.DEPARTMENT_CHOICES,
        'subject_types': Subject.SUBJECT_TYPE_CHOICES,
        'subjects': Subject.objects.all(),
    }
    return render(request, 'timetable/subject_form.html', context)

# Class Management Views
def class_list(request):
    """List all class sections"""
    classes = ClassSection.objects.all().order_by('year', 'department', 'section')
    paginator = Paginator(classes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_classes': classes.count()
    }
    return render(request, 'timetable/class_list.html', context)

def class_create(request):
    """Create new class section"""
    if request.method == 'POST':
        try:
            class_data = {
                'class_id': request.POST.get('class_id'),
                'year': int(request.POST.get('year')),
                'section': request.POST.get('section'),
                'department': request.POST.get('department'),
                'total_students': int(request.POST.get('total_students')),
                'subjects': json.loads(request.POST.get('subjects', '[]')),
                'labs': json.loads(request.POST.get('labs', '[]')),
                'electives': json.loads(request.POST.get('electives', '[]')),
                'working_days_per_week': int(request.POST.get('working_days_per_week', 5)),
                'slots_per_day': int(request.POST.get('slots_per_day', 8)),
            }
            
            class_section = ClassSection.objects.create(**class_data)
            messages.success(request, f'Class {class_section.class_id} created successfully!')
            return redirect('class_list')
            
        except Exception as e:
            messages.error(request, f'Error creating class: {str(e)}')
    
    context = {
        'departments': Staff.DEPARTMENT_CHOICES,
        'years': ClassSection.YEAR_CHOICES,
        'sections': ClassSection.SECTION_CHOICES,
        'subjects': Subject.objects.all(),
        'electives': Elective.objects.all(),
    }
    return render(request, 'timetable/class_form.html', context)

# Room Management Views
def room_list(request):
    """List all rooms"""
    rooms = Room.objects.filter(is_active=True).order_by('room_id')
    paginator = Paginator(rooms, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_rooms': rooms.count()
    }
    return render(request, 'timetable/room_list.html', context)

def room_create(request):
    """Create new room"""
    if request.method == 'POST':
        try:
            room_data = {
                'room_id': request.POST.get('room_id'),
                'room_name': request.POST.get('room_name'),
                'room_type': request.POST.get('room_type'),
                'capacity': int(request.POST.get('capacity')),
                'department': request.POST.get('department') or None,
                'floor': int(request.POST.get('floor', 0)),
                'building': request.POST.get('building'),
                'facilities': json.loads(request.POST.get('facilities', '[]')),
                'availability': json.loads(request.POST.get('availability', '{}')),
                'is_active': True,
            }
            
            room = Room.objects.create(**room_data)
            messages.success(request, f'Room {room.room_id} created successfully!')
            return redirect('room_list')
            
        except Exception as e:
            messages.error(request, f'Error creating room: {str(e)}')
    
    context = {
        'departments': Staff.DEPARTMENT_CHOICES,
        'room_types': Room.ROOM_TYPE_CHOICES,
    }
    return render(request, 'timetable/room_form.html', context)

# Timetable Generation Views
def timetable_generate(request):
    """Timetable generation interface"""
    if request.method == 'POST':
        try:
            academic_year = request.POST.get('academic_year')
            semester = int(request.POST.get('semester'))
            department = request.POST.get('department')
            
            # Create generation record
            generation = TimetableGeneration.objects.create(
                academic_year=academic_year,
                semester=semester,
                department=department if department != 'all' else None,
                status='in_progress',
                generated_by=request.user.username if request.user.is_authenticated else 'anonymous',
                started_at=datetime.now()
            )
            
            # Start GA generation
            scheduler = GeneticAlgorithmScheduler(
                population_size=100,
                generations=300,
                mutation_rate=0.15,
                crossover_rate=0.8
            )
            
            best_chromosome, stats = scheduler.generate_timetable()
            
            # Save timetable to database
            if best_chromosome:
                with transaction.atomic():
                    # Clear existing timetables for this academic year
                    if department and department != 'all':
                        Timetable.objects.filter(
                            academic_year=academic_year,
                            class_section__department=department
                        ).delete()
                    else:
                        Timetable.objects.filter(academic_year=academic_year).delete()
                    
                    # Save new timetable
                    for gene in best_chromosome.genes:
                        slot_times = scheduler.slot_times
                        start_time, end_time = slot_times[gene.slot]
                        
                        Timetable.objects.create(
                            class_section=ClassSection.objects.get(class_id=gene.class_section_id),
                            day=gene.day,
                            slot_number=gene.slot,
                            start_time=start_time,
                            end_time=end_time,
                            subject=Subject.objects.get(subject_code=gene.subject_code),
                            staff=Staff.objects.get(staff_id=gene.staff_id),
                            room=Room.objects.get(room_id=gene.room_id),
                            is_lab=gene.is_lab,
                            is_elective=gene.is_elective,
                            academic_year=academic_year,
                            week_number=1
                        )
                
                # Update generation record
                generation.status = 'completed'
                generation.fitness_score = stats['best_fitness']
                generation.conflicts_resolved = len(stats['conflicts'])
                generation.total_slots_filled = len(best_chromosome.genes)
                generation.completed_at = datetime.now()
                generation.save()
                
                messages.success(request, f'Timetable generated successfully! Fitness Score: {stats["best_fitness"]:.2f}')
                return redirect('timetable_view', academic_year=academic_year)
            
            else:
                generation.status = 'failed'
                generation.error_message = 'Failed to generate valid timetable'
                generation.save()
                messages.error(request, 'Failed to generate timetable')
                
        except Exception as e:
            logger.error(f"Error generating timetable: {e}")
            messages.error(request, f'Error generating timetable: {str(e)}')
    
    context = {
        'departments': Staff.DEPARTMENT_CHOICES,
        'current_year': datetime.now().year,
    }
    return render(request, 'timetable/generate.html', context)

def timetable_view(request, academic_year):
    """View generated timetables"""
    department = request.GET.get('department', 'all')
    view_type = request.GET.get('view', 'class')  # class, staff, room
    
    # Get timetable data
    timetables = Timetable.objects.filter(academic_year=academic_year)
    if department != 'all':
        timetables = timetables.filter(class_section__department=department)
    
    # Organize data based on view type
    if view_type == 'class':
        organized_data = _organize_by_class(timetables)
    elif view_type == 'staff':
        organized_data = _organize_by_staff(timetables)
    elif view_type == 'room':
        organized_data = _organize_by_room(timetables)
    else:
        organized_data = {}
    
    context = {
        'academic_year': academic_year,
        'department': department,
        'view_type': view_type,
        'timetables': organized_data,
        'departments': Staff.DEPARTMENT_CHOICES,
        'days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'],
        'slots': list(range(1, 9)),
        'slot_times': {
            1: '09:00-10:00', 2: '10:00-11:00', 3: '11:15-12:15', 4: '12:15-13:15',
            5: '14:00-15:00', 6: '15:00-16:00', 7: '16:15-17:15', 8: '17:15-18:15'
        }
    }
    return render(request, 'timetable/view.html', context)

def _organize_by_class(timetables):
    """Organize timetables by class section"""
    organized = {}
    for tt in timetables:
        class_id = tt.class_section.class_id
        if class_id not in organized:
            organized[class_id] = {
                'class_info': tt.class_section,
                'schedule': {}
            }
        
        day = tt.day
        if day not in organized[class_id]['schedule']:
            organized[class_id]['schedule'][day] = {}
        
        organized[class_id]['schedule'][day][tt.slot_number] = tt
    
    return organized

def _organize_by_staff(timetables):
    """Organize timetables by staff member"""
    organized = {}
    for tt in timetables:
        staff_id = tt.staff.staff_id
        if staff_id not in organized:
            organized[staff_id] = {
                'staff_info': tt.staff,
                'schedule': {}
            }
        
        day = tt.day
        if day not in organized[staff_id]['schedule']:
            organized[staff_id]['schedule'][day] = {}
        
        organized[staff_id]['schedule'][day][tt.slot_number] = tt
    
    return organized

def _organize_by_room(timetables):
    """Organize timetables by room"""
    organized = {}
    for tt in timetables:
        room_id = tt.room.room_id
        if room_id not in organized:
            organized[room_id] = {
                'room_info': tt.room,
                'schedule': {}
            }
        
        day = tt.day
        if day not in organized[room_id]['schedule']:
            organized[room_id]['schedule'][day] = {}
        
        organized[room_id]['schedule'][day][tt.slot_number] = tt
    
    return organized

# Substitution Views
def substitution_list(request):
    """List all substitutions"""
    substitutions = Substitution.objects.all().order_by('-created_at')
    paginator = Paginator(substitutions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_substitutions': substitutions.count()
    }
    return render(request, 'timetable/substitution_list.html', context)

def substitution_create(request):
    """Create new substitution"""
    if request.method == 'POST':
        try:
            timetable_id = int(request.POST.get('timetable_id'))
            substitution_date = datetime.strptime(request.POST.get('substitution_date'), '%Y-%m-%d').date()
            reason = request.POST.get('reason')
            
            engine = SubstitutionEngine()
            result = engine.find_substitute(timetable_id, substitution_date, reason)
            
            if result:
                messages.success(request, f'Substitute found! Confidence: {result["confidence_score"]:.1f}%')
                return redirect('substitution_list')
            else:
                messages.error(request, 'No suitable substitute found')
                
        except Exception as e:
            messages.error(request, f'Error creating substitution: {str(e)}')
    
    context = {
        'timetables': Timetable.objects.all().order_by('class_section__class_id', 'day', 'slot_number')
    }
    return render(request, 'timetable/substitution_form.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def substitution_approve(request, substitution_id):
    """Approve a substitution"""
    try:
        substitution = get_object_or_404(Substitution, substitution_id=substitution_id)
        substitution.is_approved = True
        substitution.approved_by = request.user.username if request.user.is_authenticated else 'system'
        substitution.save()
        
        return JsonResponse({'success': True, 'message': 'Substitution approved'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

# API Views
@csrf_exempt
def api_conflict_resolution(request):
    """API endpoint for automatic conflict resolution"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            academic_year = data.get('academic_year')
            semester = data.get('semester', 1)
            
            engine = SubstitutionEngine()
            result = engine.auto_resolve_conflicts(academic_year, semester)
            
            return JsonResponse({
                'success': True,
                'data': result
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def api_timetable_export(request):
    """API endpoint for exporting timetables"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            academic_year = data.get('academic_year')
            format_type = data.get('format', 'json')  # json, csv, pdf
            
            timetables = Timetable.objects.filter(academic_year=academic_year)
            
            if format_type == 'json':
                export_data = []
                for tt in timetables:
                    export_data.append({
                        'class': tt.class_section.class_id,
                        'day': tt.day,
                        'slot': tt.slot_number,
                        'time': f"{tt.start_time}-{tt.end_time}",
                        'subject': tt.subject.subject_code,
                        'subject_name': tt.subject.subject_name,
                        'staff': tt.staff.name,
                        'room': tt.room.room_id,
                        'is_lab': tt.is_lab,
                        'is_elective': tt.is_elective,
                    })
                
                return JsonResponse({
                    'success': True,
                    'data': export_data,
                    'count': len(export_data)
                })
            
            # Add more export formats as needed
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

def api_statistics(request):
    """API endpoint for dashboard statistics"""
    try:
        # Calculate various statistics
        stats = {
            'overview': {
                'total_staff': Staff.objects.count(),
                'total_subjects': Subject.objects.count(),
                'total_classes': ClassSection.objects.count(),
                'total_rooms': Room.objects.filter(is_active=True).count(),
                'total_timetables': Timetable.objects.count(),
            },
            'utilization': _calculate_utilization_stats(),
            'workload': _calculate_workload_stats(),
            'conflicts': _calculate_conflict_stats(),
        }
        
        return JsonResponse({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

def _calculate_utilization_stats():
    """Calculate room and time utilization statistics"""
    total_room_slots = 0
    occupied_room_slots = 0
    
    for room in Room.objects.filter(is_active=True):
        # 6 days * 8 slots = 48 slots per week per room
        total_room_slots += 48
        occupied_room_slots += Timetable.objects.filter(room=room).count()
    
    room_utilization = (occupied_room_slots / total_room_slots * 100) if total_room_slots > 0 else 0
    
    return {
        'room_utilization': round(room_utilization, 2),
        'total_room_slots': total_room_slots,
        'occupied_room_slots': occupied_room_slots,
    }

def _calculate_workload_stats():
    """Calculate staff workload statistics"""
    staff_workloads = []
    
    for staff in Staff.objects.all():
        current_load = Timetable.objects.filter(staff=staff).count()
        max_load = staff.max_sessions_per_week
        utilization = (current_load / max_load * 100) if max_load > 0 else 0
        
        staff_workloads.append({
            'staff_id': staff.staff_id,
            'name': staff.name,
            'current_load': current_load,
            'max_load': max_load,
            'utilization': round(utilization, 2)
        })
    
    # Calculate averages
    avg_utilization = sum(s['utilization'] for s in staff_workloads) / len(staff_workloads) if staff_workloads else 0
    
    return {
        'average_utilization': round(avg_utilization, 2),
        'staff_workloads': staff_workloads
    }

def _calculate_conflict_stats():
    """Calculate conflict statistics"""
    # This would be expanded based on conflict detection logic
    total_conflicts = 0
    resolved_conflicts = 0
    
    # Add actual conflict detection logic here
    
    return {
        'total_conflicts': total_conflicts,
        'resolved_conflicts': resolved_conflicts,
        'resolution_rate': (resolved_conflicts / total_conflicts * 100) if total_conflicts > 0 else 100
    }