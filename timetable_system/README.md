# 🎓 Smart Timetable Generation System

**Developed by TEAM SPIDERMERN**
- **SANJAY B**
- **YASWANTH ST** 
- **ABISHECK AM**

## 🚀 Overview

An intelligent timetable management system powered by advanced **Genetic Algorithm** for educational institutions. The system automatically generates optimal schedules while considering staff availability, room constraints, lab requirements, and elective subjects across departments.

## 📋 Features

### 🧠 AI-Powered Generation
- **Genetic Algorithm Optimization** - Uses evolutionary computing for optimal solutions
- **Conflict-free Scheduling** - Automatically resolves time, staff, and room conflicts
- **Load Balancing** - Distributes workload evenly across staff
- **Resource Optimization** - Maximizes utilization of rooms and time slots

### 🔄 Smart Substitution Engine
- **Automatic Substitute Finding** - Intelligent replacement when staff is unavailable
- **Department-wise Prioritization** - Prefers staff from same department
- **Workload Consideration** - Balances substitute assignments
- **Approval Workflow** - Structured approval process for substitutions

### 📊 Comprehensive Management
- **Staff Management** - Complete staff profiles with subjects and constraints
- **Subject Management** - Core subjects, labs, and electives handling
- **Class Management** - Multi-department class sections with customizable schedules
- **Room Management** - Classrooms and labs with capacity and availability tracking

### 📈 Analytics & Reports
- **Real-time Statistics** - Resource utilization and workload analytics
- **Conflict Resolution Reports** - Detailed analysis of scheduling conflicts
- **Export Capabilities** - Multiple export formats for timetables
- **Performance Metrics** - Genetic algorithm fitness scores and optimization data

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Django (Python) |
| **Database** | MongoDB (localhost:27017) |
| **Frontend** | HTML5, CSS3, JavaScript (Bootstrap 5) |
| **Algorithm** | Genetic Algorithm with NumPy |
| **UI Framework** | Bootstrap 5 with Font Awesome |
| **Charts** | Chart.js for analytics |

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- MongoDB (running on localhost:27017)
- pip (Python package manager)

### 1. Clone & Setup
```bash
# Clone the repository
git clone <repository-url>
cd timetable_system

# Install dependencies
pip install django pymongo requests python-decouple numpy

# Setup Django
python manage.py migrate
python manage.py collectstatic
```

### 2. Create Superuser
```bash
python manage.py createsuperuser
```

### 3. Run the Server
```bash
python manage.py runserver 0.0.0.0:8000
```

### 4. Access the Application
- **Main Application**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/

## 📊 Database Configuration

The system uses **MongoDB** as the primary database:
- **Database Name**: `TIMETABLE`
- **Host**: `localhost:27017`
- **Collections**: staff, subjects, classes, rooms, timetables, electives, substitutions

### MongoDB Collections Structure

#### Staff Collection
```json
{
  "staff_id": "CSE001",
  "name": "Dr. John Doe",
  "designation": "professor",
  "department": "cse",
  "subjects_handled": ["CS101", "CS201"],
  "labs_handled": ["CS101L"],
  "max_sessions_per_week": 20,
  "leave_dates": ["2024-12-25"]
}
```

#### Subjects Collection
```json
{
  "subject_code": "CS101",
  "subject_name": "Programming Fundamentals",
  "department": "cse",
  "hours_per_week": 4,
  "is_lab": false,
  "semester": 1
}
```

## 🎯 Key Algorithms

### Genetic Algorithm Parameters
- **Population Size**: 100-500 chromosomes
- **Generations**: 100-1000 evolution cycles
- **Mutation Rate**: 0.01-0.5 (default: 0.15)
- **Crossover Rate**: 0.5-1.0 (default: 0.8)
- **Elite Ratio**: 0.1 (top 10% preserved)

