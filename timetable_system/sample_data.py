#!/usr/bin/env python3
"""
Sample Data Generator for Smart Timetable System
Developed by TEAM SPIDERMERN (SANJAY B, YASWANTH ST, ABISHECK AM)

This script populates the database with sample data for testing the timetable generation system.
"""

import os
import sys
import django
from datetime import datetime, time

# Setup Django environment
sys.path.append('/workspace/timetable_system')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timetable_project.settings')
django.setup()

from timetable.models import Staff, Subject, ClassSection, Room, Elective

def create_sample_staff():
    """Create sample staff members"""
    staff_data = [
        {
            'staff_id': 'CSE001',
            'name': 'Dr. Rajesh Kumar',
            'designation': 'professor',
            'department': 'cse',
            'email': 'rajesh.kumar@college.edu',
            'max_sessions_per_week': 18,
            'max_sessions_per_day': 6,
            'subjects_handled': ['CS101', 'CS301', 'CS401'],
            'labs_handled': ['CS101L', 'CS301L'],
            'electives_handled': ['CSE401']
        },
        {
            'staff_id': 'CSE002',
            'name': 'Prof. Priya Sharma',
            'designation': 'associate_professor',
            'department': 'cse',
            'email': 'priya.sharma@college.edu',
            'max_sessions_per_week': 16,
            'max_sessions_per_day': 5,
            'subjects_handled': ['CS102', 'CS202', 'CS302'],
            'labs_handled': ['CS102L', 'CS202L'],
            'electives_handled': ['CSE402']
        },
        {
            'staff_id': 'ECE001',
            'name': 'Dr. Suresh Reddy',
            'designation': 'professor',
            'department': 'ece',
            'email': 'suresh.reddy@college.edu',
            'max_sessions_per_week': 18,
            'max_sessions_per_day': 6,
            'subjects_handled': ['EC101', 'EC201', 'EC301'],
            'labs_handled': ['EC101L', 'EC201L'],
            'electives_handled': ['ECE401']
        },
        {
            'staff_id': 'MECH001',
            'name': 'Prof. Anita Singh',
            'designation': 'assistant_professor',
            'department': 'mech',
            'email': 'anita.singh@college.edu',
            'max_sessions_per_week': 14,
            'max_sessions_per_day': 5,
            'subjects_handled': ['ME101', 'ME201'],
            'labs_handled': ['ME101L'],
            'electives_handled': ['MECH401']
        },
        {
            'staff_id': 'IT001',
            'name': 'Dr. Vikram Patel',
            'designation': 'associate_professor',
            'department': 'it',
            'email': 'vikram.patel@college.edu',
            'max_sessions_per_week': 16,
            'max_sessions_per_day': 5,
            'subjects_handled': ['IT101', 'IT201', 'IT301'],
            'labs_handled': ['IT101L', 'IT201L'],
            'electives_handled': ['IT401']
        }
    ]
    
    for data in staff_data:
        staff, created = Staff.objects.get_or_create(
            staff_id=data['staff_id'],
            defaults=data
        )
        if created:
            print(f"✓ Created staff: {staff.name}")
        else:
            print(f"- Staff already exists: {staff.name}")

