"""
Genetic Algorithm for Smart Timetable Generation
Developed by TEAM SPIDERMERN (SANJAY B, YASWANTH ST, ABISHECK AM)
"""

import random
import numpy as np
from datetime import datetime, time, timedelta
from typing import List, Dict, Tuple, Optional
import copy
import logging

logger = logging.getLogger(__name__)

class TimetableGene:
    """Represents a single timetable slot (gene)"""
    def __init__(self, class_section_id: str, day: str, slot: int, 
                 subject_code: str, staff_id: str, room_id: str, 
                 is_lab: bool = False, is_elective: bool = False):
        self.class_section_id = class_section_id
        self.day = day
        self.slot = slot
        self.subject_code = subject_code
        self.staff_id = staff_id
        self.room_id = room_id
        self.is_lab = is_lab
        self.is_elective = is_elective
    
    def __repr__(self):
        return f"Gene({self.class_section_id}, {self.day}, {self.slot}, {self.subject_code})"

class TimetableChromosome:
    """Represents a complete timetable solution (chromosome)"""
    def __init__(self, genes: List[TimetableGene] = None):
        self.genes = genes or []
        self.fitness_score = 0.0
        self.conflicts = []
        self.penalties = {}
    
    def add_gene(self, gene: TimetableGene):
        self.genes.append(gene)
    
    def get_genes_for_class(self, class_section_id: str) -> List[TimetableGene]:
        return [gene for gene in self.genes if gene.class_section_id == class_section_id]
    
    def get_genes_for_staff(self, staff_id: str) -> List[TimetableGene]:
        return [gene for gene in self.genes if gene.staff_id == staff_id]
    
    def get_genes_for_room(self, room_id: str) -> List[TimetableGene]:
        return [gene for gene in self.genes if gene.room_id == room_id]
    
    def __len__(self):
        return len(self.genes)

