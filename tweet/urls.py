from django.urls import path
from . import views  # ✅ Correct relative import
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home Page
    path('', views.index, name='index'),

    # Tweets
    path('tweet/', views.tweet_list, name='tweet_list'),
    path('tweet/create/', views.tweet_create, name='tweet_create'),
    path('tweet/<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('tweet/<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),

    # Authentication
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # Profile Page
    path('profile/', views.profile_view, name='profile'),

    # Teams Page
    path('teams/', views.team_list, name='teams_page'),

    # <-------Chat Url--->


    path('tweet/<str:room_name>/', views.chat_room, name ="chat"),
]