def create_sample_subjects():
    """Create sample subjects"""
    subjects_data = [
        # CSE Subjects
        {'subject_code': 'CS101', 'subject_name': 'Programming Fundamentals', 'subject_type': 'core', 'department': 'cse', 'semester': 1, 'credits': 4, 'hours_per_week': 4},
        {'subject_code': 'CS102', 'subject_name': 'Data Structures', 'subject_type': 'core', 'department': 'cse', 'semester': 2, 'credits': 4, 'hours_per_week': 4},
        {'subject_code': 'CS201', 'subject_name': 'Algorithms', 'subject_type': 'core', 'department': 'cse', 'semester': 3, 'credits': 4, 'hours_per_week': 3},
        {'subject_code': 'CS202', 'subject_name': 'Database Systems', 'subject_type': 'core', 'department': 'cse', 'semester': 4, 'credits': 4, 'hours_per_week': 3},
        {'subject_code': 'CS301', 'subject_name': 'Software Engineering', 'subject_type': 'core', 'department': 'cse', 'semester': 5, 'credits': 3, 'hours_per_week': 3},
        {'subject_code': 'CS302', 'subject_name': 'Computer Networks', 'subject_type': 'core', 'department': 'cse', 'semester': 6, 'credits': 3, 'hours_per_week': 3},
        {'subject_code': 'CS401', 'subject_name': 'Machine Learning', 'subject_type': 'core', 'department': 'cse', 'semester': 7, 'credits': 3, 'hours_per_week': 3},
        
        # Labs
        {'subject_code': 'CS101L', 'subject_name': 'Programming Lab', 'subject_type': 'lab', 'department': 'cse', 'semester': 1, 'credits': 2, 'hours_per_week': 2, 'is_lab': True},
        {'subject_code': 'CS102L', 'subject_name': 'Data Structures Lab', 'subject_type': 'lab', 'department': 'cse', 'semester': 2, 'credits': 2, 'hours_per_week': 2, 'is_lab': True},
        {'subject_code': 'CS202L', 'subject_name': 'Database Lab', 'subject_type': 'lab', 'department': 'cse', 'semester': 4, 'credits': 2, 'hours_per_week': 2, 'is_lab': True},
        {'subject_code': 'CS301L', 'subject_name': 'Software Engineering Lab', 'subject_type': 'lab', 'department': 'cse', 'semester': 5, 'credits': 2, 'hours_per_week': 2, 'is_lab': True},
        
        # ECE Subjects
        {'subject_code': 'EC101', 'subject_name': 'Circuit Analysis', 'subject_type': 'core', 'department': 'ece', 'semester': 1, 'credits': 4, 'hours_per_week': 4},
        {'subject_code': 'EC201', 'subject_name': 'Digital Electronics', 'subject_type': 'core', 'department': 'ece', 'semester': 3, 'credits': 4, 'hours_per_week': 3},
        {'subject_code': 'EC301', 'subject_name': 'Communication Systems', 'subject_type': 'core', 'department': 'ece', 'semester': 5, 'credits': 3, 'hours_per_week': 3},
        {'subject_code': 'EC101L', 'subject_name': 'Circuit Analysis Lab', 'subject_type': 'lab', 'department': 'ece', 'semester': 1, 'credits': 2, 'hours_per_week': 2, 'is_lab': True},
        {'subject_code': 'EC201L', 'subject_name': 'Digital Electronics Lab', 'subject_type': 'lab', 'department': 'ece', 'semester': 3, 'credits': 2, 'hours_per_week': 2, 'is_lab': True},
        
        # Mechanical Subjects
        {'subject_code': 'ME101', 'subject_name': 'Engineering Mechanics', 'subject_type': 'core', 'department': 'mech', 'semester': 1, 'credits': 4, 'hours_per_week': 4},
        {'subject_code': 'ME201', 'subject_name': 'Thermodynamics', 'subject_type': 'core', 'department': 'mech', 'semester': 3, 'credits': 4, 'hours_per_week': 3},
        {'subject_code': 'ME101L', 'subject_name': 'Engineering Workshop', 'subject_type': 'lab', 'department': 'mech', 'semester': 1, 'credits': 2, 'hours_per_week': 2, 'is_lab': True},
        
        # IT Subjects
        {'subject_code': 'IT101', 'subject_name': 'Web Technologies', 'subject_type': 'core', 'department': 'it', 'semester': 1, 'credits': 4, 'hours_per_week': 4},
        {'subject_code': 'IT201', 'subject_name': 'Mobile Computing', 'subject_type': 'core', 'department': 'it', 'semester': 3, 'credits': 3, 'hours_per_week': 3},
        {'subject_code': 'IT301', 'subject_name': 'Cloud Computing', 'subject_type': 'core', 'department': 'it', 'semester': 5, 'credits': 3, 'hours_per_week': 3},
        {'subject_code': 'IT101L', 'subject_name': 'Web Development Lab', 'subject_type': 'lab', 'department': 'it', 'semester': 1, 'credits': 2, 'hours_per_week': 2, 'is_lab': True},
        {'subject_code': 'IT201L', 'subject_name': 'Mobile App Lab', 'subject_type': 'lab', 'department': 'it', 'semester': 3, 'credits': 2, 'hours_per_week': 2, 'is_lab': True},
    ]
    
    for data in subjects_data:
        subject, created = Subject.objects.get_or_create(
            subject_code=data['subject_code'],
            defaults=data
        )
        if created:
            print(f"✓ Created subject: {subject.subject_name}")
        else:
            print(f"- Subject already exists: {subject.subject_name}")

