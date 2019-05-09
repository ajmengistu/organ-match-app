from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from  .forms import UserRegistrationForm, OrganRequestForm, UserProfileForm
from .models import UserProfile
from django.contrib.auth.models import User
import datetime


def home(request):
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


def calculate_age(bday):
    today = datetime.date.today()
    return (today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day)))

def add_profile(curr_user_id, input):
    userprofile = UserProfile.objects.create(
                    user_id = curr_user_id,
                    first_name = input.get('first_name'),
                    last_name = input.get('last_name'),
                    birth_date = input.get('birth_date'),
                    blood_type = input.get('blood_type'),
                )

@login_required
def profile(request):
    curr_user_id = request.user.id

    if request.method == 'POST':
        form = UserProfileForm(request.POST)

        if form.is_valid():            
            input = request.POST.copy()
            age = calculate_age(datetime.datetime.strptime(input.get('birth_date'), "%Y-%m-%d").date())
            
            if age < 18:            
                messages.error(request, f'You must be 18 years of age or older!')                    
            else:
                add_profile(curr_user_id, input)
                messages.success(request, f'You profile was created successfully.')                    
        else:
            messages.warning(request, f'Please provide correct date format!')

        return redirect('profile')
    else:        
        if UserProfile.objects.filter(user_id=curr_user_id).exists():
            user = UserProfile.objects.filter(user_id=curr_user_id).values()[0]            
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
            print(input)
            # date = self.cleaned_data['date']
            # if date < datetime.date.today():
                # raise forms.ValidationError("The date cannot be in the past!")
            # userprofile = Needs.objects.create(
                #user_id = curr_user_id
                # need_by = input.get('need_by'), 
                # organ = input.get('organ'), 
            # )
            # userprofile.save()
            #            
    else:        
        if UserProfile.objects.filter(user_id=curr_user_id).exists():
            form = OrganRequestForm()
        else:
            return redirect('profile')
    return render(request, 'matchapp/request.html', {'form': form})

