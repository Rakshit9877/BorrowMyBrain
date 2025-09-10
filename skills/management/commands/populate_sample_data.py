from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from skills.models import UserProfile, Skill, TeachableSkill, Certification
from datetime import date


class Command(BaseCommand):
    help = 'Populate the database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create sample skills
        skills_data = [
            {'name': 'Python Programming', 'category': 'technology', 'description': 'Programming in Python language'},
            {'name': 'JavaScript', 'category': 'technology', 'description': 'JavaScript programming'},
            {'name': 'React', 'category': 'technology', 'description': 'React.js framework'},
            {'name': 'Django', 'category': 'technology', 'description': 'Django web framework'},
            {'name': 'Machine Learning', 'category': 'technology', 'description': 'ML and AI concepts'},
            {'name': 'Data Science', 'category': 'technology', 'description': 'Data analysis and visualization'},
            {'name': 'English Language', 'category': 'language', 'description': 'English conversation and grammar'},
            {'name': 'Spanish Language', 'category': 'language', 'description': 'Spanish conversation and grammar'},
            {'name': 'Guitar', 'category': 'music', 'description': 'Acoustic and electric guitar'},
            {'name': 'Piano', 'category': 'music', 'description': 'Piano and keyboard'},
            {'name': 'Photography', 'category': 'arts', 'description': 'Digital photography'},
            {'name': 'Cooking', 'category': 'cooking', 'description': 'Various cooking techniques'},
        ]

        for skill_data in skills_data:
            skill, created = Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults=skill_data
            )
            if created:
                self.stdout.write(f'Created skill: {skill.name}')

        # Create sample users and profiles
        users_data = [
            {
                'username': 'john_doe',
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'profile': {
                    'bio': 'Experienced software developer with 8+ years in Python and web development.',
                    'location': 'Mumbai, India',
                    'hourly_rate': 1500.00,
                    'general_teaching_hours': 'Weekdays 7-10 PM, Weekends 10 AM - 6 PM',
                    'rating': 4.8,
                    'total_students': 25,
                    'total_lessons': 150,
                },
                'skills': [
                    {'skill': 'Python Programming', 'level': 'expert', 'years': 8},
                    {'skill': 'Django', 'level': 'advanced', 'years': 5},
                    {'skill': 'Machine Learning', 'level': 'intermediate', 'years': 3},
                ]
            },
            {
                'username': 'sarah_wilson',
                'email': 'sarah@example.com',
                'first_name': 'Sarah',
                'last_name': 'Wilson',
                'profile': {
                    'bio': 'Professional English teacher and language coach with international experience.',
                    'location': 'Delhi, India',
                    'hourly_rate': 800.00,
                    'general_teaching_hours': 'Flexible hours, prefer mornings',
                    'rating': 4.9,
                    'total_students': 45,
                    'total_lessons': 320,
                },
                'skills': [
                    {'skill': 'English Language', 'level': 'expert', 'years': 10},
                    {'skill': 'Spanish Language', 'level': 'advanced', 'years': 6},
                ]
            },
            {
                'username': 'mike_guitarist',
                'email': 'mike@example.com',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'profile': {
                    'bio': 'Professional musician and guitar instructor. Specializing in rock, blues, and classical guitar.',
                    'location': 'Bangalore, India',
                    'hourly_rate': 1200.00,
                    'general_teaching_hours': 'Evenings and weekends',
                    'rating': 4.7,
                    'total_students': 30,
                    'total_lessons': 200,
                },
                'skills': [
                    {'skill': 'Guitar', 'level': 'expert', 'years': 12},
                    {'skill': 'Piano', 'level': 'intermediate', 'years': 5},
                ]
            },
            {
                'username': 'chef_priya',
                'email': 'priya@example.com',
                'first_name': 'Priya',
                'last_name': 'Sharma',
                'profile': {
                    'bio': 'Culinary expert specializing in Indian and international cuisine.',
                    'location': 'Chennai, India',
                    'hourly_rate': 900.00,
                    'general_teaching_hours': 'Weekends, morning and evening sessions',
                    'rating': 4.6,
                    'total_students': 20,
                    'total_lessons': 80,
                },
                'skills': [
                    {'skill': 'Cooking', 'level': 'expert', 'years': 15},
                ]
            },
            {
                'username': 'alex_photographer',
                'email': 'alex@example.com',
                'first_name': 'Alex',
                'last_name': 'Chen',
                'profile': {
                    'bio': 'Professional photographer and photo editor with expertise in portrait and landscape photography.',
                    'location': 'Pune, India',
                    'hourly_rate': 1100.00,
                    'general_teaching_hours': 'Weekends and flexible weekday evenings',
                    'rating': 4.5,
                    'total_students': 18,
                    'total_lessons': 95,
                },
                'skills': [
                    {'skill': 'Photography', 'level': 'expert', 'years': 8},
                ]
            },
        ]

        for user_data in users_data:
            # Create user
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )

            if created:
                user.set_password('password123')  # Set a default password
                user.save()
                self.stdout.write(f'Created user: {user.username}')

                # Create user profile
                profile = UserProfile.objects.create(
                    user=user,
                    **user_data['profile']
                )

                # Add teachable skills
                for skill_data in user_data['skills']:
                    skill = Skill.objects.get(name=skill_data['skill'])
                    TeachableSkill.objects.create(
                        user_profile=profile,
                        skill=skill,
                        proficiency_level=skill_data['level'],
                        experience_years=skill_data['years'],
                        description=f"Expert in {skill.name} with {skill_data['years']} years of experience."
                    )

                # Add sample certifications for some users
                if user.username == 'john_doe':
                    Certification.objects.create(
                        user_profile=profile,
                        title='Python Developer Certificate',
                        issuing_organization='Python Institute',
                        issue_date=date(2020, 6, 15),
                        description='Advanced Python programming certification'
                    )
                    Certification.objects.create(
                        user_profile=profile,
                        title='Django Web Developer',
                        issuing_organization='Django Foundation',
                        issue_date=date(2021, 3, 10),
                        description='Full-stack Django development certification'
                    )

                elif user.username == 'sarah_wilson':
                    Certification.objects.create(
                        user_profile=profile,
                        title='TEFL Certificate',
                        issuing_organization='International TEFL Academy',
                        issue_date=date(2018, 8, 20),
                        description='Teaching English as a Foreign Language certification'
                    )

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.stdout.write('You can now browse the application with sample educators and skills.')
        self.stdout.write('Default password for all sample users: password123')
