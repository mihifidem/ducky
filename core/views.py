from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# esta parte redirecciona dependiendo 

def home(request):
    if request.user.is_authenticated:
        return redirect('redireccion_dashboard')
    else:
        return render(request, 'home.html')

@login_required
def redireccion_dashboard(request):
    user_profile = request.user.userprofile
    role = user_profile.role.lower()

    if role == 'user':
        return redirect('dashboard_user')
    elif role == 'premium':
        return redirect('dashboard_premium')
    elif role == 'admin':
        return redirect('dashboard_admin')
    elif role == 'teacher':
        return redirect('dashboard_teacher')
    elif role == 'headhunter':
        return redirect('dashboard_headhunter')
    elif role == 'professional':
        return redirect('dashboard_professional')
    else:
        return redirect('home')

@login_required
def dashboard_user(request):
    return render(request, 'core/dashboard_user.html')

@login_required
def dashboard_premium(request):
    return render(request, 'core/dashboard_premium.html')

@login_required
def dashboard_admin(request):
    return render(request, 'core/dashboard_admin.html')

@login_required
def dashboard_teacher(request):
    return render(request, 'core/dashboard_teacher.html')

@login_required
def dashboard_headhunter(request):
    return render(request, 'core/dashboard_headhunter.html')  

@login_required
def dashboard_profesional(request):
    return render(request, 'core/dashboard_professional.html')
