from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile for skill sharing"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    general_teaching_hours = models.CharField(max_length=100, blank=True, help_text="e.g., Weekdays 6-9 PM")
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_students = models.IntegerField(default=0)
    total_lessons = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Skill(models.Model):
    """Available skills in the platform"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=[
        ('technology', 'Technology'),
        ('language', 'Language'),
        ('arts', 'Arts & Crafts'),
        ('music', 'Music'),
        ('sports', 'Sports'),
        ('cooking', 'Cooking'),
        ('business', 'Business'),
        ('other', 'Other'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TeachableSkill(models.Model):
    """Skills that a user can teach"""
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='teachable_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ])
    experience_years = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_profile', 'skill')

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.skill.name}"


class Certification(models.Model):
    """User certifications"""
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user_profile.user.username}"


class SkillRequest(models.Model):
    """Requests for skill exchange or payment"""
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_requests')
    educator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_offers')
    requested_skill = models.ForeignKey(TeachableSkill, on_delete=models.CASCADE)
    
    # Payment or skill exchange
    is_payment_offer = models.BooleanField(default=True)
    offered_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    offered_skill = models.CharField(max_length=200, blank=True, null=True)
    
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.learner.username} -> {self.educator.username} ({self.requested_skill.skill.name})"
