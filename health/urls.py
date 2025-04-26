from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'programs', views.HealthProgramViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'enrollments', views.EnrollmentViewSet)

web_urlpatterns = [
    path('programs/', views.program_list, name='program_list'),
    path('programs/create/', views.program_create, name='program_create'),
    path('programs/<int:program_id>/edit/', views.edit_program, name='edit_program'),
    path('programs/<int:program_id>/delete/', views.delete_program, name='delete_program'),
    path('clients/', views.client_list, name='client_list'),
    path('clients/registeration/', views.client_registeration, name='client_registeration'),
    path('clients/<int:client_id>/', views.client_detail, name='client_detail'),
    path('clients/<int:client_id>/enroll/', views.enroll_client, name='enroll_client'),
    path('enrollments/<int:enrollment_id>/remove/', views.remove_enrollment, name='remove_enrollment'),
    path('clients/search/', views.client_search, name='client_search'),
    path('clients/search/quick/', views.quick_client_search, name='quick_client_search'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('clients/<int:pk>/detail/', views.ClientDetailView.as_view(), name='client-detail'),
]

urlpatterns = web_urlpatterns + router.urls