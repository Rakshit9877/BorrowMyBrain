from django.urls import path
from . import views
from . import session_views_production as session_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login_signup/', views.login_signup, name='login_signup'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/create/', views.create_profile, name='create_profile'),
    path('search/', views.search_results, name='search_results'),
    path('educator/<int:user_id>/', views.view_profile, name='view_profile'),
    path('request/<int:teachable_skill_id>/', views.make_skill_request, name='make_skill_request'),
    
    # Session URLs
    path('session/start/', session_views.start_session, name='start_session'),
    path('session/start/<int:skill_id>/', session_views.start_session, name='start_session_with_skill'),
    path('session/demo/', session_views.start_demo_session, name='start_demo_session'),
    path('session/room/<slug:room_code>/', session_views.start_session_by_code, name='start_session_by_code'),
    path('session/join/', views.test_session_page, name='join_session_page'),
    path('session/test/', views.test_session_page, name='test_session_page'),
    path('session/demo/', session_views.start_demo_session, name='start_demo_session'),
    path('session/join/', session_views.join_session_page, name='join_session_page'),
    path('session/join/submit/', session_views.join_session_submit, name='join_session_submit'),
    
    # Session API endpoints
    path('api/generate-summary/', session_views.generate_summary_api, name='generate_summary_api'),
    path('api/process-recording/', session_views.process_recording_api, name='process_recording_api'),
    path('api/save-session-notes/', session_views.save_session_notes_api, name='save_session_notes_api'),
]
