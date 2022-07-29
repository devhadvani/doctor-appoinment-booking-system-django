import time
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Custom,Topic,Blog,Book
from .forms import CustomCreationForm,BlogForm, TopicForm
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout

import datetime
from datetime import timedelta
import pytz
from apiclient.discovery import build
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

import sys

start_time =0
end_time=0
  
scopes = ['https://www.googleapis.com/auth/calendar']

credentials = pickle.load(open('H:\\django projects\\token.pkl', 'rb'))
def bookform(request,pk):
    form = Custom.objects.get(id=pk)
    if request.method == 'POST':
        form = Custom.objects.get(id=pk)
        req = request.POST['req']
        start = request.POST['start']
        time = request.POST['time']
        email = request.POST['email']
        starts = start +' '+ time +':' '00'
    
        start_time = datetime.datetime.strptime(starts,"%Y-%m-%d %H:%M:%S")
        end_time  = start_time + timedelta(minutes=45)
        context = { 'req':req,'start':start,'time':time,'start_time':start_time, 'end_time':end_time,'email':email,'form':form}
        return  render(request, 'confirm.html',context)
        

    
    return render(request,'bookform.html',{'form':form})

def confirm(request):
    service = build("calendar", "v3", credentials=credentials) 
    if request.method == 'POST':
        req = request.POST['required']
        start = request.POST['starts']
        time = request.POST['time']
        email = request.POST['email']
        start = start +' '+ time +':' '00' 
        start_time = datetime.datetime.strptime(start,"%Y-%m-%d %H:%M:%S")
        end_time  = start_time + timedelta(minutes=45)
        timezone = 'Asia/Kolkata'
        print("Gsfgfd",start_time.isoformat(),'vdfdf',end_time.isoformat())
        print("dsdv",req)
        print("Gfdg",email),
        event = (
        service.events()
        .insert(
            calendarId="primary",
            body={
                "summary": req,
               
                "start": {"dateTime": start_time.isoformat(),
                'timeZone': timezone,
               
                
                },
                "end": {
                    "dateTime": end_time.isoformat(),
                    'timeZone': timezone,
                },
                "attendees":[{"email":email}
                
                ]
            },
        )
        .execute()
         )
        
        return redirect('home')
    
    return render(request,'confirm.html')

def viewevent(request):
    service = build("calendar", "v3", credentials=credentials)
    now = datetime.datetime.utcnow().isoformat() + 'Z' 
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return

        # Prints the start and name of the next 10 events
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        email = event['attendees'][0:]
        print(start,email)

    return render(request,'viewevent.html',{'form':start})

def doctor(request):
    form = Custom.objects.filter(roles='is_doctor')
    print(form)

    return render(request,'doctor.html',{'form':form})

def home(request):
    q = request.GET.get('q') 
    if request.GET.get('q') != None:
        blog = Blog.objects.filter(
            Q( topic__name__icontains=q) &
            Q(draft = False) ) 
        
    else:
        blog = Blog.objects.filter(draft=False)


        
    topic = Topic.objects.all()
    drafts = Blog.objects.filter(draft=True)
    
    context = {'blog':blog,'topics':topic,'list':q,"draft":drafts}
    return render(request,'home.html',context)

def about(request):
        return render(request,'about.html')

def register(request):
    form = CustomCreationForm()
    if request.method == "POST":

        form = CustomCreationForm(request.POST, request.FILES)
        if form.is_valid():

            user = form.save(commit  = False)
            user.username = user.username.lower()
            user.save()
            print(user)
            return redirect('log')
  
    return render(request,"register.html",{'form':form})


def log(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print('Invalid Username or Password')
            return redirect('log')



    else:
        return render(request, 'login.html')
    return render(request,'login.html')

def logout_form(request):
    logout(request)
    return redirect('home')

def create_blog(request):
    form = BlogForm()
    form = BlogForm(request.POST,request.FILES)
    if form.is_valid():

            name = form.save(commit  = False)
            name.save()
            print(name)
            return redirect('create_blog')
    
    return render(request,'blogform.html',{'form':form})

def create_topic(request):
    form = TopicForm()
    if request.method == "POST":

        form = TopicForm(request.POST)
        if form.is_valid():

            name = form.save(commit  = False)
            name.save()
            print(name)
            return redirect('create_topic')

    
    return render(request,'topicform.html',{'form':form})

    
def blog(request,pk):
    blogs = Blog.objects.get(id=pk)
    
    context = { 'blogs':blogs}
    return render(request,'blog.html',context)
