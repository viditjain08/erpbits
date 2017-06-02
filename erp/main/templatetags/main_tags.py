import calendar
import datetime
from django import template

register = template.Library()

@register.filter
def day_name(day_number):
    l = len(str(day_number))
    s = str(day_number)
    l1 = []
    for i in range(l):
        l1.append(calendar.day_name[int(s[i])])
    return ' '.join(l1)
@register.filter
def hour_name(v):
    c = len(str(v))
    if v==0:
        return ''
    else:
        return (str(datetime.timedelta(hours=int(str(v)[0])+7))+'-'+str(datetime.timedelta(hours=int(str(v)[0])+6+c, minutes=50)))
@register.filter
def split(value):
    if value < 5:
        return (str(value+7)+':00am -'+str(value+7)+':50am')
    elif value == 5:
        return (str(value+7)+':00pm -'+str(value+7)+':50pm')
    elif value<10:
        return (str(value-5)+':00pm -'+str(value-5)+':50pm')
    else:
        return value/10

@register.filter
def li(value):
    l = len(str(value))
    l1 = []
    for i in range(l):
       l1.append(str(value)[i])
    return l1


@register.filter
def lookup(d, key1):
    s = d[(int(str(key1)[0])*9)+int(str(key1)[1])-1]
    return s

@register.filter
def addstr(a, b):
    return str(a)+str(b)






