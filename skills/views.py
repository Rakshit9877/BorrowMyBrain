from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import UserProfile, Skill, TeachableSkill, Certification, SkillRequest
from .forms import UserProfileForm, TeachableSkillForm, CertificationForm, SkillRequestForm


def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try to authenticate with username first, then email
        user = authenticate(request, username=username, password=password)
        if user is None and '@' in username:
            # Try to find user by email and authenticate with username
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
                
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username/email or password.')
    
    return render(request, 'skills/login.html')


def signup_view(request):
    """Handle user signup"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # Basic validation
        errors = []
        if User.objects.filter(username=username).exists():
            errors.append('Username already exists.')
        if User.objects.filter(email=email).exists():
            errors.append('Email already registered.')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        if not request.POST.get('terms_accepted'):
            errors.append('You must accept the terms and conditions.')
            
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'skills/signup.html')
            
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        # Log in the user
        login(request, user)
        messages.success(request, f'Welcome to BorrowMyBrain, {user.get_full_name() or user.username}! Please complete your profile.')
        return redirect('create_profile')
    
    return render(request, 'skills/signup.html')


def login_signup(request):
    """Renders a page to choose between login and signup."""
    return render(request, 'skills/login_signup.html')


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def home(request):
    """Homepage with personalized content for authenticated users"""
    context = {}
    
    if request.user.is_authenticated:
        # Get user profile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # Get skills with different price ranges for personalized recommendations
        affordable_skills = TeachableSkill.objects.select_related('skill', 'user_profile__user').filter(
            user_profile__hourly_rate__lte=30
        )[:4]
        
        mid_range_skills = TeachableSkill.objects.select_related('skill', 'user_profile__user').filter(
            user_profile__hourly_rate__gt=30,
            user_profile__hourly_rate__lte=60
        )[:4]
        
        premium_skills = TeachableSkill.objects.select_related('skill', 'user_profile__user').filter(
            user_profile__hourly_rate__gt=60
        )[:4]
        
        # Get recently joined educators
        recent_educators = UserProfile.objects.select_related('user').filter(
            teachable_skills__isnull=False
        ).distinct().order_by('-created_at')[:6]
        
        context.update({
            'user_profile': user_profile,
            'affordable_skills': affordable_skills,
            'mid_range_skills': mid_range_skills,
            'premium_skills': premium_skills,
            'recent_educators': recent_educators,
            'is_personalized': True,
        })
    else:
        # Regular homepage for anonymous users
        recommended_skills = TeachableSkill.objects.select_related('skill', 'user_profile__user').all()[:8]
        context.update({
            'recommended_skills': recommended_skills,
            'is_personalized': False,
        })
    
    return render(request, 'skills/home.html', context)


@login_required
def profile(request):
    """User profile page"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Handle profile form submission (placeholder)
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    context = {
        'user_profile': user_profile,
        'teachable_skills': user_profile.teachable_skills.all(),
        'certifications': user_profile.certifications.all(),
    }
    return render(request, 'skills/profile.html', context)


@login_required
def create_profile(request):
    """Page for users to complete their profile after signup"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update User model fields
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.save()
        
        # Update UserProfile fields - Step 1
        user_profile.bio = request.POST.get('bio', '')
        user_profile.location = request.POST.get('location', '')
        user_profile.phone_number = request.POST.get('phone_number', '')
        
        # Handle date of birth
        date_of_birth = request.POST.get('date_of_birth')
        if date_of_birth:
            user_profile.date_of_birth = date_of_birth
            
        # Handle profile picture
        if 'profile_picture' in request.FILES:
            user_profile.profile_picture = request.FILES['profile_picture']
        
        # Step 2: Availability fields
        available_days = request.POST.getlist('available_days')
        user_profile.available_days = available_days
        user_profile.preferred_time = request.POST.get('preferred_time', '')
        user_profile.teaching_mode = request.POST.get('teaching_mode', '')
        
        # Step 3: Skills & Rates
        user_profile.hourly_rate_range = request.POST.get('hourly_rate_range', '')
        user_profile.experience_level = request.POST.get('experience_level', '')
        user_profile.general_teaching_hours = request.POST.get('general_teaching_hours', '')
        
        # Convert hourly rate range to actual rate for compatibility
        hourly_rate_range = request.POST.get('hourly_rate_range', '')
        if hourly_rate_range:
            if hourly_rate_range == '10-20':
                user_profile.hourly_rate = 15.00
            elif hourly_rate_range == '20-35':
                user_profile.hourly_rate = 27.50
            elif hourly_rate_range == '35-50':
                user_profile.hourly_rate = 42.50
            elif hourly_rate_range == '50-75':
                user_profile.hourly_rate = 62.50
            elif hourly_rate_range == '75-100':
                user_profile.hourly_rate = 87.50
            elif hourly_rate_range == '100+':
                user_profile.hourly_rate = 100.00
            
        user_profile.save()

        messages.success(request, 'Your profile has been created successfully! Welcome to BorrowMyBrain!')
        return redirect('profile')

    context = {
        'user_profile': user_profile
    }
    return render(request, 'skills/create_profile.html', context)


def search_results(request):
    """Search results page for skills with filtering"""
    query = request.GET.get('q', '')
    skill_filter = request.GET.get('skill', '')
    rate_filter = request.GET.get('rate', '')
    
    # Get UserProfile objects (educators) with their teachable skills
    educators = UserProfile.objects.select_related('user').prefetch_related('teachable_skills__skill').all()
    
    if query:
        educators = educators.filter(
            Q(teachable_skills__skill__name__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(bio__icontains=query)
        ).distinct()
    
    if skill_filter:
        educators = educators.filter(teachable_skills__skill__name__icontains=skill_filter).distinct()
    
    # Filter by rate range
    if rate_filter:
        if rate_filter == 'low':
            educators = educators.filter(hourly_rate__lte=30)
        elif rate_filter == 'mid':
            educators = educators.filter(hourly_rate__gt=30, hourly_rate__lte=60)
        elif rate_filter == 'high':
            educators = educators.filter(hourly_rate__gt=60)
    
    context = {
        'educators': educators,
        'query': query,
        'skill_filter': skill_filter,
        'rate_filter': rate_filter,
    }
    return render(request, 'skills/search_results.html', context)


def view_profile(request, user_id):
    """View educator's full profile"""
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    teachable_skills = user_profile.teachable_skills.all()
    certifications = user_profile.certifications.all()
    
    context = {
        'user_profile': user_profile,
        'teachable_skills': teachable_skills,
        'certifications': certifications,
    }
    return render(request, 'skills/view_profile.html', context)


@login_required
def make_skill_request(request, teachable_skill_id):
    """Handle skill request (payment or skill exchange)"""
    teachable_skill = get_object_or_404(TeachableSkill, id=teachable_skill_id)
    
    if request.method == 'POST':
        request_type = request.POST.get('request_type')
        
        skill_request = SkillRequest.objects.create(
            learner=request.user,
            educator=teachable_skill.user_profile.user,
            requested_skill=teachable_skill,
        )
        
        if request_type == 'payment':
            skill_request.is_payment_offer = True
            skill_request.offered_amount = request.POST.get('offered_amount', 0)
        else:
            skill_request.is_payment_offer = False
            skill_request.offered_skill = request.POST.get('offered_skill', '')
        
        skill_request.message = request.POST.get('message', '')
        skill_request.save()
        
        messages.success(request, 'Your request has been sent to the educator!')
        return redirect('view_profile', user_id=teachable_skill.user_profile.user.id)
    
    context = {
        'teachable_skill': teachable_skill,
    }
    return render(request, 'skills/request_skill.html', context)