def create_sample_classes():
    """Create sample class sections"""
    classes_data = [
        {
            'class_id': 'CSE_2A',
            'year': 2,
            'section': 'A',
            'department': 'cse',
            'total_students': 60,
            'subjects': [
                {'subject_code': 'CS101', 'hours_per_week': 4},
                {'subject_code': 'CS102', 'hours_per_week': 4},
                {'subject_code': 'CS201', 'hours_per_week': 3}
            ],
            'labs': [
                {'lab_code': 'CS101L', 'sessions_per_week': 1},
                {'lab_code': 'CS102L', 'sessions_per_week': 1}
            ],
            'electives': ['CSE401', 'CSE402']
        },
        {
            'class_id': 'CSE_2B',
            'year': 2,
            'section': 'B',
            'department': 'cse',
            'total_students': 58,
            'subjects': [
                {'subject_code': 'CS101', 'hours_per_week': 4},
                {'subject_code': 'CS102', 'hours_per_week': 4},
                {'subject_code': 'CS201', 'hours_per_week': 3}
            ],
            'labs': [
                {'lab_code': 'CS101L', 'sessions_per_week': 1},
                {'lab_code': 'CS102L', 'sessions_per_week': 1}
            ],
            'electives': ['CSE401']
        },
        {
            'class_id': 'ECE_2A',
            'year': 2,
            'section': 'A',
            'department': 'ece',
            'total_students': 55,
            'subjects': [
                {'subject_code': 'EC101', 'hours_per_week': 4},
                {'subject_code': 'EC201', 'hours_per_week': 3}
            ],
            'labs': [
                {'lab_code': 'EC101L', 'sessions_per_week': 1},
                {'lab_code': 'EC201L', 'sessions_per_week': 1}
            ],
            'electives': ['ECE401']
        },
        {
            'class_id': 'MECH_2A',
            'year': 2,
            'section': 'A',
            'department': 'mech',
            'total_students': 50,
            'subjects': [
                {'subject_code': 'ME101', 'hours_per_week': 4},
                {'subject_code': 'ME201', 'hours_per_week': 3}
            ],
            'labs': [
                {'lab_code': 'ME101L', 'sessions_per_week': 1}
            ],
            'electives': ['MECH401']
        },
        {
            'class_id': 'IT_2A',
            'year': 2,
            'section': 'A',
            'department': 'it',
            'total_students': 45,
            'subjects': [
                {'subject_code': 'IT101', 'hours_per_week': 4},
                {'subject_code': 'IT201', 'hours_per_week': 3}
            ],
            'labs': [
                {'lab_code': 'IT101L', 'sessions_per_week': 1},
                {'lab_code': 'IT201L', 'sessions_per_week': 1}
            ],
            'electives': ['IT401']
        }
    ]
    
    for data in classes_data:
        class_section, created = ClassSection.objects.get_or_create(
            class_id=data['class_id'],
            defaults=data
        )
        if created:
            print(f"✓ Created class: {class_section}")
        else:
            print(f"- Class already exists: {class_section}")

