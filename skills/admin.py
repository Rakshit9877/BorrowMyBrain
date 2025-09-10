from django.contrib import admin
from .models import UserProfile, Skill, TeachableSkill, Certification, SkillRequest


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'hourly_rate', 'rating', 'total_students']
    list_filter = ['location', 'rating']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category']
    search_fields = ['name', 'description']


@admin.register(TeachableSkill)
class TeachableSkillAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'skill', 'proficiency_level', 'experience_years']
    list_filter = ['proficiency_level', 'skill__category']
    search_fields = ['user_profile__user__username', 'skill__name']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user_profile', 'issuing_organization', 'issue_date']
    list_filter = ['issuing_organization', 'issue_date']
    search_fields = ['title', 'user_profile__user__username']


@admin.register(SkillRequest)
class SkillRequestAdmin(admin.ModelAdmin):
    list_display = ['learner', 'educator', 'requested_skill', 'status', 'is_payment_offer']
    list_filter = ['status', 'is_payment_offer', 'created_at']
    search_fields = ['learner__username', 'educator__username']
