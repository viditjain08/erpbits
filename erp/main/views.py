from django.shortcuts import render
from django.contrib.auth import authenticate, login as authlogin, logout as authlogout
from django.http import HttpResponse, Http404, HttpResponseRedirect
from main.forms import loginform, adminsignupform
from django.contrib.auth.decorators import login_required
from main.models import Erpuser
import re, random
# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    else:
        if request.method == 'POST':
            form = loginform(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                username1 = cd['username']
                password1 = cd['password']
                user = authenticate(username=username1, password=password1)
                if user is not None:
                    authlogin(request, user)
                    return HttpResponseRedirect('/home/')
                else:
                    form.add_error('username', 'Incorrect login credentials')
                    return render(request, 'login.html', {'form': form})
        else:
            #return HttpResponse('D')
            form = loginform()
            return render(request, 'login.html', {'form': form})
        return render(request, 'login.html', {'form': form})
@login_required(login_url='/login/')
def home(request):
    return render(request, 'main.html')

def logout(request):
    authlogout(request)
    return HttpResponseRedirect('/login/')

@login_required(login_url='/login/')
def adminsignup(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = adminsignupform(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                firstname1 = cd['firstname']
                lastname1 = cd['lastname']
                bitsid1 = cd['bitsid']
                temp = re.compile(r'^(201[0-6])[ABH]\dPS(\d{3})P$')
                temp2 = temp.search(bitsid1)
                sem2 = cd['sem']
                if temp2:
                    username1 = '111'+temp2.group(1)+'0'+temp2.group(2)
                    password1 = 'Bits@'+str(random.randint(10000,99999))
                    email1 = 'f'+temp2.group(1)+temp2.group(2)+'@pilani.bits-pilani.ac.in'
                us = Erpuser(first_name = firstname1, last_name = lastname1, username = username1, email=email1, bitsid = bitsid1, semester=sem2)
                us.set_password(password1)
                us.save()
                return render(request, 'signup2.html', {'user': username1, 'pass': password1})
            else:
                return render(request, 'signup.html', {'form': form})
        else:
            form = adminsignupform()
            return render(request, 'signup.html', {'form': form})
    else:
        return render(request, 'main.html')

