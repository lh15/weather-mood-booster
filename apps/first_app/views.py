from django.shortcuts import render, HttpResponse, redirect
import requests
import json
import schedule
import time
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
import re
import datetime
import pytz
from .models import User, Friend

# Create your views here.


def get_quotes(request):
    categories = ["inspire", "management", "life", "funny", "love"]
    for category in categories:
        url = 'http://quotes.rest/qod.json?category=' + category
        r = requests.get(url)
        print "api called"
        quote = r.json()
        # print quote['contents']['quotes'][0]['quote']
        if category not in request.session.keys():
            request.session[category] = quote
            print request.session[category]
        else:
            request.session[category] = quote
            print request.session[category]


def get_weather(request):
    if request.method == "POST" and request.is_ajax():
        print "reached getweather"
        lat = request.POST['lat']
        lon = request.POST['lon']
        url = "http://api.openweathermap.org/data/2.5/weather?lat=" + \
            lat + "&lon=" + lon + "&APPID=91d2fecd81cd087af9adf3d373fd0276"
        r = requests.get(url)
        print "api called"
        weather = r.json()
        kelvin = weather['main']['temp']
        print kelvin
        conditions = weather['weather'][0]['main']
        print conditions
        print request.session['funny']
        if 'weather' not in request.session.keys():
            request.session['weather'] = weather
            print request.session['weather']
        else:
            request.session['weather'] = weather
        context = {
                'funny': request.session['funny'],
                'life': request.session['life'],
                'management': request.session['management'],
                'inspire': request.session['inspire'],
                'city': request.session['weather']['name'],
                'fahrenheit': int(round((kelvin*9/5.0)-459.67)),
                'celcius': int(round(kelvin-273.15)),
                'conditions': conditions,
            }

        print weather['name']
        
        return render(request, "first_app/weather.html", context)

def get_friend_weather(request):
    current_user = User.objects.get(email=request.session['logged_in'])
    count = 0
    friends_list = []
    friends = Friend.objects.filter(user = current_user)
    print "reached getweather"
    for friend in friends:
        lat = str(friend.latitude)
        lon = str(friend.longitude)
        url = "http://api.openweathermap.org/data/2.5/weather?lat=" + \
        lat + "&lon=" + lon + "&APPID=91d2fecd81cd087af9adf3d373fd0276"
        r = requests.get(url)
        print "api called"
        weather = r.json()
        kelvin = weather['main']['temp']
        print kelvin
        conditions = weather['weather'][0]['main']
        print conditions
        conditions = weather['weather'][0]['main']
        friend_dict = {
        'friend': friend,
        'weather': weather,
        'fahrenheit': int(round((kelvin*9/5.0)-459.67)),
        'conditions':conditions  
        }
        friends_list.append(friend_dict)

    print friends_list

    context = {
    'friends_list': friends_list,
    }
    return render(request, "first_app/friends_weather.html", context)
            


def process_friend(request, id):
    if request.method == "POST":
        print "reached process_friend"
        user = User.objects.get(id=id)
        new_friend= Friend.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], latitude = request.POST['latitude'],  longitude = request.POST['longitude'], user = user)
        print new_friend
    return redirect('/')


def index(request):
    if 'logged_in' not in request.session.keys():
        request.session['logged_in'] = False
        print request.session['logged_in']
        return render(request, "first_app/register.html")
    if request.session['logged_in'] == False:
        return render(request, "first_app/register.html")
        print request.session['logged_in']
    else:
        print request.session['logged_in']
        return redirect('/display')


def process_registration(request):
    if request.method == "POST":
        error = False
        # for now i am passing in the entire request object for the sake of the django messages(will fix), and i am using session to repopulate the fields,
        user = User.objects.register(request.POST, request.session, request)
        error = False
        if user:
            get_quotes(request)
            return redirect('/display')
        return redirect('/')
    return redirect('/')


def process_login(request):
    if request.method == "POST":
        error = False
        # for now i am passing in the entire request object for the sake of the django messages(will fix), and i am using session to repopulate the fields
        user = User.objects.login(request.POST, request.session, request)
        if user:
            get_quotes(request)
            return redirect('/display')
        else:
            return redirect('/login')
        return redirect('/login')


def login(request):
    return render(request, "first_app/login.html")


def log_out(request):
    request.session.pop('logged_in')
    return redirect('/login')


def display(request):
    try:
        if request.session['logged_in'] == False:
            return redirect('/')
            print request.session['logged_in']
    except:
        request.session['logged_in'] == False

    else:
        current_user = User.objects.get(email=request.session['logged_in'])
        context = {
            "current_user": current_user,
        }
        return render(request, 'first_app/display.html', context)
