from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, MeterReadingForm
from .models import Profile, MeterReading

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            bsl_staff_no = form.cleaned_data.get('bsl_staff_no')
            Profile.objects.create(user=user, bsl_staff_no=bsl_staff_no)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/password_reset.html', {'form': form})

@login_required
def home(request):
    return render(request, 'accounts/home.html')

@login_required
def account(request):
    return render(request, 'accounts/account.html')

@login_required
def electricity(request):
    form = MeterReadingForm()
    return render(request, 'accounts/electricity.html', {'form': form})

@login_required
def save_reading(request):
    if request.method == 'POST':
        form = MeterReadingForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.electricity_units = instance.current_reading - (instance.previous_reading or 0)
            instance.save()
            return redirect('success')  # Replace with your success URL
    else:
        form = MeterReadingForm()
    
    return render(request, 'accounts/electricity.html', {'form': form})  # Removed the duplicate 'return' statement
@login_required
def upload_meter_reading(request):
    if request.method == 'POST':
        form = MeterReadingForm(request.POST, request.FILES)
        if form.is_valid():
            meter_reading = form.save(commit=False)
            meter_reading.user = request.user
            meter_reading.save()
            return redirect('success')  # Redirect to a success page
    else:
        form = MeterReadingForm()
    return render(request, 'accounts/upload_meter_reading.html', {'form': form})

def success(request):
    return render(request, 'accounts/success.html')

