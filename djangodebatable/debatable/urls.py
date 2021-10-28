"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from users import views as user_views
from posts import views as post_views
from pages import views as pages_views
from posts.views import like_view
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view, search_view, construction_view
from users.views import quiz_view, feedback_view

urlpatterns = [
    path('pages/', include('pages.urls')),
    path('chat/', include('chat.urls')),
    path('chat/search_view', search_view, name='search_view'),
    path('posts/', include('posts.urls')),
    path('profile/<str:username>/search_view', search_view, name='search_view'),
    path('admin/', admin.site.urls),
    path('profiles/', include('profiles.urls')),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', include('users.urls')),
    path('', home_view, name="home"),
    path('profileChange/', user_views.profileChange, name='profileChange'),
    path('chat/like_view', like_view, name='like_view'),
    path('profile/<str:username>/like_view', like_view, name='like_view'),
    path('quiz/', quiz_view, name="quiz"),
    path('profileChange/', user_views.profileChange, name='profileChange'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('construction/', construction_view, name="construction"),
    path('feedback/', feedback_view, name='feedback')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
