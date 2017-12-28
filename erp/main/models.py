from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import is_password_usable

class slot(models.Model):

    course = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    teacher = models.CharField(max_length=150)
    day = models.CharField(max_length=7)
    hour = models.CharField(max_length=30)
    totalseats = models.IntegerField()
    availableseats = models.IntegerField(default=0)
    stype = models.CharField(max_length=20)	# type of class i.e project, tutorial, etc.
    room = models.IntegerField()
    sec = models.IntegerField()			# section number
    def save(self):
        if self.pk is None:
            self.availableseats = self.totalseats
        super(slot, self).save()
    def __str__(self):
        return u'%s %s %s' % (self.course, self.name, self.teacher)

class Erpuser(AbstractUser):
    semester = models.IntegerField(default=1)
    bitsid = models.CharField(max_length=12, unique=True)
    cgpa = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=2)
    timetable = models.TextField(default='', blank=True)
    pr = models.IntegerField(default=0)
    availablecourses = models.ManyToManyField(slot)
    def save(self, **kwargs):
        password1 = self.password
        if is_password_usable(password1) is False:
            self.set_password(password1)
        super(Erpuser, self).save(**kwargs)
    class Meta:
        permissions = (
            ("can_changett_pr", "Can Change Timetable PR"),
            ("can_changett_final", "Can Change Timetable Final"),

        )

