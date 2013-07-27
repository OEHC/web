# vim: set fileencoding=utf8:
from django.db import models

from ..tutor.models import TutorProfile

class ShirtPreference(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(TutorProfile)
    choice1 = models.CharField(max_length=60)
    choice2 = models.CharField(max_length=60)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def json_of(self):
        return {
            'tutor': self.profile.studentnumber,
            'choices': [self.choice1, self.choice2],
            'created': created,
            'updated': updated,
        }

class ShirtOption(models.Model):
    id = models.AutoField(primary_key=True)
    choice = models.CharField(max_length=60)
    position = models.IntegerField()

    class Meta:
        ordering = ('position',)

    def __unicode__(self):
        return self.choice

    def json_of(self):
        return {
            'choice': self.choice,
            'position': self.position,
        }
