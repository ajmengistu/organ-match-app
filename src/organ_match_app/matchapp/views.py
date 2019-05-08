from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from  .forms import UserRegistrationForm

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
            username = form.clean_date.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'matchapp/register.html', {'form' : form})