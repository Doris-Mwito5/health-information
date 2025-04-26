from django.contrib import admin
from django.urls import path, include
from health import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'programs', views.HealthProgramViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'enrollments', views.EnrollmentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('health/', include('health.urls')),
    path('account/', include('main.urls')),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('api/', include(router.urls)),
    path('api/token-auth/', obtain_auth_token, name='api_token_auth'),
]