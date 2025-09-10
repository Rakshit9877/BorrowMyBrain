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
    
    # New fields for enhanced profile
    available_days = models.JSONField(default=list, blank=True, help_text="List of available days")
    preferred_time = models.CharField(max_length=20, blank=True, choices=[
        ('early_morning', 'Early Morning (6:00 AM - 9:00 AM)'),
        ('morning', 'Morning (9:00 AM - 12:00 PM)'),
        ('afternoon', 'Afternoon (12:00 PM - 5:00 PM)'),
        ('evening', 'Evening (5:00 PM - 8:00 PM)'),
        ('night', 'Night (8:00 PM - 11:00 PM)'),
        ('flexible', 'Flexible'),
    ])
    teaching_mode = models.CharField(max_length=20, blank=True, choices=[
        ('online', 'Online Only'),
        ('in_person', 'In-Person Only'),
        ('both', 'Both Online & In-Person'),
    ])
    hourly_rate_range = models.CharField(max_length=20, blank=True, choices=[
        ('10-20', '$10 - $20 per hour'),
        ('20-35', '$20 - $35 per hour'),
        ('35-50', '$35 - $50 per hour'),
        ('50-75', '$50 - $75 per hour'),
        ('75-100', '$75 - $100 per hour'),
        ('100+', '$100+ per hour'),
    ])
    experience_level = models.CharField(max_length=20, blank=True, choices=[
        ('beginner', 'New to teaching (0-1 years)'),
        ('intermediate', 'Some experience (1-3 years)'),
        ('experienced', 'Experienced (3-5 years)'),
        ('expert', 'Highly experienced (5+ years)'),
    ])
    
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


class Session(models.Model):
    """Learning session between users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, blank=True, null=True)
    room_name = models.CharField(max_length=200, unique=True)
    room_url = models.URLField()
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='active')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.room_name} - {self.user.username}"


class SessionRecording(models.Model):
    """Recording information for sessions"""
    session = models.OneToOneField(Session, on_delete=models.CASCADE, related_name='recording')
    recording_id = models.CharField(max_length=200)
    download_url = models.URLField()
    gcs_uri = models.CharField(max_length=500, blank=True, null=True)
    file_size = models.BigIntegerField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recording for {self.session.room_name}"


class SessionSummary(models.Model):
    """AI-generated session summaries"""
    session = models.OneToOneField(Session, on_delete=models.CASCADE, related_name='summary')
    transcript = models.TextField()
    summary = models.TextField()
    language = models.CharField(max_length=10, default='hi', choices=[
        ('hi', 'Hindi'),
        ('en', 'English'),
    ])
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary for {self.session.room_name}"


class SessionNotes(models.Model):
    """User notes during sessions"""
    session = models.OneToOneField(Session, on_delete=models.CASCADE, related_name='notes')
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notes for {self.session.room_name}"
