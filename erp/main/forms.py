from django import forms
import re
from main.models import Erpuser
class loginform(forms.Form):
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(max_length=20, required=True, widget=forms.PasswordInput)

class adminsignupform(forms.Form):
    firstname= forms.CharField(max_length=20, required=True)
    lastname = forms.CharField(max_length=20)
    bitsid = forms.CharField(max_length=12, required=True)
    sem = forms.IntegerField(required=True)
    def clean_bitsid(self):
        bitsid2 = self.cleaned_data['bitsid']
        temp = re.compile(r'^201([0-6])([ABH])(\d)PS(\d{3})P$')
        flag = temp.search(bitsid2)
        if flag is None:
            raise forms.ValidationError("Invalid BitsID")
        if Erpuser.objects.filter(bitsid=bitsid2).exists():
            raise forms.ValidationError(u'BITSID "%s" is already in use.' % bitsid2)
        return bitsid2
    def clean_sem(self):
       sem2 = self.cleaned_data['sem']
       if sem2 < 1 or sem2 > 10:
           raise forms.ValidationError("Invalid Semester Number")
       return sem2


