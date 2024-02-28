import string
import random
import requests

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Register

# Create your views here.
def hello1(request):
    return HttpResponse("<centre>Welcome to Home page</centre>")

def newhomepage(request):
    return render(request, 'newhomepage.html')

def travelpackage(request):
    return render(request, 'travelpackage.html')

def print1(request):
    return render(request,'print_to_console.html')


def print_to_console(request):
    if request.method == "POST":
        user_input = request.POST['user_input']
        print(f'user input:{user_input}')
    a1 = {'user_input': user_input}
    return render(request, 'print_to_console.html',a1)


def randomcall(request):
    return render(request,'randomotpgenerator.html')


def randomlogic(request):
    if request.method == "POST":
        user_input = request.POST['user_input']
        print(f'user input:{user_input}')
        a2 = int(user_input)
        ran1 = ''.join(random.sample(string.digits, k=a2))
    a1 = {'ran1': ran1}
    return render(request, 'randomotpgenerator.html',a1)

def getdate1(request):
    return render(request,'get_date.html')

import datetime
from django.shortcuts import render
from .forms import *
def get_date(request):
    if request.method == 'POST':
        form = IntegerDateForm(request.POST)
        if form.is_valid():
            integer_value = form.cleaned_data['integer_value']
            date_value = form.cleaned_data['date_value']
            updated_date = date_value + datetime.timedelta(days=integer_value)
            return render(request, 'get_date.html',{'updated_date':updated_date})
        else:
            form = IntegerDateForm()
        return render(request, 'get_date.html',{'form':form})


def register1(request):
    return render(request,'myregisterpage.html')




def registerloginfunction(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        phonenumber=request.POST.get('phonenumber')

        if Register.objects.filter(email=email).exists():
            return HttpResponse("Email already registered .choose a different email .")
        Register.objects.create(name=name,email=email,password=password,phonenumber=phonenumber)
        return redirect('newhomepage')
    return render(request,'myregisterpage.html')

import matplotlib.pyplot as plt
import numpy as np

def pie_chart(request):
    if request.method == 'POST':
        form = PieChartForm(request.POST)
        if form.is_valid():
            # Process user input
            y_values = [int(val) for val in form.cleaned_data['y_values'].split(',')]
            labels = [label.strip() for label in form.cleaned_data['labels'].split(',')]

            # Create pie chart
            plt.pie(y_values, labels=labels, startangle=90)
            plt.savefig('static/images/pie_chart.png')  # Save the chart image
            img1={'chart_image': '/static/images/pie_chart.png'}
            return render(request, 'piechart.html', img1)
    else:
        form = PieChartForm()
    return render(request, 'piechart.html', {'form': form})
class PieChartForm(forms.Form):
    y_values = forms.CharField(label='Y Values', help_text='Enter comma-separated values')
    labels = forms.CharField(label='Labels', help_text='Enter comma-separated labels')

def weatherpage(request):
    return render(request,'weatherpage.html')


def weatherlogic(request):
    if request.method == 'POST':
        place = request.POST['place']
        API_KEY = 'b3a0bbf01acef240eea73ae0a16512d3'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={place}&appid={API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            temperature1= round(temperature - 273.15,2)
            return render(request, 'weatherpage.html',
                          {'city': str.upper(place), 'temperature': temperature1, 'humidity': humidity})
        else:
            error_message = 'City not found. Please try again.'
            return render(request, 'weatherpage.html', {'error_message': error_message})

from django.shortcuts import render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login(request):
    return render(request,'login.html')
def signup(request):
    return render(request,'signup.html')
def login1(request):
    if request.method=='POST':
        username=request.POST['username']
        pass1=request.POST['password']
        user=auth.authenticate(username=username,password=pass1)
        if user is not None:
            auth.login(request,user)
            return render(request,'newhomepage.html')
        else:
            messages.info(request,'Invalid Credentials')
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def signup1(request):
 if request.method=="POST":
    username=request.POST['username']
    pass1=request.POST['password']
    pass2=request.POST['password1']
    if pass1==pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'OOPS! Usename already taken')
                return render(request,'signup.html')
            else:
                user=User.objects.create_user(username=username,password=pass1)
                user.save()
                messages.info(request,'Account created successfully!!')
                return render(request,'login.html')
    else:
            messages.info(request,'Password do not match')
            return render(request,'signup.html')
def logout(request):
    auth.logout(request)
    return render (request,'newhomepage.html')

def feedbackform(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        feedback = request.POST.get('feedback')
        rating = request.POST.get('rating')

        Feedback.objects.create(first_name=first_name, last_name=last_name, email=email,  phonenumber=phonenumber,feedback=feedback,rating = rating)
        return redirect('newhomepage')
    send_mail(
        'Thank You for Contacting Deepaks Travel Tourism and Managment '
    tosend,
        '2200090256@csitgmail.com'
    'Email'
    [email],
    fail_silently = False
    )

    return render(request, 'feedback.html')

from django.shortcuts import render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required