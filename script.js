// DOM Elements
const navbar = document.getElementById('navbar');
const promoBanner = document.getElementById('promo-banner');
const promoClose = document.getElementById('promo-close');
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');
const bookSessionModal = document.getElementById('book-session-modal');
const modalClose = document.getElementById('modal-close');
const sessionsGrid = document.getElementById('sessions-grid');

// Authentication Elements
const loginModal = document.getElementById('login-modal');
const signupModal = document.getElementById('signup-modal');
const loginBtn = document.getElementById('login-btn');
const signupBtn = document.getElementById('signup-btn');
const ctaLogin = document.getElementById('cta-login');
const ctaSignup = document.getElementById('cta-signup');
const loginModalClose = document.getElementById('login-modal-close');
const signupModalClose = document.getElementById('signup-modal-close');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const switchToSignup = document.querySelector('.switch-to-signup');
const switchToLogin = document.querySelector('.switch-to-login');

// Sample session data
const featuredSessions = [
    {
        id: 1,
        title: "Python for Beginners",
        teacher: "Alex Chen",
        avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=40&h=40&fit=crop&crop=face",
        image: "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=300&h=200&fit=crop",
        description: "Learn Python fundamentals with hands-on coding exercises",
        price: "$25",
        duration: "45 min",
        rating: "4.9",
        reviews: 127,
        type: "online"
    },
    {
        id: 2,
        title: "Guitar Basics",
        teacher: "Sarah Johnson",
        avatar: "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=40&h=40&fit=crop&crop=face",
        image: "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=300&h=200&fit=crop",
        description: "Master basic chords and strumming patterns",
        price: "Skill Trade",
        duration: "30 min",
        rating: "5.0",
        reviews: 89,
        type: "offline"
    },
    {
        id: 3,
        title: "Digital Photography",
        teacher: "Mike Rodriguez",
        avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=40&h=40&fit=crop&crop=face",
        image: "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=300&h=200&fit=crop",
        description: "Composition, lighting, and editing techniques",
        price: "$30",
        duration: "60 min",
        rating: "4.8",
        reviews: 156,
        type: "online"
    },
    {
        id: 4,
        title: "Spanish Conversation",
        teacher: "Elena Martinez",
        avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=40&h=40&fit=crop&crop=face",
        image: "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=300&h=200&fit=crop",
        description: "Practice conversational Spanish with native speaker",
        price: "$15 + Recipe",
        duration: "30 min",
        rating: "4.9",
        reviews: 203,
        type: "hybrid"
    },
    {
        id: 5,
        title: "Cooking Basics",
        teacher: "James Wilson",
        avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=40&h=40&fit=crop&crop=face",
        image: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=200&fit=crop",
        description: "Essential cooking techniques and knife skills",
        price: "Skill Trade",
        duration: "45 min",
        rating: "4.7",
        reviews: 92,
        type: "offline"
    },
    {
        id: 6,
        title: "Excel Masterclass",
        teacher: "Lisa Park",
        avatar: "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=40&h=40&fit=crop&crop=face",
        image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=300&h=200&fit=crop",
        description: "Advanced Excel formulas and data analysis",
        price: "$35",
        duration: "60 min",
        rating: "4.9",
        reviews: 178,
        type: "online"
    }
];

// Promotional banner close
function closeBanner() {
    if (promoBanner) {
        promoBanner.style.display = 'none';
        // Store in localStorage to remember user preference
        localStorage.setItem('promoBannerClosed', 'true');
        // Adjust navbar position
        navbar.style.top = '0';
        // Adjust hero padding
        const hero = document.querySelector('.hero');
        if (hero) {
            hero.style.paddingTop = '8rem';
        }
    }
}

// Check if banner should be shown
function checkBannerVisibility() {
    const bannerClosed = localStorage.getItem('promoBannerClosed');
    if (bannerClosed === 'true' && promoBanner) {
        promoBanner.style.display = 'none';
        navbar.style.top = '0';
        const hero = document.querySelector('.hero');
        if (hero) {
            hero.style.paddingTop = '8rem';
        }
    }
}