def create_sample_rooms():
    """Create sample rooms"""
    rooms_data = [
        # Classrooms
        {'room_id': 'CR101', 'room_name': 'Classroom 101', 'room_type': 'classroom', 'capacity': 70, 'floor': 1, 'building': 'Academic Block A', 'facilities': ['projector', 'ac', 'whiteboard']},
        {'room_id': 'CR102', 'room_name': 'Classroom 102', 'room_type': 'classroom', 'capacity': 65, 'floor': 1, 'building': 'Academic Block A', 'facilities': ['projector', 'whiteboard']},
        {'room_id': 'CR201', 'room_name': 'Classroom 201', 'room_type': 'classroom', 'capacity': 60, 'floor': 2, 'building': 'Academic Block A', 'facilities': ['projector', 'ac', 'whiteboard']},
        {'room_id': 'CR202', 'room_name': 'Classroom 202', 'room_type': 'classroom', 'capacity': 55, 'floor': 2, 'building': 'Academic Block A', 'facilities': ['projector', 'whiteboard']},
        {'room_id': 'CR301', 'room_name': 'Classroom 301', 'room_type': 'classroom', 'capacity': 50, 'floor': 3, 'building': 'Academic Block A', 'facilities': ['projector', 'ac', 'whiteboard']},
        
        # Computer Labs
        {'room_id': 'LAB_CS1', 'room_name': 'Computer Lab 1', 'room_type': 'lab', 'capacity': 30, 'department': 'cse', 'floor': 1, 'building': 'Lab Block', 'facilities': ['computers', 'projector', 'ac']},
        {'room_id': 'LAB_CS2', 'room_name': 'Computer Lab 2', 'room_type': 'lab', 'capacity': 30, 'department': 'cse', 'floor': 1, 'building': 'Lab Block', 'facilities': ['computers', 'projector', 'ac']},
        {'room_id': 'LAB_CS3', 'room_name': 'Computer Lab 3', 'room_type': 'lab', 'capacity': 25, 'department': 'it', 'floor': 2, 'building': 'Lab Block', 'facilities': ['computers', 'projector', 'ac']},
        
        # Other Labs
        {'room_id': 'LAB_ECE1', 'room_name': 'Electronics Lab 1', 'room_type': 'lab', 'capacity': 20, 'department': 'ece', 'floor': 2, 'building': 'Lab Block', 'facilities': ['equipment', 'projector']},
        {'room_id': 'LAB_ECE2', 'room_name': 'Digital Lab', 'room_type': 'lab', 'capacity': 20, 'department': 'ece', 'floor': 2, 'building': 'Lab Block', 'facilities': ['equipment', 'projector']},
        {'room_id': 'LAB_MECH1', 'room_name': 'Workshop Lab', 'room_type': 'lab', 'capacity': 25, 'department': 'mech', 'floor': 0, 'building': 'Workshop Block', 'facilities': ['machines', 'tools']},
        
        # Seminar Halls
        {'room_id': 'SH101', 'room_name': 'Seminar Hall 1', 'room_type': 'seminar_hall', 'capacity': 100, 'floor': 1, 'building': 'Admin Block', 'facilities': ['projector', 'ac', 'audio_system']},
        {'room_id': 'SH201', 'room_name': 'Seminar Hall 2', 'room_type': 'seminar_hall', 'capacity': 80, 'floor': 2, 'building': 'Admin Block', 'facilities': ['projector', 'ac', 'audio_system']},
    ]
    
    for data in rooms_data:
        room, created = Room.objects.get_or_create(
            room_id=data['room_id'],
            defaults=data
        )
        if created:
            print(f"✓ Created room: {room.room_name}")
        else:
            print(f"- Room already exists: {room.room_name}")

