"""
Django Admin Configuration for Timetable Management System
Developed by TEAM SPIDERMERN (SANJAY B, YASWANTH ST, ABISHECK AM)
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import (
    Staff, Subject, ClassSection, Room, Timetable, 
    Elective, Substitution, TimetableGeneration
)

# Custom Admin Site Configuration
admin.site.site_header = "Smart Timetable Management System"
admin.site.site_title = "TEAM SPIDERMERN Timetable System"
admin.site.index_title = "Developed by SANJAY B, YASWANTH ST, ABISHECK AM"

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['staff_id', 'name', 'designation', 'department', 'email', 'max_sessions_per_week', 'current_load']
    list_filter = ['department', 'designation', 'created_at']
    search_fields = ['staff_id', 'name', 'email']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('staff_id', 'name', 'designation', 'department', 'email')
        }),
        ('Workload Settings', {
            'fields': ('max_sessions_per_week', 'max_sessions_per_day')
        }),
        ('Subject Assignments', {
            'fields': ('subjects_handled', 'labs_handled', 'electives_handled'),
            'classes': ('collapse',)
        }),
        ('Leave Management', {
            'fields': ('leave_dates',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def current_load(self, obj):
        count = Timetable.objects.filter(staff=obj).count()
        if count > obj.max_sessions_per_week:
            return format_html('<span style="color: red;">{}</span>', count)
        elif count > obj.max_sessions_per_week * 0.8:
            return format_html('<span style="color: orange;">{}</span>', count)
        else:
            return count
    current_load.short_description = 'Current Load'

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_code', 'subject_name', 'subject_type', 'department', 'semester', 'credits', 'hours_per_week', 'is_lab']
    list_filter = ['subject_type', 'department', 'semester', 'is_lab', 'created_at']
    search_fields = ['subject_code', 'subject_name']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('subject_code', 'subject_name', 'subject_type', 'department')
        }),
        ('Academic Details', {
            'fields': ('semester', 'credits', 'hours_per_week')
        }),
        ('Lab Configuration', {
            'fields': ('is_lab', 'lab_duration_hours'),
            'classes': ('collapse',)
        }),
        ('Prerequisites', {
            'fields': ('prerequisite_subjects',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(ClassSection)
class ClassSectionAdmin(admin.ModelAdmin):
    list_display = ['class_id', 'year', 'section', 'department', 'total_students', 'working_days_per_week', 'slots_per_day']
    list_filter = ['year', 'section', 'department', 'created_at']
    search_fields = ['class_id']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('class_id', 'year', 'section', 'department', 'total_students')
        }),
        ('Schedule Configuration', {
            'fields': ('working_days_per_week', 'slots_per_day')
        }),
        ('Subject Assignments', {
            'fields': ('subjects', 'labs', 'electives'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_id', 'room_name', 'room_type', 'capacity', 'department', 'floor', 'building', 'is_active', 'utilization']
    list_filter = ['room_type', 'department', 'floor', 'building', 'is_active', 'created_at']
    search_fields = ['room_id', 'room_name']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('room_id', 'room_name', 'room_type', 'capacity')
        }),
        ('Location Details', {
            'fields': ('department', 'floor', 'building')
        }),
        ('Facilities & Availability', {
            'fields': ('facilities', 'availability'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def utilization(self, obj):
        if obj.is_active:
            count = Timetable.objects.filter(room=obj).count()
            max_slots = 48  # 6 days * 8 slots
            utilization_rate = (count / max_slots) * 100
            if utilization_rate > 80:
                return format_html('<span style="color: red;">{:.1f}%</span>', utilization_rate)
            elif utilization_rate > 60:
                return format_html('<span style="color: orange;">{:.1f}%</span>', utilization_rate)
            else:
                return f"{utilization_rate:.1f}%"
        return "Inactive"
    utilization.short_description = 'Utilization %'

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['timetable_id', 'class_section', 'day', 'slot_number', 'time_display', 'subject', 'staff', 'room', 'is_lab', 'is_elective']
    list_filter = ['day', 'is_lab', 'is_elective', 'academic_year', 'week_number', 'created_at']
    search_fields = ['class_section__class_id', 'subject__subject_code', 'staff__name', 'room__room_id']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Schedule Information', {
            'fields': ('class_section', 'day', 'slot_number', 'start_time', 'end_time')
        }),
        ('Assignment Details', {
            'fields': ('subject', 'staff', 'room')
        }),
        ('Flags', {
            'fields': ('is_lab', 'is_elective', 'is_substitute')
        }),
        ('Academic Context', {
            'fields': ('academic_year', 'week_number')
        }),
        ('Substitution Details', {
            'fields': ('original_staff',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def time_display(self, obj):
        return f"{obj.start_time.strftime('%H:%M')}-{obj.end_time.strftime('%H:%M')}"
    time_display.short_description = 'Time'
    
    actions = ['duplicate_for_next_week']
    
    def duplicate_for_next_week(self, request, queryset):
        duplicated = 0
        for timetable in queryset:
            timetable.pk = None
            timetable.week_number += 1
            timetable.save()
            duplicated += 1
        self.message_user(request, f'Successfully duplicated {duplicated} timetable entries for next week.')
    duplicate_for_next_week.short_description = 'Duplicate selected entries for next week'

@admin.register(Elective)
class ElectiveAdmin(admin.ModelAdmin):
    list_display = ['elective_id', 'elective_name', 'offering_department', 'semester', 'credits', 'staff_assigned', 'max_students', 'enrolled_count']
    list_filter = ['offering_department', 'semester', 'created_at']
    search_fields = ['elective_id', 'elective_name', 'staff_assigned__name']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('elective_id', 'elective_name', 'offering_department')
        }),
        ('Academic Details', {
            'fields': ('semester', 'credits', 'hours_per_week')
        }),
        ('Assignment & Enrollment', {
            'fields': ('staff_assigned', 'max_students', 'enrolled_sections')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def enrolled_count(self, obj):
        return len(obj.enrolled_sections)
    enrolled_count.short_description = 'Enrolled Sections'

@admin.register(Substitution)
class SubstitutionAdmin(admin.ModelAdmin):
    list_display = ['substitution_id', 'original_timetable_display', 'substitute_staff', 'date_of_substitution', 'reason_short', 'is_approved', 'approval_status']
    list_filter = ['is_approved', 'date_of_substitution', 'created_at']
    search_fields = ['original_timetable__subject__subject_code', 'substitute_staff__name', 'reason']
    readonly_fields = ['created_at']
    date_hierarchy = 'date_of_substitution'
    
    fieldsets = (
        ('Substitution Details', {
            'fields': ('original_timetable', 'substitute_staff', 'date_of_substitution')
        }),
        ('Reason & Approval', {
            'fields': ('reason', 'is_approved', 'approved_by')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def original_timetable_display(self, obj):
        tt = obj.original_timetable
        return f"{tt.class_section.class_id} - {tt.subject.subject_code} ({tt.day} Slot {tt.slot_number})"
    original_timetable_display.short_description = 'Original Class'
    
    def reason_short(self, obj):
        return obj.reason[:50] + "..." if len(obj.reason) > 50 else obj.reason
    reason_short.short_description = 'Reason'
    
    def approval_status(self, obj):
        if obj.is_approved:
            return format_html('<span style="color: green;">✓ Approved</span>')
        else:
            return format_html('<span style="color: red;">✗ Pending</span>')
    approval_status.short_description = 'Status'
    
    actions = ['approve_substitutions']
    
    def approve_substitutions(self, request, queryset):
        updated = queryset.update(is_approved=True, approved_by=request.user.username)
        self.message_user(request, f'Successfully approved {updated} substitutions.')
    approve_substitutions.short_description = 'Approve selected substitutions'

@admin.register(TimetableGeneration)
class TimetableGenerationAdmin(admin.ModelAdmin):
    list_display = ['generation_id', 'academic_year', 'semester', 'department', 'status', 'fitness_score', 'conflicts_resolved', 'duration', 'generated_by']
    list_filter = ['status', 'academic_year', 'semester', 'department', 'created_at']
    search_fields = ['academic_year', 'generated_by']
    readonly_fields = ['created_at', 'started_at', 'completed_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Generation Parameters', {
            'fields': ('academic_year', 'semester', 'department', 'generated_by')
        }),
        ('Status & Results', {
            'fields': ('status', 'fitness_score', 'conflicts_resolved', 'total_slots_filled')
        }),
        ('Configuration', {
            'fields': ('generation_parameters',),
            'classes': ('collapse',)
        }),
        ('Error Information', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'started_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def duration(self, obj):
        if obj.started_at and obj.completed_at:
            duration = obj.completed_at - obj.started_at
            return str(duration).split('.')[0]  # Remove microseconds
        return "N/A"
    duration.short_description = 'Duration'
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status in ['completed', 'failed']:
            return self.readonly_fields + ['status', 'fitness_score', 'conflicts_resolved', 'total_slots_filled']
        return self.readonly_fields

# Custom admin actions
def regenerate_timetable(modeladmin, request, queryset):
    """Custom action to regenerate timetables"""
    for generation in queryset:
        if generation.status != 'in_progress':
            # Trigger regeneration logic here
            generation.status = 'pending'
            generation.save()
    modeladmin.message_user(request, f'Marked {queryset.count()} generations for regeneration.')

regenerate_timetable.short_description = 'Mark for regeneration'

# Add the action to TimetableGenerationAdmin
TimetableGenerationAdmin.actions = ['regenerate_timetable'] + list(TimetableGenerationAdmin.actions or [])