// Navbar scroll effect
function handleNavbarScroll() {
    if (window.scrollY > 100) {
        navbar.style.backdropFilter = 'blur(15px)';
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.15)';
    } else {
        navbar.style.backdropFilter = 'blur(10px)';
        navbar.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.05)';
    }
}

// Mobile menu toggle
function toggleMobileMenu() {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
    
    // Prevent body scroll when menu is open
    document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
}

// Close mobile menu when clicking on a nav link
function closeMobileMenu() {
    hamburger.classList.remove('active');
    navMenu.classList.remove('active');
    document.body.style.overflow = '';
}

// Smooth scroll for navigation links
function smoothScroll(targetId) {
    const targetElement = document.querySelector(targetId);
    if (targetElement) {
        const offsetTop = targetElement.offsetTop - 80; // Account for fixed navbar
        window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
        });
    }
}

// Hero slider functionality
function initHeroSlider() {
    const slides = document.querySelectorAll('.hero-slide');
    let currentSlide = 0;
    
    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === index);
        });
    }
    
    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }
    
    // Auto-advance slides every 5 seconds
    if (slides.length > 1) {
        setInterval(nextSlide, 5000);
    }
}

// Modal functionality
function openModal() {
    bookSessionModal.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // Focus on first input for accessibility
    const firstInput = bookSessionModal.querySelector('input, select');
    if (firstInput) {
        setTimeout(() => firstInput.focus(), 100);
    }
}

function closeModal() {
    bookSessionModal.classList.remove('active');
    document.body.style.overflow = '';
}

// Create session card HTML
function createSessionCard(session) {
    const typeIcon = session.type === 'online' ? '💻' : session.type === 'offline' ? '📍' : '⚡';
    const priceClass = session.price.includes('$') ? 'session-price' : 
                      session.price.includes('Trade') ? 'barter' : 'hybrid';
    
    return `
        <div class="session-card" data-session-id="${session.id}">
            <img src="${session.image}" alt="${session.title}" class="session-image" loading="lazy">
            <div class="session-content">
                <div class="session-meta">
                    <img src="${session.avatar}" alt="${session.teacher}" class="session-avatar">
                    <div class="session-info">
                        <h4>${session.teacher}</h4>
                        <div class="rating">
                            <span class="stars">★★★★★</span>
                            <span class="rating-text">${session.rating} (${session.reviews})</span>
                        </div>
                    </div>
                    <span class="session-type">${typeIcon}</span>
                </div>
                <h3 class="session-title">${session.title}</h3>
                <p class="session-description">${session.description}</p>
                <div class="session-footer">
                    <span class="${priceClass}">${session.price}</span>
                    <span class="session-duration">${session.duration}</span>
                </div>
            </div>
        </div>
    `;
}

// Render featured sessions
function renderFeaturedSessions() {
    if (!sessionsGrid) return;
    
    // Show loading state
    sessionsGrid.innerHTML = '<div class="loading">Loading sessions...</div>';
    
    // Simulate loading delay for better UX
    setTimeout(() => {
        sessionsGrid.innerHTML = featuredSessions
            .slice(0, 6) // Show first 6 sessions
            .map(session => createSessionCard(session))
            .join('');
        
        // Add click handlers to session cards
        sessionsGrid.querySelectorAll('.session-card').forEach(card => {
            card.addEventListener('click', () => {
                const sessionId = card.dataset.sessionId;
                handleSessionClick(sessionId);
            });
        });
    }, 500);
}

// Handle session card clicks
function handleSessionClick(sessionId) {
    const session = featuredSessions.find(s => s.id == sessionId);
    if (!session) return;
    
    // Pre-fill modal with session data
    const skillSearch = document.getElementById('skill-search');
    const sessionType = document.getElementById('session-type');
    
    if (skillSearch) skillSearch.value = session.title;
    if (sessionType) sessionType.value = session.type;
    
    openModal();
}

// Form submission handler
function handleBookingSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const bookingData = Object.fromEntries(formData.entries());
    
    // Simulate booking process
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    submitBtn.textContent = 'Searching...';
    submitBtn.disabled = true;
    
    setTimeout(() => {
        alert('Great! We found 12 matching sessions. Redirecting to search results...');
        closeModal();
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        
        // Reset form
        event.target.reset();
    }, 2000);
}