class GeneticAlgorithmScheduler:
    """Genetic Algorithm implementation for timetable generation"""
    
    def __init__(self, 
                 population_size: int = 100,
                 generations: int = 500,
                 mutation_rate: float = 0.15,
                 crossover_rate: float = 0.8,
                 elite_ratio: float = 0.1,
                 tournament_size: int = 5):
        
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_ratio = elite_ratio
        self.tournament_size = tournament_size
        
        # Data containers
        self.staff_data = {}
        self.subject_data = {}
        self.class_data = {}
        self.room_data = {}
        self.elective_data = {}
        
        # Constraints
        self.days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        self.time_slots = list(range(1, 9))  # 8 slots per day
        self.slot_times = {
            1: (time(9, 0), time(10, 0)),
            2: (time(10, 0), time(11, 0)),
            3: (time(11, 15), time(12, 15)),
            4: (time(12, 15), time(13, 15)),
            5: (time(14, 0), time(15, 0)),
            6: (time(15, 0), time(16, 0)),
            7: (time(16, 15), time(17, 15)),
            8: (time(17, 15), time(18, 15)),
        }
        
        # Generation statistics
        self.generation_stats = []
        self.best_fitness_history = []
    
    def load_data(self):
        """Load all necessary data from database"""
        try:
            from .models import Staff, Subject, ClassSection, Room, Timetable, Elective
            
            # Load staff data
            for staff in Staff.objects.all():
                self.staff_data[staff.staff_id] = {
                    'name': staff.name,
                    'department': staff.department,
                    'designation': staff.designation,
                    'subjects': staff.subjects_handled,
                    'labs': staff.labs_handled,
                    'electives': staff.electives_handled,
                    'max_sessions_per_day': staff.max_sessions_per_day,
                    'max_sessions_per_week': staff.max_sessions_per_week,
                    'leave_dates': staff.leave_dates,
                }
            
            # Load subject data
            for subject in Subject.objects.all():
                self.subject_data[subject.subject_code] = {
                    'name': subject.subject_name,
                    'type': subject.subject_type,
                    'department': subject.department,
                    'credits': subject.credits,
                    'hours_per_week': subject.hours_per_week,
                    'is_lab': subject.is_lab,
                    'lab_duration': subject.lab_duration_hours,
                }
            
            # Load class data
            for class_section in ClassSection.objects.all():
                self.class_data[class_section.class_id] = {
                    'year': class_section.year,
                    'section': class_section.section,
                    'department': class_section.department,
                    'total_students': class_section.total_students,
                    'subjects': class_section.subjects,
                    'labs': class_section.labs,
                    'electives': class_section.electives,
                    'working_days': class_section.working_days_per_week,
                    'slots_per_day': class_section.slots_per_day,
                }
            
            # Load room data
            for room in Room.objects.filter(is_active=True):
                self.room_data[room.room_id] = {
                    'name': room.room_name,
                    'type': room.room_type,
                    'capacity': room.capacity,
                    'department': room.department,
                    'availability': room.availability,
                }
            
            # Load elective data
            for elective in Elective.objects.all():
                self.elective_data[elective.elective_id] = {
                    'name': elective.elective_name,
                    'department': elective.offering_department,
                    'staff': elective.staff_assigned.staff_id,
                    'hours_per_week': elective.hours_per_week,
                    'enrolled_sections': elective.enrolled_sections,
                }
            
            logger.info(f"Data loaded: {len(self.staff_data)} staff, {len(self.subject_data)} subjects, "
                       f"{len(self.class_data)} classes, {len(self.room_data)} rooms")
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def create_initial_population(self) -> List[TimetableChromosome]:
        """Create initial population of random timetables"""
        population = []
        
        for _ in range(self.population_size):
            chromosome = TimetableChromosome()
            
            # Generate genes for each class
            for class_id, class_info in self.class_data.items():
                self._generate_genes_for_class(chromosome, class_id, class_info)
            
            population.append(chromosome)
        
        logger.info(f"Created initial population of {len(population)} chromosomes")
        return population
    
    def _generate_genes_for_class(self, chromosome: TimetableChromosome, 
                                 class_id: str, class_info: Dict):
        """Generate genes for a specific class"""
        working_days = self.days[:class_info['working_days']]
        slots_per_day = class_info['slots_per_day']
        
        # Track allocated slots to avoid conflicts
        allocated_slots = set()
        
        # Schedule core subjects
        for subject_info in class_info['subjects']:
            subject_code = subject_info['subject_code']
            hours_needed = subject_info['hours_per_week']
            
            for _ in range(hours_needed):
                # Find available slot
                available_slots = []
                for day in working_days:
                    for slot in range(1, slots_per_day + 1):
                        slot_key = (day, slot)
                        if slot_key not in allocated_slots:
                            available_slots.append(slot_key)
                
                if available_slots:
                    day, slot = random.choice(available_slots)
                    allocated_slots.add((day, slot))
                    
                    # Find suitable staff and room
                    staff_id = self._find_suitable_staff(subject_code, day, slot)
                    room_id = self._find_suitable_room(subject_code, day, slot, class_info)
                    
                    if staff_id and room_id:
                        gene = TimetableGene(
                            class_section_id=class_id,
                            day=day,
                            slot=slot,
                            subject_code=subject_code,
                            staff_id=staff_id,
                            room_id=room_id,
                            is_lab=self.subject_data[subject_code]['is_lab']
                        )
                        chromosome.add_gene(gene)
        
        # Schedule labs
        for lab_info in class_info['labs']:
            lab_code = lab_info['lab_code']
            sessions_per_week = lab_info['sessions_per_week']
            
            for _ in range(sessions_per_week):
                # Labs need consecutive slots
                consecutive_slots = self._find_consecutive_slots(
                    allocated_slots, working_days, slots_per_day, 2
                )
                
                if consecutive_slots:
                    day, start_slot = consecutive_slots
                    for i in range(2):  # 2-hour lab session
                        allocated_slots.add((day, start_slot + i))
                    
                    staff_id = self._find_suitable_staff(lab_code, day, start_slot, is_lab=True)
                    room_id = self._find_suitable_lab_room(lab_code, day, start_slot)
                    
                    if staff_id and room_id:
                        for i in range(2):
                            gene = TimetableGene(
                                class_section_id=class_id,
                                day=day,
                                slot=start_slot + i,
                                subject_code=lab_code,
                                staff_id=staff_id,
                                room_id=room_id,
                                is_lab=True
                            )
                            chromosome.add_gene(gene)
        
        # Schedule electives
        for elective_id in class_info['electives']:
            if elective_id in self.elective_data:
                elective_info = self.elective_data[elective_id]
                hours_needed = elective_info['hours_per_week']
                
                for _ in range(hours_needed):
                    available_slots = []
                    for day in working_days:
                        for slot in range(1, slots_per_day + 1):
                            slot_key = (day, slot)
                            if slot_key not in allocated_slots:
                                available_slots.append(slot_key)
                    
                    if available_slots:
                        day, slot = random.choice(available_slots)
                        allocated_slots.add((day, slot))
                        
                        staff_id = elective_info['staff']
                        room_id = self._find_suitable_room(elective_id, day, slot, class_info)
                        
                        if room_id:
                            gene = TimetableGene(
                                class_section_id=class_id,
                                day=day,
                                slot=slot,
                                subject_code=elective_id,
                                staff_id=staff_id,
                                room_id=room_id,
                                is_elective=True
                            )
                            chromosome.add_gene(gene)
    
    def _find_consecutive_slots(self, allocated_slots: set, working_days: List[str], 
                               slots_per_day: int, duration: int) -> Optional[Tuple[str, int]]:
        """Find consecutive available slots for labs"""
        for day in working_days:
            for start_slot in range(1, slots_per_day - duration + 2):
                consecutive_available = True
                for i in range(duration):
                    if (day, start_slot + i) in allocated_slots:
                        consecutive_available = False
                        break
                
                if consecutive_available:
                    return (day, start_slot)
        
        return None
    
    def _find_suitable_staff(self, subject_code: str, day: str, slot: int, 
                           is_lab: bool = False) -> Optional[str]:
        """Find suitable staff for a subject"""
        suitable_staff = []
        
        for staff_id, staff_info in self.staff_data.items():
            # Check if staff can handle this subject/lab
            can_handle = False
            if is_lab and subject_code in staff_info['labs']:
                can_handle = True
            elif not is_lab and subject_code in staff_info['subjects']:
                can_handle = True
            elif subject_code in staff_info['electives']:
                can_handle = True
            
            if can_handle:
                suitable_staff.append(staff_id)
        
        return random.choice(suitable_staff) if suitable_staff else None
    
    def _find_suitable_room(self, subject_code: str, day: str, slot: int, 
                          class_info: Dict) -> Optional[str]:
        """Find suitable room for a subject"""
        suitable_rooms = []
        
        for room_id, room_info in self.room_data.items():
            # Check capacity
            if room_info['capacity'] >= class_info['total_students']:
                # Check if room type matches subject requirement
                if subject_code in self.subject_data:
                    subject_info = self.subject_data[subject_code]
                    if subject_info['is_lab'] and room_info['type'] != 'lab':
                        continue
                    if not subject_info['is_lab'] and room_info['type'] not in ['classroom', 'seminar_hall']:
                        continue
                
                suitable_rooms.append(room_id)
        
        return random.choice(suitable_rooms) if suitable_rooms else None
    
    def _find_suitable_lab_room(self, lab_code: str, day: str, slot: int) -> Optional[str]:
        """Find suitable lab room"""
        lab_rooms = [room_id for room_id, room_info in self.room_data.items() 
                    if room_info['type'] == 'lab']
        return random.choice(lab_rooms) if lab_rooms else None
    
    def calculate_fitness(self, chromosome: TimetableChromosome) -> float:
        """Calculate fitness score for a chromosome"""
        fitness = 100.0  # Start with perfect score
        conflicts = []
        penalties = {}
        
        # Check for conflicts
        conflicts.extend(self._check_staff_conflicts(chromosome))
        conflicts.extend(self._check_room_conflicts(chromosome))
        conflicts.extend(self._check_class_conflicts(chromosome))
        conflicts.extend(self._check_lab_constraints(chromosome))
        
        # Apply penalties
        penalties['workload'] = self._check_staff_workload(chromosome)
        penalties['preferences'] = self._check_preferences(chromosome)
        penalties['distribution'] = self._check_subject_distribution(chromosome)
        
        # Calculate final fitness
        conflict_penalty = len(conflicts) * 10
        workload_penalty = penalties['workload'] * 5
        preference_penalty = penalties['preferences'] * 2
        distribution_penalty = penalties['distribution'] * 3
        
        total_penalty = conflict_penalty + workload_penalty + preference_penalty + distribution_penalty
        fitness = max(0, fitness - total_penalty)
        
        chromosome.fitness_score = fitness
        chromosome.conflicts = conflicts
        chromosome.penalties = penalties
        
        return fitness
    
    def _check_staff_conflicts(self, chromosome: TimetableChromosome) -> List[str]:
        """Check for staff scheduling conflicts"""
        conflicts = []
        staff_schedule = {}
        
        for gene in chromosome.genes:
            staff_id = gene.staff_id
            time_slot = (gene.day, gene.slot)
            
            if staff_id not in staff_schedule:
                staff_schedule[staff_id] = set()
            
            if time_slot in staff_schedule[staff_id]:
                conflicts.append(f"Staff {staff_id} double-booked on {gene.day} slot {gene.slot}")
            else:
                staff_schedule[staff_id].add(time_slot)
        
        return conflicts
    
    def _check_room_conflicts(self, chromosome: TimetableChromosome) -> List[str]:
        """Check for room scheduling conflicts"""
        conflicts = []
        room_schedule = {}
        
        for gene in chromosome.genes:
            room_id = gene.room_id
            time_slot = (gene.day, gene.slot)
            
            if room_id not in room_schedule:
                room_schedule[room_id] = set()
            
            if time_slot in room_schedule[room_id]:
                conflicts.append(f"Room {room_id} double-booked on {gene.day} slot {gene.slot}")
            else:
                room_schedule[room_id].add(time_slot)
        
        return conflicts
    
    def _check_class_conflicts(self, chromosome: TimetableChromosome) -> List[str]:
        """Check for class scheduling conflicts"""
        conflicts = []
        class_schedule = {}
        
        for gene in chromosome.genes:
            class_id = gene.class_section_id
            time_slot = (gene.day, gene.slot)
            
            if class_id not in class_schedule:
                class_schedule[class_id] = set()
            
            if time_slot in class_schedule[class_id]:
                conflicts.append(f"Class {class_id} has multiple subjects on {gene.day} slot {gene.slot}")
            else:
                class_schedule[class_id].add(time_slot)
        
        return conflicts
    
    def _check_lab_constraints(self, chromosome: TimetableChromosome) -> List[str]:
        """Check lab-specific constraints"""
        conflicts = []
        
        for gene in chromosome.genes:
            if gene.is_lab:
                # Check if lab is in appropriate room
                room_info = self.room_data.get(gene.room_id, {})
                if room_info.get('type') != 'lab':
                    conflicts.append(f"Lab {gene.subject_code} scheduled in non-lab room {gene.room_id}")
        
        return conflicts
    
    def _check_staff_workload(self, chromosome: TimetableChromosome) -> int:
        """Check staff workload violations"""
        violations = 0
        staff_workload = {}
        
        for gene in chromosome.genes:
            staff_id = gene.staff_id
            day = gene.day
            
            if staff_id not in staff_workload:
                staff_workload[staff_id] = {'total': 0, 'daily': {}}
            
            if day not in staff_workload[staff_id]['daily']:
                staff_workload[staff_id]['daily'][day] = 0
            
            staff_workload[staff_id]['total'] += 1
            staff_workload[staff_id]['daily'][day] += 1
        
        for staff_id, workload in staff_workload.items():
            staff_info = self.staff_data.get(staff_id, {})
            max_daily = staff_info.get('max_sessions_per_day', 8)
            max_weekly = staff_info.get('max_sessions_per_week', 30)
            
            if workload['total'] > max_weekly:
                violations += workload['total'] - max_weekly
            
            for day_load in workload['daily'].values():
                if day_load > max_daily:
                    violations += day_load - max_daily
        
        return violations
    
    def _check_preferences(self, chromosome: TimetableChromosome) -> int:
        """Check preference violations (can be extended)"""
        # Placeholder for preference checking
        return 0
    
    def _check_subject_distribution(self, chromosome: TimetableChromosome) -> int:
        """Check subject distribution quality"""
        violations = 0
        
        # Check for consecutive subject sessions (should be avoided)
        for class_id in self.class_data.keys():
            class_genes = chromosome.get_genes_for_class(class_id)
            
            for day in self.days:
                day_genes = [g for g in class_genes if g.day == day]
                day_genes.sort(key=lambda x: x.slot)
                
                for i in range(len(day_genes) - 1):
                    if (day_genes[i].subject_code == day_genes[i + 1].subject_code and
                        day_genes[i + 1].slot == day_genes[i].slot + 1):
                        violations += 1
        
        return violations
    
    def tournament_selection(self, population: List[TimetableChromosome]) -> TimetableChromosome:
        """Tournament selection for parent selection"""
        tournament = random.sample(population, min(self.tournament_size, len(population)))
        return max(tournament, key=lambda x: x.fitness_score)
    
    def crossover(self, parent1: TimetableChromosome, 
                 parent2: TimetableChromosome) -> Tuple[TimetableChromosome, TimetableChromosome]:
        """Order crossover for chromosomes"""
        if random.random() > self.crossover_rate:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)
        
        # Simple crossover: exchange genes for random classes
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)
        
        # Select random classes to exchange
        all_classes = list(self.class_data.keys())
        exchange_classes = random.sample(all_classes, len(all_classes) // 2)
        
        # Exchange genes for selected classes
        child1_genes = [g for g in parent1.genes if g.class_section_id not in exchange_classes]
        child1_genes.extend([g for g in parent2.genes if g.class_section_id in exchange_classes])
        
        child2_genes = [g for g in parent2.genes if g.class_section_id not in exchange_classes]
        child2_genes.extend([g for g in parent1.genes if g.class_section_id in exchange_classes])
        
        child1.genes = child1_genes
        child2.genes = child2_genes
        
        return child1, child2
    
    def mutate(self, chromosome: TimetableChromosome) -> TimetableChromosome:
        """Mutation operator"""
        if random.random() > self.mutation_rate:
            return chromosome
        
        mutated = copy.deepcopy(chromosome)
        
        if mutated.genes:
            # Random mutation strategies
            mutation_type = random.choice(['change_staff', 'change_room', 'change_time'])
            gene_index = random.randint(0, len(mutated.genes) - 1)
            gene = mutated.genes[gene_index]
            
            if mutation_type == 'change_staff':
                new_staff = self._find_suitable_staff(gene.subject_code, gene.day, gene.slot, gene.is_lab)
                if new_staff:
                    gene.staff_id = new_staff
            
            elif mutation_type == 'change_room':
                class_info = self.class_data[gene.class_section_id]
                new_room = self._find_suitable_room(gene.subject_code, gene.day, gene.slot, class_info)
                if new_room:
                    gene.room_id = new_room
            
            elif mutation_type == 'change_time':
                # Try to find a new time slot
                class_info = self.class_data[gene.class_section_id]
                working_days = self.days[:class_info['working_days']]
                new_day = random.choice(working_days)
                new_slot = random.randint(1, class_info['slots_per_day'])
                
                gene.day = new_day
                gene.slot = new_slot
        
        return mutated
    
    def evolve_population(self, population: List[TimetableChromosome]) -> List[TimetableChromosome]:
        """Evolve population for one generation"""
        # Calculate fitness for all chromosomes
        for chromosome in population:
            self.calculate_fitness(chromosome)
        
        # Sort by fitness (descending)
        population.sort(key=lambda x: x.fitness_score, reverse=True)
        
        # Elite selection
        elite_count = int(self.population_size * self.elite_ratio)
        next_population = population[:elite_count]
        
        # Generate offspring
        while len(next_population) < self.population_size:
            parent1 = self.tournament_selection(population)
            parent2 = self.tournament_selection(population)
            
            child1, child2 = self.crossover(parent1, parent2)
            child1 = self.mutate(child1)
            child2 = self.mutate(child2)
            
            next_population.extend([child1, child2])
        
        # Trim to exact population size
        return next_population[:self.population_size]
    
    def generate_timetable(self) -> Tuple[TimetableChromosome, Dict]:
        """Main method to generate timetable using GA"""
        logger.info("Starting timetable generation using Genetic Algorithm")
        
        try:
            # Load data
            self.load_data()
            
            # Create initial population
            population = self.create_initial_population()
            
            # Evolution loop
            best_chromosome = None
            best_fitness = -1
            
            for generation in range(self.generations):
                # Evolve population
                population = self.evolve_population(population)
                
                # Track best chromosome
                current_best = max(population, key=lambda x: x.fitness_score)
                if current_best.fitness_score > best_fitness:
                    best_fitness = current_best.fitness_score
                    best_chromosome = copy.deepcopy(current_best)
                
                # Log progress
                avg_fitness = sum(c.fitness_score for c in population) / len(population)
                self.generation_stats.append({
                    'generation': generation,
                    'best_fitness': best_fitness,
                    'average_fitness': avg_fitness,
                    'conflicts': len(best_chromosome.conflicts) if best_chromosome else 0
                })
                
                self.best_fitness_history.append(best_fitness)
                
                if generation % 50 == 0:
                    logger.info(f"Generation {generation}: Best={best_fitness:.2f}, "
                              f"Avg={avg_fitness:.2f}, Conflicts={len(best_chromosome.conflicts)}")
                
                # Early termination if perfect solution found
                if best_fitness >= 95.0 and len(best_chromosome.conflicts) == 0:
                    logger.info(f"Perfect solution found at generation {generation}")
                    break
            
            # Prepare result
            result_stats = {
                'best_fitness': best_fitness,
                'total_generations': len(self.generation_stats),
                'conflicts_count': len(best_chromosome.conflicts),
                'conflicts': best_chromosome.conflicts,
                'penalties': best_chromosome.penalties,
                'generation_stats': self.generation_stats,
                'fitness_history': self.best_fitness_history
            }
            
            logger.info(f"Timetable generation completed. Best fitness: {best_fitness:.2f}")
            return best_chromosome, result_stats
            
        except Exception as e:
            logger.error(f"Error in timetable generation: {e}")
            raise