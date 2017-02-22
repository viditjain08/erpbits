import calendar
import datetime
from django import template

register = template.Library()

@register.filter
def day_name(day_number):
    return calendar.day_name[day_number]

@register.filter
def hour_name(v):
    c = len(str(v))
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