def create_sample_electives():
    """Create sample elective subjects"""
    electives_data = [
        {
            'elective_id': 'CSE401',
            'elective_name': 'Artificial Intelligence',
            'offering_department': 'cse',
            'semester': 7,
            'credits': 3,
            'max_students': 40,
            'hours_per_week': 3,
            'staff_assigned_id': 'CSE001',
            'enrolled_sections': ['CSE_2A', 'CSE_2B', 'IT_2A']
        },
        {
            'elective_id': 'CSE402',
            'elective_name': 'Blockchain Technology',
            'offering_department': 'cse',
            'semester': 7,
            'credits': 3,
            'max_students': 30,
            'hours_per_week': 3,
            'staff_assigned_id': 'CSE002',
            'enrolled_sections': ['CSE_2A']
        },
        {
            'elective_id': 'ECE401',
            'elective_name': 'Embedded Systems',
            'offering_department': 'ece',
            'semester': 7,
            'credits': 3,
            'max_students': 35,
            'hours_per_week': 3,
            'staff_assigned_id': 'ECE001',
            'enrolled_sections': ['ECE_2A']
        },
        {
            'elective_id': 'MECH401',
            'elective_name': 'Robotics Engineering',
            'offering_department': 'mech',
            'semester': 7,
            'credits': 3,
            'max_students': 25,
            'hours_per_week': 3,
            'staff_assigned_id': 'MECH001',
            'enrolled_sections': ['MECH_2A']
        },
        {
            'elective_id': 'IT401',
            'elective_name': 'DevOps and CI/CD',
            'offering_department': 'it',
            'semester': 7,
            'credits': 3,
            'max_students': 30,
            'hours_per_week': 3,
            'staff_assigned_id': 'IT001',
            'enrolled_sections': ['IT_2A']
        }
    ]
    
    for data in electives_data:
        try:
            staff = Staff.objects.get(staff_id=data['staff_assigned_id'])
            elective_data = data.copy()
            elective_data['staff_assigned'] = staff
            del elective_data['staff_assigned_id']
            
            elective, created = Elective.objects.get_or_create(
                elective_id=data['elective_id'],
                defaults=elective_data
            )
            if created:
                print(f"✓ Created elective: {elective.elective_name}")
            else:
                print(f"- Elective already exists: {elective.elective_name}")
        except Staff.DoesNotExist:
            print(f"✗ Staff {data['staff_assigned_id']} not found for elective {data['elective_name']}")

def main():
    """Main function to populate sample data"""
    print("🎓 Smart Timetable System - Sample Data Generator")
    print("=" * 60)
    print("Developed by TEAM SPIDERMERN")
    print("SANJAY B | YASWANTH ST | ABISHECK AM")
    print("=" * 60)
    
    print("\n📊 Creating sample data...")
    
    print("\n👥 Creating Staff Members...")
    create_sample_staff()
    
    print("\n📚 Creating Subjects...")
    create_sample_subjects()
    
    print("\n🎓 Creating Class Sections...")
    create_sample_classes()
    
    print("\n🏢 Creating Rooms...")
    create_sample_rooms()
    
    print("\n🎯 Creating Elective Subjects...")
    create_sample_electives()
    
    print("\n✅ Sample data creation completed!")
    print("\nSummary:")
    print(f"- Staff Members: {Staff.objects.count()}")
    print(f"- Subjects: {Subject.objects.count()}")
    print(f"- Class Sections: {ClassSection.objects.count()}")
    print(f"- Rooms: {Room.objects.count()}")
    print(f"- Electives: {Elective.objects.count()}")
    
    print("\n🚀 You can now:")
    print("1. Access the admin panel at: http://localhost:8000/admin/")
    print("2. Generate timetables at: http://localhost:8000/timetable/generate/")
    print("3. View the dashboard at: http://localhost:8000/")

if __name__ == '__main__':
    main()