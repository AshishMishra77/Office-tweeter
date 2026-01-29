from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Main app
    path('', include('tweet.urls')),  # ✅ include all routes (index, tweet, teams, profile, etc.)

    # Authentication
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