// Authentication Functions
function openLoginModal() {
    if (loginModal) {
        loginModal.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Focus on first input for accessibility
        const firstInput = loginModal.querySelector('input');
        if (firstInput) {
            setTimeout(() => firstInput.focus(), 100);
        }
    }
}

function openSignupModal() {
    if (signupModal) {
        signupModal.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Focus on first input for accessibility
        const firstInput = signupModal.querySelector('input');
        if (firstInput) {
            setTimeout(() => firstInput.focus(), 100);
        }
    }
}

function closeLoginModal() {
    if (loginModal) {
        loginModal.classList.remove('active');
        document.body.style.overflow = '';
        loginForm?.reset();
    }
}

function closeSignupModal() {
    if (signupModal) {
        signupModal.classList.remove('active');
        document.body.style.overflow = '';
        signupForm?.reset();
    }
}

function switchToSignupModal() {
    closeLoginModal();
    setTimeout(openSignupModal, 100);
}

function switchToLoginModal() {
    closeSignupModal();
    setTimeout(openLoginModal, 100);
}

// Handle login form submission
function handleLoginSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const loginData = Object.fromEntries(formData.entries());
    
    // Validate form
    if (!loginData.email || !loginData.password) {
        alert('Please fill in all required fields.');
        return;
    }
    
    // Simulate login process
    const submitBtn = event.target.querySelector('.auth-submit');
    const originalText = submitBtn.textContent;
    
    submitBtn.textContent = 'Logging in...';
    submitBtn.disabled = true;
    
    setTimeout(() => {
        // Simulate successful login
        alert(`Welcome back! You're now logged in as ${loginData.email}`);
        closeLoginModal();
        
        // Update UI to show logged in state
        updateAuthUI(loginData.email);
        
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }, 1500);
}

// Handle signup form submission
function handleSignupSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const signupData = Object.fromEntries(formData.entries());
    
    // Validate form
    if (!signupData.firstName || !signupData.lastName || !signupData.email || !signupData.password || !signupData.confirmPassword || !signupData.userType) {
        alert('Please fill in all required fields.');
        return;
    }
    
    if (signupData.password !== signupData.confirmPassword) {
        alert('Passwords do not match.');
        return;
    }
    
    if (signupData.password.length < 8) {
        alert('Password must be at least 8 characters long.');
        return;
    }
    
    if (!signupData.agreeTerms) {
        alert('Please agree to the Terms of Service and Privacy Policy.');
        return;
    }
    
    // Simulate signup process
    const submitBtn = event.target.querySelector('.auth-submit');
    const originalText = submitBtn.textContent;
    
    submitBtn.textContent = 'Creating account...';
    submitBtn.disabled = true;
    
    setTimeout(() => {
        // Simulate successful signup
        alert(`Welcome to BorrowMyBrain, ${signupData.firstName}! Your account has been created successfully.`);
        closeSignupModal();
        
        // Update UI to show logged in state
        updateAuthUI(signupData.email, `${signupData.firstName} ${signupData.lastName}`);
        
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }, 2000);
}

// Update UI after successful authentication
function updateAuthUI(email, fullName = '') {
    // Update navigation buttons
    const loginBtn = document.getElementById('login-btn');
    const signupBtn = document.getElementById('signup-btn');
    
    if (loginBtn && signupBtn) {
        const userName = fullName || email.split('@')[0];
        loginBtn.textContent = userName;
        loginBtn.classList.remove('btn-outline');
        loginBtn.classList.add('btn-secondary');
        
        signupBtn.textContent = 'Logout';
        signupBtn.onclick = () => {
            if (confirm('Are you sure you want to logout?')) {
                // Reset UI
                loginBtn.textContent = 'Log in';
                loginBtn.classList.add('btn-outline');
                loginBtn.classList.remove('btn-secondary');
                signupBtn.textContent = 'Sign up';
                signupBtn.onclick = null;
                
                alert('You have been logged out successfully.');
            }
        };
    }
}

