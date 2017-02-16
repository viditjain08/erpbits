from django.db import models
from django.contrib.auth.models import AbstractUser

class slot(models.Model):

    course = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30)
    teacher = models.CharField(max_length=50)
    day = models.IntegerField()
    hour = models.IntegerField()
    totalseats = models.IntegerField()
    availableseats = models.IntegerField(default=0)
    stype = models.CharField(max_length=20)
    room = models.IntegerField()
    def save(self):
        if self.pk is None:
            self.availableseats = self.totalseats
        super(slot, self).save()
    def __str__(self):
        return u'%s %s' % (self.course, self.name)

class Erpuser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
