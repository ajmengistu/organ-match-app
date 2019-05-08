from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from  .forms import UserRegistrationForm, OrganRequestForm
from .models import UserProfile

def home(request):
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM organs")
    #     row = cursor.fetchone()
    #     print(row)

    # result = 'hi'

    # context = {
    #     'result': result,
    #     'title': 'Home',
    # }
    return render(request, 'matchapp/home.html', {'title':'Home'})

def about(request):
    return render(request, 'matchapp/about.html', {'title': 'About'})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'matchapp/register.html', {'form' : form})

@login_required
def request(request):
    if request.method == 'POST':
        form = OrganRequestForm(request.POST)
        if form.is_valid:
            input = request.POST.copy()

            userprofile = UserProfile.objects.create(
                first_name=input.get('first_name'), 
                last_name=input.get('last_name'), 
                birth_date=input.get('birth_date'), 
                blood_type=input.get('blood_type'),
                doctor_id=12)

            userprofile.save()
            
            return redirect('request')
            print(userprofile)
            
    else:
        form = OrganRequestForm()
    return render(request, 'matchapp/request.html', {'form': form})