// Handle social login (LinkedIn/Google)
function handleSocialLogin(provider) {
    alert(`${provider} login will be implemented with OAuth integration. For now, this is a demo.`);
}

// Simple and subtle scroll animations
function setupScrollAnimations() {
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const delay = entry.target.dataset.delay || 0;
                
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, delay);
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements with animate-on-scroll class
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => {
        observer.observe(el);
    });
    
    // Add animate-on-scroll to other elements
    const otherElements = document.querySelectorAll('.skill-card, .career-card, .testimonial-card, .session-card, .step, .feature-item');
    otherElements.forEach(el => {
        if (!el.classList.contains('animate-on-scroll')) {
            el.classList.add('animate-on-scroll');
            observer.observe(el);
        }
    });
}

// Simple hover effects for skill cards
function setupSkillCardHovers() {
    const skillCards = document.querySelectorAll('.skill-card');
    
    skillCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-3px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });
}

// Simple page initialization
function initPageAnimations() {
    // Setup simple hover effects
    setupSkillCardHovers();
    
    // Add gentle fade-in to sections
    const sections = document.querySelectorAll('section');
    sections.forEach((section, index) => {
        section.style.opacity = '0.95';
        section.style.transition = 'opacity 0.3s ease-in-out';
        
        setTimeout(() => {
            section.style.opacity = '1';
        }, index * 100);
    });
}

// No additional animation styles needed - using CSS-based animations

// Initialize tooltips for accessibility
function initializeTooltips() {
    const elementsWithTooltips = document.querySelectorAll('[title]');
    elementsWithTooltips.forEach(el => {
        const title = el.getAttribute('title');
        el.setAttribute('aria-label', title);
    });
}

// Keyboard navigation for modals
function handleModalKeyboard(event) {
    let activeModal = null;
    
    if (bookSessionModal?.classList.contains('active')) {
        activeModal = bookSessionModal;
    } else if (loginModal?.classList.contains('active')) {
        activeModal = loginModal;
    } else if (signupModal?.classList.contains('active')) {
        activeModal = signupModal;
    }
    
    if (!activeModal) return;
    
    if (event.key === 'Escape') {
        if (activeModal === bookSessionModal) closeModal();
        else if (activeModal === loginModal) closeLoginModal();
        else if (activeModal === signupModal) closeSignupModal();
    }
    
    // Trap focus within modal
    if (event.key === 'Tab') {
        const focusableElements = activeModal.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        const firstFocusable = focusableElements[0];
        const lastFocusable = focusableElements[focusableElements.length - 1];
        
        if (event.shiftKey) {
            if (document.activeElement === firstFocusable) {
                lastFocusable.focus();
                event.preventDefault();
            }
        } else {
            if (document.activeElement === lastFocusable) {
                firstFocusable.focus();
                event.preventDefault();
            }
        }
    }
}

// Performance optimization: Debounce scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Error handling for image loading
function handleImageError(event) {
    event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iI2Y4ZjlmYSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiM2YTZmNzMiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5JbWFnZSBub3QgYXZhaWxhYmxlPC90ZXh0Pjwvc3ZnPg==';
}

// Add error handlers to all images
function setupImageErrorHandling() {
    document.addEventListener('error', (event) => {
        if (event.target.tagName === 'IMG') {
            handleImageError(event);
        }
    }, true);
}

