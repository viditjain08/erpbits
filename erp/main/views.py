from django.shortcuts import render
from django.contrib.auth import authenticate, login as authlogin, logout as authlogout
from django.http import HttpResponse, Http404, HttpResponseRedirect
from main.forms import loginform, adminsignupform
from django.contrib.auth.decorators import login_required
from main.models import Erpuser, slot
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

@login_required(login_url='/login/')
def timetable(request):
    if request.method == 'POST':
        id1 = request.POST['id']
        s = slot.objects.get(pk=id1)
        current_user = request.user
        arr = []
        l = []
        l2= []
        flag2 = 0
        for x in current_user.timetable.split('\n'):
            if x != '':
                arr.append(str(x))
        for i in arr:
            s1 = slot.objects.get(pk=int(str(i)[2:]))

            if s.course == s1.course and s.stype == s1.stype:
                flag2 = 1
                break
            
            d1 = len(str(s1.day))
            h1 = len(str(s1.hour))
            for j in range(d1):
                for k in range(h1):
                    l2.append((int(str(s1.day)[j]), int(str(s1.hour)[k])))
                    
            d = len(str(s.day))
            h = len(str(s.hour))
            for j in range(d):
                for k in range(h):
                    l.append((int(str(s.day)[j]), int(str(s.hour)[k])))
        flag = 0
        for (x,y) in l2:
            if (x,y) in l:
                flag = 1
                break
        error = ''
        if s.availableseats < 1:
            error = 'No seats available'
        elif (str(s.pk) == str(i)[2:] for i in arr):
            error = 'You have already selected this'
        elif flag == 1:
            error = "Teleportation isn't yet possible. You can't attend two classes at once"
        elif flag2 == 1:
            error = "Why are you trying to waste your time attending the same class again"
        else:
            s.availableseats = s.availableseats - 1
            s.save()
            d = len(str(s.day))
            h = len(str(s.hour))
            for j in range(d):
                for k in range(h):
                    if current_user.timetable == '':
                        current_user.timetable = str(s.day)[j] + str(s.hour)[k] + str(s.pk)
                    else:
                        current_user.timetable = current_user.timetable + '\n' + str(s.day)[j]+str(s.hour)[k]+str(s.pk)
            current_user.save()
        l3 = []
        l4 = []
        for x in current_user.timetable.split('\n'):
            if x:
                l3.append(str(x))
                l4.append(int(str(x)[2:]))
        l3.sort()
        timetable = []
        for i in range(6):
            for j in range(1,10):
                flag = 0
                for num in l3:
                    if num[0] == str(i) and num[1] == str(j):
                        flag = 1
                        break
                if flag == 1:
                    timetable.append(slot.objects.get(pk=num[2:]))
                else:
                    timetable.append('')
        l4 = set(l4)
        l4 = list(l4)
        s1 = slot.objects.all()
        return render(request, 'timetable.html', {'errors': error, 'slots': s1, 'timetab': timetable, 'timeid': l4})
    else:
        l3 = []
        l4 = []
        for x in request.user.timetable.split('\n'):
            if x:
                l3.append(str(x))
                l4.append(int(str(x)[2:]))
        l3.sort()
        timetable = []
        for i in range(6):
            for j in range(1,10):
                flag = 0
                for num in l3:
                    if num[0] == str(i) and num[1] == str(j):
                        flag = 1
                        break
                if flag == 1:
                    timetable.append(slot.objects.get(pk=num[2:]))
                else:
                    timetable.append('')

        l4 = set(l4)
        l4 = list(l4)
        s = slot.objects.all()
        return render(request, 'timetable.html', {'slots': s, 'timetab': timetable, 'timeid': l4})
    


