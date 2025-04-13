from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


# Create your views here.
def hello(request):
    text = '<h1>Welcome to my app!</h1>Nice to see you here'
    return HttpResponse(text)

def homepage(request):
    return render(request, 'homepage.html', {'name': 'Zak'})

def formjs(request):
    return render(request, 'formjs.html', {})

def bookings(request):
    return render(request, 'bookings.html', {})

def aircraft(request):
    return render(request, 'aircraft.html', {})



#TODO add more views for the other pages