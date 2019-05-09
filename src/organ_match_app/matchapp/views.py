from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from  .forms import UserRegistrationForm, OrganRequestForm, UserProfileForm
from .models import UserProfile
from django.contrib.auth.models import User

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
def profile(request):
    curr_user_id = request.user.id

    if request.method == 'POST':
        print("post")
    else:
        if UserProfile.objects.filter(user_id=curr_user_id).exists():
            user = UserProfile.objects.filter(user_id=curr_user_id).values()[0]
            print('exists')
            print(user.get('last_name'))
            context = {
                'form_exists': False,
                'first_name': user.get('first_name'),
                'last_name': user.get('last_name'),
                'birth_date': user.get('birth_date'),
                'blood_type': user.get('blood_type'),
                'doctor_id': user.get('doctor_id'),
                'profile_id': user.get('id'),
            }
        else:            
            context = {
                'form_exists': True,
                'form': UserProfileForm()
            }
    return render(request, 'matchapp/profile.html', context)

@login_required
def request(request):    
    curr_user_id = request.user.id
    
    if request.method == 'POST':
        form = OrganRequestForm(request.POST)
        if form.is_valid:
            input = request.POST.copy()
            # print(User.objects.filter(user=self.request.user))
            userprofile = UserProfile.objects.create(
                first_name=input.get('first_name'), 
                last_name=input.get('last_name'), 
                birth_date=input.get('birth_date'), 
                blood_type=input.get('blood_type'),
                    user_id=curr_user_id)

            # userprofile.save()           
    else:        
        if UserProfile.objects.filter(user_id=curr_user_id).exists():
            print(True)
        form = OrganRequestForm()
    return render(request, 'matchapp/request.html', {'form': form})

