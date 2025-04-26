from datetime import date
from django.db.models import Q
from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import HealthProgram, Client, ClientEnrollment
from .forms import HealthProgramForm, ContactForm, ClientRegistrationForm, EnrollmentForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Count
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets, generics, filters
from rest_framework.response import Response
from .serializers import (HealthProgramSerializer, ClientSerializer, ClientDetailSerializer, EnrollmentSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny



def doctor_required(view_func=None, redirect_url='home'):
   
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_doctor,
        login_url=redirect_url,
        redirect_field_name=None
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


@login_required
def program_list(request):
    programs = HealthProgram.objects.filter(created_by=request.user).order_by('-id')
    paginator = Paginator(programs, 10)
    page_number = request.GET.get('pg')
    page_obj = paginator.get_page(page_number)
    return render(request, 'program_list.html', {'programs': page_obj})

@login_required
def program_create(request):
    if request.method == 'POST':
        form = HealthProgramForm(request.POST)
        if form.is_valid():
            program = form.save(commit=False)
            program.created_by = request.user
            program.save()
            messages.success(request, 'Program created successfully!')
            return redirect('program_list')
    else:
        form = HealthProgramForm()
    return render(request, 'program_create.html', {'form': form})

@login_required
def edit_program(request, program_id):
    program = HealthProgram.objects.get(pk=program_id)
    
    if request.method == 'POST':
        form = HealthProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program updated successfully!')
            return redirect('program_list')
    else:
        form = HealthProgramForm(instance=program)
    
    return render(request, 'edit_program.html', {
        'form': form,
        'program': program  
    })
    
@login_required
def delete_program(request, program_id):
    program = HealthProgram.objects.get(pk=program_id)
    if program.created_by == request.user:
        program.delete()
        messages.success(request, 'Program deleted successfully!')
        return redirect('program_list')

def home(request):
    context = {
        'home_text':"Welcome Homepage Page.",
    }
    return render(request, 'home.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, "Message sent successfully! 🎉")
            return redirect('contact') 
        else:
            messages.error(request, "Oops! Please correct the errors below.")
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def about(request):
    context = {
        'about_text':"Welcome To About Page.",
    }
    return render(request, 'about.html', context)

def dashboard(request):
    context = {
        'about_text':"Welcome To The Dashboard.",
    }
    return render(request, 'dashboard.html', context)

def client_registeration(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()
            messages.success(request, f'Client {client.first_name} {client.last_name} registered successfully!')
            return redirect('client_list')
    else:
        form = ClientRegistrationForm()
    
    return render(request, 'sign.html', {'form': form})

@login_required
def client_list(request):
    clients = Client.objects.filter(created_by=request.user).order_by('-created_at')
    
    for client in clients:
        today = date.today()
        client.age = today.year - client.date_of_birth.year - ((today.month, today.day) < (client.date_of_birth.month, client.date_of_birth.day))
    
    paginator = Paginator(clients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'list.html', {'clients': page_obj})

@login_required
def enroll_client(request, client_id):
    client = Client.objects.get(pk=client_id)
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, client=client)
        if form.is_valid():
            programs = form.cleaned_data['programs']
            notes = form.cleaned_data['notes']
            success_count = 0
            
            for program in programs:
                try:
                    ClientEnrollment.objects.create(
                        client=client,
                        program=program,
                        notes=notes
                    )
                    success_count += 1
                except IntegrityError:
                    continue 
            
            if success_count > 0:
                if success_count == 1:
                    messages.success(request, "Successfully enrolled in 1 program")
                else:
                    messages.success(request, f"Successfully enrolled in {success_count} programs")
            else:
                messages.warning(request, "No new programs were added")
            
            return redirect('client_detail', client_id=client.id)
    else:
        form = EnrollmentForm(client=client)
    
    return render(request, 'enroll.html', {
        'form': form,
        'client': client
    })

@login_required
def client_detail(request, client_id):
    client = Client.objects.get(pk=client_id)
    enrollments = client.enrollments.select_related('program').all()
    
    enrolled_program_ids = enrollments.values_list('program_id', flat=True)
    available_programs = HealthProgram.objects.exclude(id__in=enrolled_program_ids)
    
    return render(request, 'detail.html', {
        'client': client,
        'enrollments': enrollments,
        'has_available_programs': available_programs.exists()
    })

@login_required
def remove_enrollment(request, enrollment_id):
    enrollment = ClientEnrollment.objects.get(pk=enrollment_id)
    
    if request.method == 'POST':
        program_name = enrollment.program.name
        enrollment.delete()
        messages.success(request, f'Successfully removed from {program_name}')
    
    return redirect('client_detail', client_id=enrollment.client.id)

@login_required
def client_search(request):
    query = request.GET.get('q', '').strip()
    
    if query:
        clients = Client.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(contact_number__icontains=query) |
            Q(address__icontains=query),
            created_by=request.user
        ).order_by('last_name', 'first_name')
    else:
        clients = Client.objects.none()
    
    paginator = Paginator(clients, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'search.html', {
        'clients': page_obj,
        'query': query,
        'results_count': clients.count()
    })

@login_required
def quick_client_search(request):
    query = request.GET.get('q', '').strip()
    clients = []
    
    if query:
        clients = Client.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query),
            created_by=request.user
        ).annotate(
            enrollments_count=Count('enrollments')
        ).values(
            'id', 
            'first_name', 
            'last_name', 
            'contact_number',
            'enrollments_count'
        )[:10] 
    
    return JsonResponse({
        'clients': list(clients),
        'query': query
    })

class HealthProgramViewSet(viewsets.ModelViewSet):
    queryset = HealthProgram.objects.all()
    serializer_class = HealthProgramSerializer

class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name', 'contact_number', 'email']
    filterset_fields = ['gender']

class ClientDetailView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientDetailSerializer
    lookup_field = 'pk'

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = ClientEnrollment.objects.all()
    serializer_class = EnrollmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'program']