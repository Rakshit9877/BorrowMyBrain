from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile, Skill, TeachableSkill, Certification


class BorrowMyBrainTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Create user profile
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            bio='Test bio',
            location='Test City',
            hourly_rate=1000.00
        )
        
        # Create test skill
        self.skill = Skill.objects.create(
            name='Python Programming',
            description='Programming in Python',
            category='technology'
        )
        
        # Create teachable skill
        self.teachable_skill = TeachableSkill.objects.create(
            user_profile=self.user_profile,
            skill=self.skill,
            proficiency_level='advanced',
            experience_years=5,
            description='Expert Python developer'
        )

    def test_home_page_loads(self):
        """Test that home page loads successfully"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Share Your Skills')

    def test_login_page_loads(self):
        """Test that login page loads successfully"""
        response = self.client.get(reverse('login_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to BorrowMyBrain')

    def test_search_results_page(self):
        """Test search functionality"""
        response = self.client.get(reverse('search_results'))
        self.assertEqual(response.status_code, 200)
        
        # Test search with query
        response = self.client.get(reverse('search_results'), {'q': 'Python'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Programming')

    def test_view_profile_page(self):
        """Test educator profile view"""
        response = self.client.get(reverse('view_profile', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')
        self.assertContains(response, 'Python Programming')

    def test_profile_page_requires_login(self):
        """Test that profile page requires authentication"""
        response = self.client.get(reverse('profile'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        
        # Test with logged in user
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_user_profile_creation(self):
        """Test UserProfile model"""
        self.assertEqual(str(self.user_profile), "testuser's Profile")
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(self.user_profile.hourly_rate, 1000.00)

    def test_skill_model(self):
        """Test Skill model"""
        self.assertEqual(str(self.skill), 'Python Programming')
        self.assertEqual(self.skill.category, 'technology')

    def test_teachable_skill_model(self):
        """Test TeachableSkill model"""
        expected_str = "testuser - Python Programming"
        self.assertEqual(str(self.teachable_skill), expected_str)
        self.assertEqual(self.teachable_skill.proficiency_level, 'advanced')
        self.assertEqual(self.teachable_skill.experience_years, 5)

    def test_certification_model(self):
        """Test Certification model"""
        cert = Certification.objects.create(
            user_profile=self.user_profile,
            title='AWS Certified Developer',
            issuing_organization='Amazon Web Services',
            issue_date='2023-01-01',
            description='AWS certification'
        )
        
        expected_str = "AWS Certified Developer - testuser"
        self.assertEqual(str(cert), expected_str)


class ModelValidationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )

    def test_user_profile_defaults(self):
        """Test UserProfile default values"""
        profile = UserProfile.objects.create(user=self.user)
        
        self.assertEqual(profile.rating, 0.00)
        self.assertEqual(profile.total_students, 0)
        self.assertEqual(profile.total_lessons, 0)
        self.assertTrue(profile.created_at)
        self.assertTrue(profile.updated_at)

    def test_skill_categories(self):
        """Test skill category choices"""
        categories = ['technology', 'language', 'arts', 'music', 'sports', 'cooking', 'business', 'other']
        
        for category in categories:
            skill = Skill.objects.create(
                name=f'Test {category.title()}',
                category=category
            )
            self.assertEqual(skill.category, category)


class ViewPermissionTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='permuser',
            email='perm@example.com',
            password='testpass123'
        )

    def test_anonymous_user_access(self):
        """Test what anonymous users can access"""
        # Public pages should be accessible
        public_urls = [
            reverse('home'),
            reverse('login_signup'),
            reverse('search_results'),
        ]
        
        for url in public_urls:
            response = self.client.get(url)
            self.assertIn(response.status_code, [200, 302])  # 200 OK or redirect

    def test_authenticated_user_access(self):
        """Test authenticated user access"""
        self.client.login(username='permuser', password='testpass123')
        
        # Should be able to access profile
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