### Fitness Function
The fitness score considers:
1. **Conflict Minimization** (40% weight)
2. **Workload Balance** (30% weight)
3. **Resource Utilization** (20% weight)
4. **Preference Satisfaction** (10% weight)

### Constraint Handling
- ✅ No staff double-booking
- ✅ No room conflicts
- ✅ No class overlaps
- ✅ Lab consecutive slot requirements
- ✅ Staff workload limits
- ✅ Room capacity constraints

## 📱 User Interface

### Dashboard Features
- **Real-time Statistics** - Live data on system status
- **Quick Actions** - One-click access to common tasks
- **Analytics Modal** - Detailed system performance metrics
- **Responsive Design** - Mobile-friendly interface

### Timetable Generation
- **Interactive Form** - User-friendly parameter selection
- **Real-time Progress** - Live generation status updates
- **Advanced Options** - Fine-tune algorithm parameters
- **Results Visualization** - Comprehensive generation reports

### View Options
- **Class-wise Timetables** - Individual class schedules
- **Staff-wise Timetables** - Personal staff schedules
- **Room-wise Timetables** - Room utilization schedules
- **Department Filtering** - Focused departmental views

## 🔄 API Endpoints

### Core APIs
- `POST /api/conflict-resolution/` - Automatic conflict resolution
- `POST /api/timetable-export/` - Export timetables in various formats
- `GET /api/statistics/` - System analytics and statistics
- `POST /substitutions/approve/<id>/` - Approve substitution requests

### Data Management
- Staff CRUD operations
- Subject management
- Class section handling
- Room administration
- Timetable generation and viewing

## 🧪 Testing & Validation

### Model Validation
- Input validation for all form fields
- Database constraints enforcement
- Cross-field validation rules

### Algorithm Testing
- Fitness function optimization
- Constraint satisfaction verification
- Performance benchmarking

## 🔒 Security Features

- **CSRF Protection** - All forms protected against CSRF attacks
- **Input Validation** - Comprehensive server-side validation
- **SQL Injection Prevention** - ORM-based database operations
- **Authentication** - Django's built-in authentication system

## 📈 Performance Optimization

### Genetic Algorithm
- **Parallel Processing** - Multi-threaded population evaluation
- **Early Termination** - Stop when optimal solution found
- **Adaptive Parameters** - Dynamic mutation and crossover rates
- **Memory Optimization** - Efficient chromosome representation

### Database
- **Indexing** - Optimized database queries
- **Connection Pooling** - Efficient MongoDB connections
- **Caching** - Strategic data caching for performance

## 🎨 UI/UX Design

### Modern Interface
- **Bootstrap 5** - Latest responsive framework
- **Font Awesome** - Professional iconography
- **Google Fonts** - Clean typography (Inter font)
- **Color Scheme** - Professional blue gradient theme

### User Experience
- **Intuitive Navigation** - Clear menu structure
- **Progress Indicators** - Visual feedback for long operations
- **Toast Notifications** - Non-intrusive user feedback
- **Mobile Responsive** - Works on all device sizes

## 🚀 Future Enhancements

### Planned Features
- **Google Calendar Integration** - Sync with external calendars
- **WhatsApp Notifications** - Automated schedule reminders
- **PDF Export** - Professional printable timetables
- **Advanced Analytics** - Machine learning insights
- **Multi-language Support** - Internationalization

### Algorithm Improvements
- **Hybrid Algorithms** - Combine GA with other optimization techniques
- **Preference Learning** - Adaptive preference weights
- **Constraint Relaxation** - Flexible constraint handling
- **Real-time Updates** - Dynamic schedule adjustments

## 📞 Support & Contact

**Development Team: TEAM SPIDERMERN**

For technical support or feature requests, please contact the development team.

## 📄 License

This project is developed as part of an educational initiative by TEAM SPIDERMERN.

---

**© 2024 TEAM SPIDERMERN - Smart Timetable Generation System**

*Intelligent Scheduling • Conflict Resolution • Resource Optimization*