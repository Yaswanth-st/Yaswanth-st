// Main JavaScript for Smart Timetable System Frontend
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎓 Smart Timetable System - Frontend Loaded');
    
    // Initialize all components
    initSmoothScrolling();
    initAnimations();
    initNavbar();
    initDemoButtons();
    
    // Show loading message
    showWelcomeMessage();
});

// Smooth scrolling for navigation links
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80; // Account for fixed navbar
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Initialize scroll animations
function initAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate
    const animateElements = document.querySelectorAll('.feature-box, .demo-card, .team-member');
    animateElements.forEach(el => {
        observer.observe(el);
    });
}

// Navbar functionality
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    
    // Change navbar background on scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Close mobile menu when clicking on a link
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        });
    });
}

// Demo button functionality
function initDemoButtons() {
    const demoButtons = document.querySelectorAll('.demo-card .btn');
    
    demoButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const buttonText = this.textContent;
            const originalText = buttonText;
            
            // Show loading state
            this.innerHTML = '<span class="loading"></span> Loading...';
            this.disabled = true;
            
            // Simulate loading time
            setTimeout(() => {
                // Check if page exists
                const href = this.getAttribute('href');
                checkPageExists(href).then(exists => {
                    if (exists) {
                        window.location.href = href;
                    } else {
                        // Show coming soon message
                        showComingSoonMessage(originalText);
                        this.innerHTML = originalText;
                        this.disabled = false;
                    }
                });
            }, 1000);
        });
    });
}

// Check if a page exists
async function checkPageExists(url) {
    try {
        const response = await fetch(url, { method: 'HEAD' });
        return response.ok;
    } catch (error) {
        return false;
    }
}

// Show coming soon message
function showComingSoonMessage(feature) {
    const message = `
        <div class="alert alert-info alert-dismissible fade show position-fixed" 
             style="top: 100px; right: 20px; z-index: 1050; max-width: 350px;">
            <i class="fas fa-info-circle me-2"></i>
            <strong>${feature}</strong> is coming soon! 
            <br><small>The backend is ready - frontend pages are being prepared.</small>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', message);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        const alert = document.querySelector('.alert');
        if (alert) {
            alert.remove();
        }
    }, 5000);
}

// Show welcome message
function showWelcomeMessage() {
    setTimeout(() => {
        const message = `
            <div class="alert alert-success alert-dismissible fade show position-fixed" 
                 style="top: 100px; right: 20px; z-index: 1050; max-width: 350px;">
                <i class="fas fa-rocket me-2"></i>
                <strong>Welcome to Smart Timetable System!</strong>
                <br><small>Developed by TEAM SPIDERMERN</small>
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', message);
        
        // Auto-remove after 4 seconds
        setTimeout(() => {
            const alert = document.querySelector('.alert-success');
            if (alert) {
                alert.remove();
            }
        }, 4000);
    }, 1000);
}

// API Configuration (for future backend integration)
const API_CONFIG = {
    // For development
    development: 'http://localhost:8000',
    // For production (replace with your actual backend URL)
    production: 'https://your-backend-api.herokuapp.com',
    
    // Current environment
    current: 'development'
};

// API Helper functions
const API = {
    baseURL: API_CONFIG[API_CONFIG.current],
    
    async get(endpoint) {
        try {
            const response = await fetch(`${this.baseURL}/api${endpoint}`);
            return await response.json();
        } catch (error) {
            console.error('API GET Error:', error);
            return { error: 'Failed to fetch data' };
        }
    },
    
    async post(endpoint, data) {
        try {
            const response = await fetch(`${this.baseURL}/api${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('API POST Error:', error);
            return { error: 'Failed to send data' };
        }
    }
};

// Feature showcase animations
function startFeatureShowcase() {
    const featureCards = document.querySelectorAll('.feature-card');
    let currentIndex = 0;
    
    setInterval(() => {
        // Remove highlight from all cards
        featureCards.forEach(card => card.classList.remove('highlighted'));
        
        // Highlight current card
        if (featureCards[currentIndex]) {
            featureCards[currentIndex].classList.add('highlighted');
        }
        
        currentIndex = (currentIndex + 1) % featureCards.length;
    }, 3000);
}

// Initialize feature showcase after page load
window.addEventListener('load', () => {
    setTimeout(startFeatureShowcase, 2000);
});

// Utility functions
const Utils = {
    // Format date for display
    formatDate(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date(date));
    },
    
    // Show notification
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 100px; right: 20px; z-index: 1050; max-width: 350px;';
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'times' : 'info'}-circle me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    },
    
    // Loading state
    setLoading(element, loading = true) {
        if (loading) {
            element.disabled = true;
            element.innerHTML = '<span class="loading"></span> Loading...';
        } else {
            element.disabled = false;
        }
    }
};

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    Utils.showNotification('An unexpected error occurred. Please refresh the page.', 'error');
});

// Add CSS for highlighted feature cards
const style = document.createElement('style');
style.textContent = `
    .feature-card.highlighted {
        transform: translateX(15px) scale(1.05);
        background: rgba(255, 255, 255, 0.2);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }
    
    .navbar.scrolled {
        background-color: rgba(13, 110, 253, 0.95) !important;
        backdrop-filter: blur(10px);
    }
    
    .animate-in {
        animation: slideInUp 0.6s ease-out;
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

console.log('✅ Smart Timetable System Frontend - All modules loaded successfully!');