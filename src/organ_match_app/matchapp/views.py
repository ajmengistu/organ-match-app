from django.shortcuts import render

def home(request):
    return render(request, 'matchapp/home.html', {'title': 'Home'})

def about(request):
    return render(request, 'matchapp/about.html', {'title': 'About'})