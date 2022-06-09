from django.shortcuts import render

# Create your views here.


def home(request):
    return render (request, 'index.html')

def login(request):
    pass

def register(request):
    
    return render (request, 'register.html')