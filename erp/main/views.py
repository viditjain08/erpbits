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
        #If user logged in, redirect to home page
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = loginform(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                username1 = cd['username']
                password1 = cd['password']
                user = authenticate(username=username1, password=password1)
                #Login credentials verification
                if user is not None:
                    authlogin(request, user)
                    #if next page is mentioned
                    url = re.compile(r'next=/(\w+)')
                    temp = url.search(request.get_full_path())
                    if temp is None:
                        return HttpResponseRedirect('/') 
                    else:
                        return HttpResponseRedirect('/'+temp.group(1)+'/')
                else:
                    #error if username/password incorrect
                    form.add_error('username', 'Incorrect login credentials')
                    return render(request, 'login.html', {'form': form})
        else:
            form = loginform()
            url = re.compile(r'next=/(\w+)')
            temp = url.search(request.get_full_path())

            if temp is None:
                status = ''
            elif temp.group(1) == 'pr' or temp.group(1) == 'signup':
                status = 'Only admin can access this'
            else:
                status = 'You need to sign in to view that page'
            return render(request, 'login.html', {'form': form, 'status': status})
        return render(request, 'login.html', {'form': form})

#login required to access home page
@login_required(login_url='/login/')
def home(request):
    return render(request, 'main.html')

def logout(request):
    authlogout(request)
    return HttpResponseRedirect('/login/')

#only admin can create student ids
@login_required(login_url='/login/')
def adminsignup(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = adminsignupform(request.POST)
            if form.is_valid():
                #username and password generation
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
        return HttpResponseRedirect('/')

#random numbers allotted to students which denotes hour allotted to student for time table registration
@login_required(login_url='/login/')
def pr(request):
    #only admin can generate PR numbers for student
    if request.user.is_superuser:
        if request.method == 'POST':
            student = {}
            #admins are excluded from PR allotment
            u = Erpuser.objects.filter(is_superuser='False')
            c = Erpuser.objects.filter(is_superuser='False').count()
            for users in u:
                users.pr = 0
                users.save()
            for users in u:
                d = 0
                while d == 0:
                    #No duplicate PRs allotted
                    if Erpuser.objects.filter(pr=users.pr).count() is not 0:
                        users.pr = random.randint(1, c)
                    else:
                        d = 1
                users.save()
                student[users.bitsid] = users.pr
            return HttpResponseRedirect('/prlist/')
        else:
            return render(request, 'pr.html')

    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def prlist(request):
    u = Erpuser.objects.filter(is_superuser='False')
    student = {}
    for users in u:
        student[users.bitsid] = users.pr
    return render(request, 'pr2.html', {'student': student})
