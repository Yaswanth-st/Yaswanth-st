"""
Django Models for Timetable Management System
Developed by TEAM SPIDERMERN (SANJAY B, YASWANTH ST, ABISHECK AM)
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, time
import json

class Staff(models.Model):
    DESIGNATION_CHOICES = [
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('visiting_faculty', 'Visiting Faculty'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('cse', 'Computer Science Engineering'),
        ('ece', 'Electronics and Communication Engineering'),
        ('eee', 'Electrical and Electronics Engineering'),
        ('mech', 'Mechanical Engineering'),
        ('civil', 'Civil Engineering'),
        ('it', 'Information Technology'),
        ('ai_ml', 'Artificial Intelligence and Machine Learning'),
        ('cyber_security', 'Cyber Security'),
    ]
    
    staff_id = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=30, choices=DESIGNATION_CHOICES)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    email = models.EmailField(unique=True)
    max_sessions_per_week = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    max_sessions_per_day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    subjects_handled = models.JSONField(default=list)
    labs_handled = models.JSONField(default=list)
    electives_handled = models.JSONField(default=list)
    leave_dates = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'staff'
        verbose_name = 'Staff Member'
        verbose_name_plural = 'Staff Members'
    
    def __str__(self):
        return f"{self.name} ({self.staff_id})"

class Subject(models.Model):
    SUBJECT_TYPE_CHOICES = [
        ('core', 'Core Subject'),
        ('elective', 'Elective Subject'),
        ('lab', 'Laboratory'),
        ('project', 'Project Work'),
    ]
    
    subject_code = models.CharField(max_length=20, unique=True, primary_key=True)
    subject_name = models.CharField(max_length=100)
    subject_type = models.CharField(max_length=20, choices=SUBJECT_TYPE_CHOICES)
    department = models.CharField(max_length=20, choices=Staff.DEPARTMENT_CHOICES)
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    credits = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    hours_per_week = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    is_lab = models.BooleanField(default=False)
    lab_duration_hours = models.IntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(4)])
    prerequisite_subjects = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'subjects'
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
    
    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"

class ClassSection(models.Model):
    YEAR_CHOICES = [
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
    ]
    
    SECTION_CHOICES = [
        ('A', 'Section A'),
        ('B', 'Section B'),
        ('C', 'Section C'),
        ('D', 'Section D'),
    ]
    
    class_id = models.CharField(max_length=20, unique=True, primary_key=True)
    year = models.IntegerField(choices=YEAR_CHOICES)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)
    department = models.CharField(max_length=20, choices=Staff.DEPARTMENT_CHOICES)
    total_students = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    subjects = models.JSONField(default=list)
    labs = models.JSONField(default=list)
    electives = models.JSONField(default=list)
    working_days_per_week = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(7)])
    slots_per_day = models.IntegerField(default=8, validators=[MinValueValidator(1), MaxValueValidator(12)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'class_sections'
        verbose_name = 'Class Section'
        verbose_name_plural = 'Class Sections'
        unique_together = ['year', 'section', 'department']
    
    def __str__(self):
        return f"{self.year} Year {self.section} - {self.department.upper()}"

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('classroom', 'Classroom'),
        ('lab', 'Laboratory'),
        ('seminar_hall', 'Seminar Hall'),
        ('auditorium', 'Auditorium'),
    ]
    
    room_id = models.CharField(max_length=20, unique=True, primary_key=True)
    room_name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(500)])
    department = models.CharField(max_length=20, choices=Staff.DEPARTMENT_CHOICES, blank=True, null=True)
    floor = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    building = models.CharField(max_length=50)
    facilities = models.JSONField(default=list)
    availability = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rooms'
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
    
    def __str__(self):
        return f"{self.room_id} - {self.room_name}"

class Elective(models.Model):
    elective_id = models.CharField(max_length=20, unique=True, primary_key=True)
    elective_name = models.CharField(max_length=100)
    offering_department = models.CharField(max_length=20, choices=Staff.DEPARTMENT_CHOICES)
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    credits = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    max_students = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    enrolled_sections = models.JSONField(default=list)
    staff_assigned = models.ForeignKey(Staff, on_delete=models.CASCADE)
    hours_per_week = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'electives'
        verbose_name = 'Elective Subject'
        verbose_name_plural = 'Elective Subjects'
    
    def __str__(self):
        return f"{self.elective_id} - {self.elective_name}"

class Timetable(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]
    
    timetable_id = models.AutoField(primary_key=True)
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    slot_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_lab = models.BooleanField(default=False)
    is_elective = models.BooleanField(default=False)
    week_number = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(52)])
    academic_year = models.CharField(max_length=10, default='2024-25')
    is_substitute = models.BooleanField(default=False)
    original_staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='substituted_classes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'timetables'
        verbose_name = 'Timetable Entry'
        verbose_name_plural = 'Timetable Entries'
        unique_together = [
            ['class_section', 'day', 'slot_number', 'week_number'],
            ['staff', 'day', 'slot_number', 'week_number'],
            ['room', 'day', 'slot_number', 'week_number'],
        ]
    
    def __str__(self):
        return f"{self.class_section} - {self.day} Slot {self.slot_number}"

class Substitution(models.Model):
    substitution_id = models.AutoField(primary_key=True)
    original_timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='substitutions')
    substitute_staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    reason = models.TextField()
    date_of_substitution = models.DateField()
    is_approved = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'substitutions'
        verbose_name = 'Substitution'
        verbose_name_plural = 'Substitutions'
    
    def __str__(self):
        return f"Substitution for {self.original_timetable} on {self.date_of_substitution}"

class TimetableGeneration(models.Model):
    GENERATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    generation_id = models.AutoField(primary_key=True)
    academic_year = models.CharField(max_length=10)
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    department = models.CharField(max_length=20, choices=Staff.DEPARTMENT_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=20, choices=GENERATION_STATUS_CHOICES, default='pending')
    generation_parameters = models.JSONField(default=dict)
    fitness_score = models.FloatField(null=True, blank=True)
    conflicts_resolved = models.IntegerField(default=0)
    total_slots_filled = models.IntegerField(default=0)
    generated_by = models.CharField(max_length=100)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'timetable_generations'
        verbose_name = 'Timetable Generation'
        verbose_name_plural = 'Timetable Generations'
    
    def __str__(self):
        return f"Generation {self.generation_id} - {self.academic_year} Sem {self.semester}"