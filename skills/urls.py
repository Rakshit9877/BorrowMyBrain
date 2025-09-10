from django.urls import path
from . import views

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
]
