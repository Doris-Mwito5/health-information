from django.contrib import admin
from .models import HealthProgram, Client, ClientEnrollment, ContactMessage

@admin.register(HealthProgram)
class HealthProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'created_by', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'gender', 'contact_number', 'email')
    list_filter = ('gender', 'created_at')
    search_fields = ('first_name', 'last_name', 'contact_number', 'email')
    date_hierarchy = 'created_at'

@admin.register(ClientEnrollment)
class ClientEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'program', 'enrollment_date')
    list_filter = ('program', 'enrollment_date')
    search_fields = ('client__first_name', 'client__last_name', 'program__name')
    raw_id_fields = ('client', 'program')
    date_hierarchy = 'enrollment_date'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    date_hierarchy = 'created_at'