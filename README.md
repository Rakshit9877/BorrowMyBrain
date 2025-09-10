# BorrowMyBrain - Skill Sharing Platform

A Django-based skill sharing platform where users can offer to teach skills in exchange for payment or other skills.

## 🚀 Features

### Current Implementation
- **User Authentication System** (placeholder for teammate implementation)
- **User Profiles** with comprehensive information
- **Skill Management** - Users can add skills they can teach
- **Certification Upload** - Users can upload and manage their certifications
- **Search & Discovery** - Browse and search for educators and skills
- **Request System** - Users can offer payment or skill exchange
- **Responsive Design** - Udemy-inspired color scheme and layout

### Pages Implemented
1. **Login/Signup Page** - Placeholder with basic structure
2. **Homepage** - Displays recommended skills and platform overview
3. **Profile Page** - Complete profile management with forms
4. **Search Results** - Grid view of educator cards with offer functionality
5. **View Profile** - Detailed educator profile with contact options

## 🛠 Tech Stack

- **Framework**: Django 4.2.7
- **Database**: SQLite (with Django ORM)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with Udemy color scheme
- **Icons**: Font Awesome
- **File Uploads**: Django file handling for images and certificates

## 🎨 Design System

### Color Palette (Udemy-inspired)
- **Primary Purple**: #A435F0 - Main brand color
- **Primary Black**: #1C1D1F - Headings and important text
- **Dark Gray**: #6A6F73 - Body text and subheadings
- **Light Gray**: #D1D7DC - Borders and dividers
- **White**: #FFFFFF - Primary background
- **Yellow-Orange**: #E59819 - Star ratings and accents

## 📋 Database Schema

### Core Models
- **UserProfile** - Extended user information
- **Skill** - Available skills with categories
- **TeachableSkill** - Skills a user can teach
- **Certification** - User certifications with file uploads
- **SkillRequest** - Payment or skill exchange requests

## 🔧 Setup Instructions

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   cd BorrowMyBrain
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open http://127.0.0.1:8000 in your browser
   - Admin panel: http://127.0.0.1:8000/admin

## 📱 Usage Guide

### For Educators
1. Create an account (placeholder - implementation pending)
2. Complete your profile with bio, skills, and certifications
3. Set your hourly rate and availability
4. Manage incoming skill requests

### For Learners
1. Browse available skills on the homepage
2. Use search to find specific skills or educators
3. View detailed educator profiles
4. Make payment offers or propose skill exchanges

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📁 Project Structure

```
borrowmybrain/
├── borrowmybrain/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── skills/                 # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── forms.py           # Django forms
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin configuration
│   └── tests.py           # Test cases
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   └── skills/            # Skill app templates
├── static/                 # Static files
│   ├── css/
│   │   └── style.css      # Main stylesheet
│   └── js/
│       └── main.js        # JavaScript functionality
├── media/                  # User uploads (created automatically)
├── requirements.txt        # Python dependencies
└── manage.py              # Django management script
```

## 🔮 Planned Features

### Authentication Integration
- User registration and login (to be implemented by teammate)
- Password reset functionality
- Email verification

### Enhanced Features
- Real-time messaging between users
- Video call integration for lessons
- Payment gateway integration
- Review and rating system
- Advanced search filters
- Skill recommendation algorithm
- Notification system

## 🤝 Contributing

### For Teammate (Authentication Implementation)
The login/signup functionality is placeholder. Key integration points:
- Use Django's built-in User model
- UserProfile model will auto-create on user registration
- Login redirect should go to homepage or profile
- Forms are ready in `templates/skills/login_signup.html`

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Write tests for new features

## 🐛 Known Issues

1. **Authentication**: Login/signup forms are placeholder only
2. **File Uploads**: Media files need proper production configuration
3. **Search**: Basic search implementation - needs enhancement
4. **Mobile**: Some responsive design improvements needed

## 📞 Support

For questions or issues:
1. Check the Django documentation
2. Review the test cases for usage examples
3. Check the admin panel for data management

## 📄 License

This project is for educational purposes. Please add appropriate license as needed.

---

**Note**: This is a development version. Before deploying to production, ensure proper security settings, environment variables, and database configuration.
