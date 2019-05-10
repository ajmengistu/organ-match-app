from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from  .forms import UserRegistrationForm, OrganRequestForm, PersonForm, OrganOfferForm
from .models import Person, Doctors, Needs, Available
from django.contrib.auth.models import User
import datetime


def home(request):
    curr_user_id = request.user.id
    context = {
        'title': 'Home',
        'requests': get_requests(curr_user_id),
        'offers': get_offers(curr_user_id),
    }
    return render(request, 'matchapp/home.html', context)

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
    person = Person.objects.create(
                    user_id = curr_user_id,
                    first_name = input.get('first_name'),
                    last_name = input.get('last_name'),
                    birth_date = input.get('birth_date'),
                    blood_type = input.get('blood_type'),
                )
    person.save()
    print("-------Added user profile information---------")

def assign_doctor(uid):
    """
    Assign a doctor to a person as they sign up for the first time.
	A doctor is assigned to a person by updating the person's doctor_id field with
	the doctor with the fewest patients. The number of patients is defined as the number of
	people assigned to that doctor through their doctor_id field. To break ties, choose
	the doctor with the smallest id.
    """
    q = ("WITH temp AS ( "
    + "(SELECT matchapp_doctors.id, 0 patients FROM matchapp_doctors "
    + "LEFT OUTER JOIN matchapp_person ON matchapp_person.doctor_id = matchapp_doctors.id "
    + "WHERE matchapp_person.user_id IS NULL ORDER BY matchapp_doctors.id) "
    + "UNION (SELECT matchapp_doctors.id, COUNT(*) patients FROM matchapp_doctors "
    + "JOIN matchapp_person ON matchapp_person.doctor_id = matchapp_doctors.id "
    + "GROUP BY matchapp_doctors.id ORDER BY matchapp_doctors.id) ) "
    + "SELECT * FROM temp ORDER BY patients, id")

    # Must include primary key in the query set
    query_set = Doctors.objects.raw(q)
    
    did = -1
    for doctor in query_set:
        did = doctor.id
        break
    print(did)
    
    # Assign a doctor to uid
    person = Person.objects.get(user_id=uid)
    person.doctor_id = did
    person.save()
    print("--------Assigned a doctor to uid------------")
    
@login_required
def profile(request):    
    """
    Add a person to the database with all of the fields specified.
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
                add_person(curr_user_id, input)
                assign_doctor(curr_user_id)
                messages.success(request, f'Your information was submitted successfully.')                    
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
                'doctor_id': Doctors.objects.get(id=user.get('doctor_id')).name,
                'profile_id': user.get('id'),
                'requests': get_requests(curr_user_id),
                'offers': get_offers(curr_user_id),
            }
        else:            
            context = {
                'form_exists': True,
                'form': PersonForm(),
                'requests': get_requests(curr_user_id),
                'offers': get_offers(curr_user_id), 
            }
    return render(request, 'matchapp/profile.html', context)

def add_requested_organ(request, curr_user_id, org, need_by):
    try:
        needs = Needs.objects.create(
            user_id = curr_user_id,
            organ = org,
            date_by = need_by
        )
        needs.save()
        print("------------Added requested organ-------------")
        return True
    except Exception as e:
        print(type(e))
        return False

def date_in_future(date):    
    return datetime.datetime.strptime(date, "%Y-%m-%d").date() > datetime.date.today()

def get_offers(curr_user_id):
    return Available.objects.filter(user_id=curr_user_id)
def get_requests(curr_user_id):
    return Needs.objects.filter(user_id=curr_user_id)
@login_required
def request_organ(request): 
    """
    Add a needed organ into the database. The person who needs
	the organ is given by their id. A person should not be able to submit a request for 2
	of the same organ.    
    """   
    curr_user_id = request.user.id
    
    if request.method == 'POST':
        form = OrganRequestForm(request.POST)                
        if form.is_valid():
            input = request.POST.copy()
            organ = input.get('organ')
            need_by = input.get('need_by')

            if date_in_future(need_by):
                if add_requested_organ(request, curr_user_id, organ, need_by):
                    messages.success(request, f'Your request has been submitted successfully!')    
                else:
                    messages.error(request, f'You have already requested for this organ [' + organ  +']!')
            else:
                messages.warning(request, f'Please provide a correct date in the future!')    
        else:            
            messages.warning(request, f'Please provide a correct date in the future!')
            redirect('matchapp-request')
    else:        
        if not Person.objects.filter(user_id=curr_user_id).exists():
            return redirect('profile')

    context = {
                'form': OrganRequestForm(),
                'requests': get_requests(curr_user_id),
                'offers': get_offers(curr_user_id),
            }
    return render(request, 'matchapp/request.html', context)

def add_offer_organ(id, organ):
    try:
        available = Available.objects.create(
            user_id = id,
            organ = organ,            
        )
        available.save()
        print("------------Added offered organ-------------")
        return True
    except Exception as e:
        print(type(e))
        return False

@login_required
def offer_organ(request):
    curr_user_id = request.user.id

    if request.method == 'POST':
        form = OrganOfferForm(request.POST)
        if form.is_valid():
            input = request.POST.copy()
            if add_offer_organ(curr_user_id, input.get('organ')):
                 messages.success(request, f'Your offer has been submitted successfully!')    
            else:
                 messages.error(request, f'You have already offered this organ [' + input.get('organ')  +']!')
            

    context = {
        'form': OrganOfferForm(),
        'requests' : get_requests(curr_user_id),
        'offers' : get_offers(curr_user_id),
    }

    return render(request, 'matchapp/offer.html', context)