// Newsletter subscription
function handleNewsletterSubmit(event) {
    event.preventDefault();
    const email = event.target.querySelector('.newsletter-input').value;
    
    if (!email || !email.includes('@')) {
        alert('Please enter a valid email address.');
        return;
    }
    
    const submitBtn = event.target.querySelector('.newsletter-btn');
    const originalText = submitBtn.textContent;
    
    submitBtn.textContent = 'Subscribing...';
    submitBtn.disabled = true;
    
    setTimeout(() => {
        alert('Thank you for subscribing! You\'ll receive updates about new learning opportunities.');
        event.target.reset();
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }, 1500);
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize all functionality
    checkBannerVisibility();
    renderFeaturedSessions();
    setupScrollAnimations();
    initializeTooltips();
    setupImageErrorHandling();
    
    // Initialize simple animations
    initPageAnimations();
    
    // Initialize hero slider
    initHeroSlider();
    
    // Banner close
    promoClose?.addEventListener('click', closeBanner);
    
    // Scroll events
    window.addEventListener('scroll', debounce(handleNavbarScroll, 10));
    
    // Mobile menu
    hamburger?.addEventListener('click', toggleMobileMenu);
    
    // Navigation links
    document.querySelectorAll('.nav-link[href^="#"]').forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const targetId = link.getAttribute('href');
            smoothScroll(targetId);
            closeMobileMenu();
        });
    });
    
    // Initialize hero slider
    initHeroSlider();
    
    // Modal controls
    document.querySelectorAll('.btn').forEach(btn => {
        if (btn.textContent.includes('Try it') || btn.textContent.includes('Learn AI')) {
            btn.addEventListener('click', openModal);
        }
    });
    modalClose?.addEventListener('click', closeModal);
    
    // Close modal when clicking outside
    bookSessionModal?.addEventListener('click', (event) => {
        if (event.target === bookSessionModal) {
            closeModal();
        }
    });
    
    // Form submission
    const bookingForm = document.querySelector('.booking-form');
    bookingForm?.addEventListener('submit', handleBookingSubmit);
    
    // Newsletter subscription
    const newsletterForm = document.querySelector('.newsletter-form');
    newsletterForm?.addEventListener('submit', handleNewsletterSubmit);
    
    // Authentication event listeners
    loginBtn?.addEventListener('click', openLoginModal);
    signupBtn?.addEventListener('click', openSignupModal);
    ctaLogin?.addEventListener('click', openLoginModal);
    ctaSignup?.addEventListener('click', openSignupModal);
    
    loginModalClose?.addEventListener('click', closeLoginModal);
    signupModalClose?.addEventListener('click', closeSignupModal);
    
    switchToSignup?.addEventListener('click', (e) => {
        e.preventDefault();
        switchToSignupModal();
    });
    
    switchToLogin?.addEventListener('click', (e) => {
        e.preventDefault();
        switchToLoginModal();
    });
    
    loginForm?.addEventListener('submit', handleLoginSubmit);
    signupForm?.addEventListener('submit', handleSignupSubmit);
    
    // Close modals when clicking outside
    loginModal?.addEventListener('click', (event) => {
        if (event.target === loginModal) {
            closeLoginModal();
        }
    });
    
    signupModal?.addEventListener('click', (event) => {
        if (event.target === signupModal) {
            closeSignupModal();
        }
    });
    
    // Social login buttons
    document.querySelectorAll('#linkedin-login, #linkedin-signup').forEach(btn => {
        btn.addEventListener('click', () => handleSocialLogin('LinkedIn'));
    });
    
    document.querySelectorAll('#google-login, #google-signup').forEach(btn => {
        btn.addEventListener('click', () => handleSocialLogin('Google'));
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', handleModalKeyboard);
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', (event) => {
        if (!navbar.contains(event.target) && navMenu.classList.contains('active')) {
            closeMobileMenu();
        }
    });
    
    // Handle window resize
    window.addEventListener('resize', debounce(() => {
        if (window.innerWidth > 768 && navMenu.classList.contains('active')) {
            closeMobileMenu();
        }
    }, 100));
});

// Service Worker registration for better performance (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then((registration) => {
                console.log('SW registered: ', registration);
            })
            .catch((registrationError) => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Analytics and tracking (placeholder)
function trackEvent(eventName, properties = {}) {
    // Placeholder for analytics tracking
    console.log('Event tracked:', eventName, properties);
}

// Track user interactions
document.addEventListener('click', (event) => {
    if (event.target.matches('.btn-primary')) {
        trackEvent('cta_clicked', {
            button_text: event.target.textContent.trim(),
            page_location: window.location.pathname
        });
    }
});

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        handleExchangeToggle,
        createSessionCard,
        smoothScroll,
        debounce
    };
}
