from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.urlresolvers import reverse

class NewsPost(models.Model):
    author = models.ForeignKey(User, verbose_name='Forfatter')
    title = models.CharField(max_length=200, verbose_name='Titel')
    posted = models.DateTimeField(verbose_name='Dato', default=lambda: datetime.date.today())
    body = models.TextField(verbose_name='Indhold')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        p = self.posted
        return reverse('news', kwargs={'year':p.year, 'month':p.month, 'day':p.day, 'pk':self.pk})

    class Meta:
        verbose_name = 'nyhed'
        verbose_name_plural = verbose_name + 'er'

    def json_of(self):
        return {
            'author': self.author.get_profile().studentnumber,
            'title': self.title,
            'posted': self.posted,
            'body': self.body,
        }
