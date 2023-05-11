from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import user_info_forms
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from google.transliteration import transliterate_text
import google.transliteration
# Create your views here.
def index(request):
    return render(request,'chatapp/index.html')
@login_required
def chat(request,group_name):
    groupobj, created = Grp.objects.get_or_create(name=group_name)
    user=request.user
    username=user.username
    private = request.GET.get('private')
    if private == 'True':
        messages.add_message(
            request,
            messages.SUCCESS,
            'Hey {username}! Share RoomCode with your Friend to Chat'.format(username=username)
        )
    elif created:
        messages.add_message(
            request,
            messages.SUCCESS,
            'Hey {username}! You have created a New Group {group_name}'.format(username=username, group_name=group_name)
        )
    else:
        messages.add_message(
            request,
            messages.SUCCESS,
            'Hey {username}! You have joined {group_name} Group'.format(username=username, group_name=group_name)
        )

    options = {
    'en': 'English',
    'as': 'Assamese',
    'bn': 'Bengali',
    'gu': 'Gujarati',
    'hi': 'Hindi',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'ne': 'Nepali',
    'or': 'Oriya',
    'pa': 'Punjabi',
    'sa': 'Sanskrit',
    'si': 'Sinhala',
    'ta': 'Tamil',
    'te': 'Telugu',
    'be': 'Belarusian',
    'bg': 'Bulgarian',
    'ru': 'Russian',
    'sr': 'Serbian',
    'uk': 'Ukrainian',
    'ar': 'Arabic',
    'fa': 'Persian',
    'ur': 'Urdu',
    'am': 'Amharic',
    'el': 'Greek',
    'he': 'Hebrew',
    'ja': 'Japanese',
    'th': 'Thai',
    'ti': 'Tigrinya'
    }
    chatobjs = Chat.objects.select_related('user').filter(group=groupobj)
    # for chat in  chatobjs:
     # chat.content= transliterate_text(chat.content, lang_code='hi')
        # print(result)
    return render(request, 'chatapp/home.html', {'group_name': group_name,'user_name':user.username,'chats':chatobjs,'privatechat': private,'options': options })

@login_required
def group(request):
    if request.method=="POST":
        grp_name = request.POST['groupname']
        print(grp_name)
        private=False
        redirect_url = '/chat/'+grp_name+'/?private={}'.format(private)
        return redirect(redirect_url)

    return render(request, 'chatapp/forms.html',{"case": 2 })

@login_required
def private(request):
    if request.method=="POST":
        my_uuid="not found"
        friend=request.POST['fname']
        print(friend)
        user=request.user
        if User.objects.filter(username=friend).exists() and friend != user.username:
            frdobj=User.objects.get(username=friend)
            my_uuid = str(100+min(frdobj.id,user.id))+'-'+str(100+max(frdobj.id,user.id))  
            private=True
            redirect_url = '/chat/'+my_uuid+'/?private={}'.format(private)
            return redirect(redirect_url)
        else:
            messages.add_message(
                    request, messages.ERROR, 'ENTER VALID USERNAME ! ')
    return render(request, 'chatapp/forms.html',{"case": 3 })

    # Do something with the UUID
    # ...

# def private(request):
#     myuuid=uuid.uuid4()
#     print(myuuid)

def logins(request):
    if request.method =='POST':
        print(request.POST.get('submit'))
        if request.POST.get('submit')=="Register":
            user_form = user_info_forms(data=request.POST)
            if user_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                messages.add_message(request, messages.SUCCESS,
                                    'REGISTERED SUCCESSFULLY ')
            else:
                messages.add_message(
                    request, messages.ERROR, 'ENTER VALID DETAILS OR USERNAME ALREADY EXIST ! ')
        else:
            username=request.POST.get('username') 
            password=request.POST.get('password') 
            print(username,password)
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.add_message(
                        request, messages.SUCCESS, 'LOGGED IN SUCCESSFULLY! ')
                    return redirect("/")
                else:
                    messages.add_message(
                        request, messages.ERROR, 'ACCOUNT IS NOT ACTIVE! ')
            else:
                messages.add_message(request, messages.ERROR,
                                        'ACCOUNT IS NOT PRESENT! ')
    return render(request, 'chatapp/forms.html', {"case": 1 })

@login_required
def logouts(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS,
                         'LOGGED OUT SUCCESSFULLY. ')
    return redirect("/")

