from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from  .forms import UserRegistrationForm, OrganRequestForm, PersonForm
from .models import Person
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

def add_person(curr_user_id, input):
    Person = Person.objects.create(
                    user_id = curr_user_id,
                    first_name = input.get('first_name'),
                    last_name = input.get('last_name'),
                    birth_date = input.get('birth_date'),
                    blood_type = input.get('blood_type'),
                )
    print("-------Added user profile information---------")

def assign_doctor(uid):
    """
    Assign a doctor to a person as they sign up for the first time.
	A doctor is assigned to a person by updating the person's doctor_id field with
	the doctor with the fewest patients. The number of patients is defined as the number of
	people assigned to that doctor through their doctor_id field. To break ties, choose
	the doctor with the smallest id.
    """
    print("--------Assigned a doctor to uid------------")

@login_required
def profile(request):
    """
    Add a person to the database with all of the fields specified.
	Do not update the user's doctor_id in this method, simply leave it null in this method.
    """
    curr_user_id = request.user.id

    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():            
            input = request.POST.copy()
            age = calculate_age(datetime.datetime.strptime(input.get('birth_date'), "%Y-%m-%d").date())
            
            if age < 18:            
                messages.error(request, f'You must be 18 years of age or older!')                    
            else:
                # add_profile(curr_user_id, input)
                assign_doctor(curr_user_id)
                messages.success(request, f'You profile was created successfully.')                    
        else:
            messages.warning(request, f'Please provide correct date format!')

        return redirect('profile')
    else:        
        if Person.objects.filter(user_id=curr_user_id).exists():
            user = Person.objects.filter(user_id=curr_user_id).values()[0]            
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
                'form': PersonForm()
            }
    return render(request, 'matchapp/profile.html', context)

@login_required
def request_organ(request): 
    """
    Add a needed organ into the database. The person who needs
	the organ is given by their id. A person should not be able to submit a request for 2
	of the same organ.
    Do not update the person's doctor_id in this method.
    """   
    curr_user_id = request.user.id
    
    if request.method == 'POST':
        form = OrganRequestForm(request.POST)        
        if form.is_valid:
            input = request.POST.copy()            
            print(input)
            messages.warning(request, f'Please provide a date in the future!')
        else:
            messages.warning(request, f'Please provide a correct date in the future!')
            # date = self.cleaned_data['date']
            # if date < datetime.date.today():
                # raise forms.ValidationError("The date cannot be in the past!")
            # Person = Needs.objects.create(
                #user_id = curr_user_id
                # need_by = input.get('need_by'), 
                # organ = input.get('organ'), 
            # )
            # Person.save()
            #            
    else:        
        if Person.objects.filter(user_id=curr_user_id).exists():
            form = OrganRequestForm()
        else:
            return redirect('profile')
    return render(request, 'matchapp/request.html', {'form': form})

