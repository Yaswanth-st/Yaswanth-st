"""
Substitution Engine for Automatic Staff Replacement
Developed by TEAM SPIDERMERN (SANJAY B, YASWANTH ST, ABISHECK AM)
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
from .mongodb import mongo_collections
import logging

logger = logging.getLogger(__name__)

class SubstitutionEngine:
    """
    Intelligent substitution engine that automatically finds suitable staff
    replacements when original staff is on leave or unavailable
    """
    
    def __init__(self):
        self.substitution_rules = {
            'same_department_priority': True,
            'subject_expertise_required': True,
            'workload_balance': True,
            'min_advance_notice_hours': 2,
            'max_daily_substitutions': 3,
        }
    
    def find_substitute(self, original_timetable_id: int, 
                       substitution_date: date, 
                       reason: str = "Staff on leave") -> Optional[Dict]:
        """
        Find the best substitute for a given timetable entry
        
        Args:
            original_timetable_id: ID of the original timetable entry
            substitution_date: Date when substitution is needed
            reason: Reason for substitution
            
        Returns:
            Dictionary with substitute details or None if no suitable substitute found
        """
        try:
            from .models import Staff, Subject, ClassSection, Room, Timetable, Substitution
            
            # Get original timetable entry
            original_entry = Timetable.objects.get(timetable_id=original_timetable_id)
            
            # Find potential substitutes
            candidates = self._find_substitute_candidates(original_entry, substitution_date)
            
            if not candidates:
                logger.warning(f"No substitute candidates found for timetable {original_timetable_id}")
                return None
            
            # Rank candidates based on suitability
            ranked_candidates = self._rank_substitute_candidates(
                candidates, original_entry, substitution_date
            )
            
            # Select best candidate
            best_candidate = ranked_candidates[0] if ranked_candidates else None
            
            if best_candidate:
                # Create substitution record
                substitution = self._create_substitution_record(
                    original_entry, best_candidate, substitution_date, reason
                )
                
                return {
                    'substitute_staff': best_candidate,
                    'substitution_id': substitution.substitution_id,
                    'confidence_score': best_candidate.get('score', 0),
                    'reason': reason,
                    'date': substitution_date
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding substitute: {e}")
            return None
    
    def _find_substitute_candidates(self, original_entry: Timetable, 
                                   substitution_date: date) -> List[Dict]:
        """Find all potential substitute candidates"""
        candidates = []
        
        # Get all staff members
        all_staff = Staff.objects.all()
        
        for staff in all_staff:
            # Skip if it's the same staff member
            if staff.staff_id == original_entry.staff.staff_id:
                continue
            
            # Check if staff is available on the given date and time
            if self._is_staff_available(staff, original_entry, substitution_date):
                # Check if staff can handle the subject
                if self._can_handle_subject(staff, original_entry):
                    candidates.append({
                        'staff': staff,
                        'staff_id': staff.staff_id,
                        'name': staff.name,
                        'department': staff.department,
                        'designation': staff.designation,
                        'subjects': staff.subjects_handled,
                        'labs': staff.labs_handled,
                        'electives': staff.electives_handled,
                    })
        
        logger.info(f"Found {len(candidates)} substitute candidates")
        return candidates
    
    def _is_staff_available(self, staff: Staff, original_entry: Timetable, 
                           substitution_date: date) -> bool:
        """Check if staff is available at the required time"""
        
        # Check if staff is on leave on that date
        if substitution_date.isoformat() in staff.leave_dates:
            return False
        
        # Check if staff has any conflicting classes at the same time
        conflicting_entries = Timetable.objects.filter(
            staff=staff,
            day=original_entry.day,
            slot_number=original_entry.slot_number,
            week_number=original_entry.week_number
        ).exclude(timetable_id=original_entry.timetable_id)
        
        if conflicting_entries.exists():
            return False
        
        # Check workload limits
        daily_load = self._get_staff_daily_load(staff, original_entry.day, original_entry.week_number)
        if daily_load >= staff.max_sessions_per_day:
            return False
        
        weekly_load = self._get_staff_weekly_load(staff, original_entry.week_number)
        if weekly_load >= staff.max_sessions_per_week:
            return False
        
        return True
    
    def _can_handle_subject(self, staff: Staff, original_entry: Timetable) -> bool:
        """Check if staff can handle the subject/lab"""
        subject_code = original_entry.subject.subject_code
        
        # Check if it's a lab or regular subject
        if original_entry.is_lab:
            return subject_code in staff.labs_handled
        elif original_entry.is_elective:
            return subject_code in staff.electives_handled
        else:
            return subject_code in staff.subjects_handled
    
    def _get_staff_daily_load(self, staff: Staff, day: str, week_number: int) -> int:
        """Get staff's current daily teaching load"""
        return Timetable.objects.filter(
            staff=staff,
            day=day,
            week_number=week_number
        ).count()
    
    def _get_staff_weekly_load(self, staff: Staff, week_number: int) -> int:
        """Get staff's current weekly teaching load"""
        return Timetable.objects.filter(
            staff=staff,
            week_number=week_number
        ).count()
    
    def _rank_substitute_candidates(self, candidates: List[Dict], 
                                   original_entry: Timetable, 
                                   substitution_date: date) -> List[Dict]:
        """Rank substitute candidates based on suitability"""
        
        for candidate in candidates:
            score = 0
            staff = candidate['staff']
            
            # Same department bonus
            if staff.department == original_entry.staff.department:
                score += 30
            
            # Same designation bonus
            if staff.designation == original_entry.staff.designation:
                score += 20
            
            # Subject expertise bonus
            subject_code = original_entry.subject.subject_code
            if original_entry.is_lab and subject_code in staff.labs_handled:
                score += 40
            elif original_entry.is_elective and subject_code in staff.electives_handled:
                score += 35
            elif not original_entry.is_lab and subject_code in staff.subjects_handled:
                score += 40
            
            # Workload balance - prefer staff with lower current load
            current_weekly_load = self._get_staff_weekly_load(staff, original_entry.week_number)
            workload_ratio = current_weekly_load / staff.max_sessions_per_week
            workload_bonus = max(0, 20 * (1 - workload_ratio))
            score += workload_bonus
            
            # Experience bonus based on designation
            designation_scores = {
                'professor': 25,
                'associate_professor': 20,
                'assistant_professor': 15,
                'lecturer': 10,
                'visiting_faculty': 5,
            }
            score += designation_scores.get(staff.designation, 0)
            
            # Availability bonus (fewer conflicts = higher score)
            daily_conflicts = self._count_daily_conflicts(staff, original_entry.day, original_entry.week_number)
            availability_bonus = max(0, 15 - daily_conflicts * 3)
            score += availability_bonus
            
            candidate['score'] = score
        
        # Sort by score (descending)
        return sorted(candidates, key=lambda x: x['score'], reverse=True)
    
    def _count_daily_conflicts(self, staff: Staff, day: str, week_number: int) -> int:
        """Count potential conflicts for staff on a given day"""
        return Timetable.objects.filter(
            staff=staff,
            day=day,
            week_number=week_number
        ).count()
    
    def _create_substitution_record(self, original_entry: Timetable, 
                                   substitute_candidate: Dict, 
                                   substitution_date: date, 
                                   reason: str) -> Substitution:
        """Create a substitution record in the database"""
        
        substitution = Substitution.objects.create(
            original_timetable=original_entry,
            substitute_staff=substitute_candidate['staff'],
            reason=reason,
            date_of_substitution=substitution_date,
            is_approved=False,  # Requires approval
            created_at=datetime.now()
        )
        
        logger.info(f"Created substitution record {substitution.substitution_id}")
        return substitution
    
    def auto_resolve_conflicts(self, academic_year: str, semester: int) -> Dict:
        """
        Automatically resolve scheduling conflicts for a given academic year and semester
        """
        conflicts_resolved = 0
        conflicts_found = 0
        resolution_report = []
        
        try:
            # Find all conflicting timetable entries
            conflicts = self._detect_scheduling_conflicts(academic_year, semester)
            conflicts_found = len(conflicts)
            
            logger.info(f"Found {conflicts_found} scheduling conflicts")
            
            for conflict in conflicts:
                resolution = self._resolve_single_conflict(conflict)
                if resolution:
                    conflicts_resolved += 1
                    resolution_report.append(resolution)
                    logger.info(f"Resolved conflict: {resolution['description']}")
                else:
                    resolution_report.append({
                        'conflict': conflict,
                        'status': 'unresolved',
                        'description': f"Could not resolve conflict {conflict['type']}"
                    })
            
            return {
                'total_conflicts': conflicts_found,
                'resolved_conflicts': conflicts_resolved,
                'resolution_rate': conflicts_resolved / conflicts_found if conflicts_found > 0 else 1.0,
                'resolutions': resolution_report
            }
            
        except Exception as e:
            logger.error(f"Error in auto conflict resolution: {e}")
            return {
                'error': str(e),
                'total_conflicts': 0,
                'resolved_conflicts': 0,
                'resolution_rate': 0.0
            }
    
    def _detect_scheduling_conflicts(self, academic_year: str, semester: int) -> List[Dict]:
        """Detect various types of scheduling conflicts"""
        conflicts = []
        
        # Get all timetable entries for the academic year and semester
        timetable_entries = Timetable.objects.filter(academic_year=academic_year)
        
        # Check for staff double booking
        staff_schedule = {}
        for entry in timetable_entries:
            key = (entry.staff.staff_id, entry.day, entry.slot_number, entry.week_number)
            if key in staff_schedule:
                conflicts.append({
                    'type': 'staff_double_booking',
                    'staff_id': entry.staff.staff_id,
                    'day': entry.day,
                    'slot': entry.slot_number,
                    'week': entry.week_number,
                    'entries': [staff_schedule[key], entry.timetable_id]
                })
            else:
                staff_schedule[key] = entry.timetable_id
        
        # Check for room double booking
        room_schedule = {}
        for entry in timetable_entries:
            key = (entry.room.room_id, entry.day, entry.slot_number, entry.week_number)
            if key in room_schedule:
                conflicts.append({
                    'type': 'room_double_booking',
                    'room_id': entry.room.room_id,
                    'day': entry.day,
                    'slot': entry.slot_number,
                    'week': entry.week_number,
                    'entries': [room_schedule[key], entry.timetable_id]
                })
            else:
                room_schedule[key] = entry.timetable_id
        
        # Check for class double booking
        class_schedule = {}
        for entry in timetable_entries:
            key = (entry.class_section.class_id, entry.day, entry.slot_number, entry.week_number)
            if key in class_schedule:
                conflicts.append({
                    'type': 'class_double_booking',
                    'class_id': entry.class_section.class_id,
                    'day': entry.day,
                    'slot': entry.slot_number,
                    'week': entry.week_number,
                    'entries': [class_schedule[key], entry.timetable_id]
                })
            else:
                class_schedule[key] = entry.timetable_id
        
        return conflicts
    
    def _resolve_single_conflict(self, conflict: Dict) -> Optional[Dict]:
        """Resolve a single scheduling conflict"""
        
        try:
            if conflict['type'] == 'staff_double_booking':
                return self._resolve_staff_conflict(conflict)
            elif conflict['type'] == 'room_double_booking':
                return self._resolve_room_conflict(conflict)
            elif conflict['type'] == 'class_double_booking':
                return self._resolve_class_conflict(conflict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error resolving conflict: {e}")
            return None
    
    def _resolve_staff_conflict(self, conflict: Dict) -> Optional[Dict]:
        """Resolve staff double booking conflict"""
        
        # Get the conflicting timetable entries
        entry_ids = conflict['entries']
        entries = [Timetable.objects.get(timetable_id=eid) for eid in entry_ids]
        
        # Strategy: Move one of the entries to a different time slot
        for entry in entries:
            new_slot = self._find_alternative_slot(entry)
            if new_slot:
                old_slot = entry.slot_number
                entry.slot_number = new_slot['slot']
                entry.start_time = new_slot['start_time']
                entry.end_time = new_slot['end_time']
                entry.save()
                
                return {
                    'type': 'staff_conflict_resolved',
                    'timetable_id': entry.timetable_id,
                    'staff_id': conflict['staff_id'],
                    'old_slot': old_slot,
                    'new_slot': new_slot['slot'],
                    'description': f"Moved {entry.subject.subject_code} from slot {old_slot} to {new_slot['slot']}"
                }
        
        return None
    
    def _resolve_room_conflict(self, conflict: Dict) -> Optional[Dict]:
        """Resolve room double booking conflict"""
        
        entry_ids = conflict['entries']
        entries = [Timetable.objects.get(timetable_id=eid) for eid in entry_ids]
        
        # Strategy: Assign one entry to a different room
        for entry in entries:
            alternative_room = self._find_alternative_room(entry)
            if alternative_room:
                old_room = entry.room.room_id
                entry.room = alternative_room
                entry.save()
                
                return {
                    'type': 'room_conflict_resolved',
                    'timetable_id': entry.timetable_id,
                    'old_room': old_room,
                    'new_room': alternative_room.room_id,
                    'description': f"Moved {entry.subject.subject_code} from {old_room} to {alternative_room.room_id}"
                }
        
        return None
    
    def _resolve_class_conflict(self, conflict: Dict) -> Optional[Dict]:
        """Resolve class double booking conflict"""
        
        entry_ids = conflict['entries']
        entries = [Timetable.objects.get(timetable_id=eid) for eid in entry_ids]
        
        # Strategy: Move one entry to a different time slot
        for entry in entries:
            new_slot = self._find_alternative_slot(entry)
            if new_slot:
                old_slot = entry.slot_number
                entry.slot_number = new_slot['slot']
                entry.start_time = new_slot['start_time']
                entry.end_time = new_slot['end_time']
                entry.save()
                
                return {
                    'type': 'class_conflict_resolved',
                    'timetable_id': entry.timetable_id,
                    'class_id': conflict['class_id'],
                    'old_slot': old_slot,
                    'new_slot': new_slot['slot'],
                    'description': f"Moved {entry.subject.subject_code} from slot {old_slot} to {new_slot['slot']}"
                }
        
        return None
    
    def _find_alternative_slot(self, entry: Timetable) -> Optional[Dict]:
        """Find an alternative time slot for a timetable entry"""
        
        class_section = entry.class_section
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        working_days = days[:class_section.working_days_per_week]
        
        slot_times = {
            1: (time(9, 0), time(10, 0)),
            2: (time(10, 0), time(11, 0)),
            3: (time(11, 15), time(12, 15)),
            4: (time(12, 15), time(13, 15)),
            5: (time(14, 0), time(15, 0)),
            6: (time(15, 0), time(16, 0)),
            7: (time(16, 15), time(17, 15)),
            8: (time(17, 15), time(18, 15)),
        }
        
        for day in working_days:
            for slot in range(1, class_section.slots_per_day + 1):
                # Check if slot is available for class, staff, and room
                if self._is_slot_available(entry, day, slot):
                    return {
                        'day': day,
                        'slot': slot,
                        'start_time': slot_times[slot][0],
                        'end_time': slot_times[slot][1]
                    }
        
        return None
    
    def _find_alternative_room(self, entry: Timetable) -> Optional[Room]:
        """Find an alternative room for a timetable entry"""
        
        # Get suitable rooms
        suitable_rooms = Room.objects.filter(
            is_active=True,
            capacity__gte=entry.class_section.total_students
        )
        
        # Filter by room type if it's a lab
        if entry.is_lab:
            suitable_rooms = suitable_rooms.filter(room_type='lab')
        else:
            suitable_rooms = suitable_rooms.filter(room_type__in=['classroom', 'seminar_hall'])
        
        # Check availability
        for room in suitable_rooms:
            if not Timetable.objects.filter(
                room=room,
                day=entry.day,
                slot_number=entry.slot_number,
                week_number=entry.week_number
            ).exclude(timetable_id=entry.timetable_id).exists():
                return room
        
        return None
    
    def _is_slot_available(self, entry: Timetable, day: str, slot: int) -> bool:
        """Check if a time slot is available for class, staff, and room"""
        
        # Check class availability
        if Timetable.objects.filter(
            class_section=entry.class_section,
            day=day,
            slot_number=slot,
            week_number=entry.week_number
        ).exclude(timetable_id=entry.timetable_id).exists():
            return False
        
        # Check staff availability
        if Timetable.objects.filter(
            staff=entry.staff,
            day=day,
            slot_number=slot,
            week_number=entry.week_number
        ).exclude(timetable_id=entry.timetable_id).exists():
            return False
        
        # Check room availability
        if Timetable.objects.filter(
            room=entry.room,
            day=day,
            slot_number=slot,
            week_number=entry.week_number
        ).exclude(timetable_id=entry.timetable_id).exists():
            return False
        
        return True
    
    def get_substitution_statistics(self, start_date: date, end_date: date) -> Dict:
        """Get substitution statistics for a date range"""
        
        substitutions = Substitution.objects.filter(
            date_of_substitution__range=[start_date, end_date]
        )
        
        total_substitutions = substitutions.count()
        approved_substitutions = substitutions.filter(is_approved=True).count()
        
        # Group by staff
        staff_stats = {}
        for sub in substitutions:
            staff_id = sub.substitute_staff.staff_id
            if staff_id not in staff_stats:
                staff_stats[staff_id] = {
                    'name': sub.substitute_staff.name,
                    'total': 0,
                    'approved': 0
                }
            staff_stats[staff_id]['total'] += 1
            if sub.is_approved:
                staff_stats[staff_id]['approved'] += 1
        
        return {
            'total_substitutions': total_substitutions,
            'approved_substitutions': approved_substitutions,
            'approval_rate': approved_substitutions / total_substitutions if total_substitutions > 0 else 0,
            'staff_statistics': staff_stats,
            'date_range': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            }
        }