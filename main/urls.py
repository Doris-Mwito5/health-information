from django.urls import path
from main import views
from main.views import logout_view
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('register', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
]

