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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'skills/login.html')


def signup_view(request):
    """Handle user signup"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Simple validation, should be replaced by a form
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('signup')
            
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', '')
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
    """Homepage with recommended skills"""
    # Get all skills for now (recommendation logic to be implemented)
    recommended_skills = TeachableSkill.objects.select_related('skill', 'user_profile__user').all()[:8]
    return render(request, 'skills/home.html', {'recommended_skills': recommended_skills})


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
        # This is a simplified version. A real implementation would use a Django form.
        user_profile.bio = request.POST.get('bio', '')
        user_profile.headline = request.POST.get('headline', '')
        # ... process other fields ...
        user_profile.save()
        
        # Also update User model
        request.user.first_name = request.POST.get('firstName', '')
        request.user.last_name = request.POST.get('lastName', '')
        request.user.save()

        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('profile') # Redirect to the main profile view after saving

    context = {
        'user_profile': user_profile
    }
    return render(request, 'skills/create_profile.html', context)


def search_results(request):
    """Search results page for skills"""
    query = request.GET.get('q', '')
    skill_filter = request.GET.get('skill', '')
    
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
    
    context = {
        'educators': educators,
        'query': query,
        'skill_filter': skill_filter,
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
