from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, TeachableSkill, Certification, SkillRequest, Skill


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'phone_number', 'date_of_birth', 
                 'location', 'general_teaching_hours', 'hourly_rate']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'general_teaching_hours': forms.TextInput(attrs={'placeholder': 'e.g., Weekdays 6-9 PM'}),
        }


class TeachableSkillForm(forms.ModelForm):
    skill = forms.ModelChoiceField(queryset=Skill.objects.all(), empty_label="Select a skill")
    
    class Meta:
        model = TeachableSkill
        fields = ['skill', 'proficiency_level', 'experience_years', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['title', 'issuing_organization', 'issue_date', 'expiry_date', 
                 'certificate_file', 'description']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class SkillRequestForm(forms.ModelForm):
    class Meta:
        model = SkillRequest
        fields = ['offered_amount', 'offered_skill', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }
