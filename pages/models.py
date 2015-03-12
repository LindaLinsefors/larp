from django.db import models

# Create your models here.

class Page(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    def __unicode__(self):          # for Python 2 
        return unicode(self.name)

    text = models.TextField(blank=True, default='')
    
    up = models.ForeignKey('Page', null=True,)

