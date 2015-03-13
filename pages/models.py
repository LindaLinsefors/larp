from django.db import models

# Create your models here.

class Page(models.Model):
    class Meta:
        ordering = ['title']

    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title
    def __unicode__(self):          # for Python 2 
        return unicode(self.title)

    top_page = models.BooleanField(default=True)
    sort_under = models.ForeignKey('Page', null=True)
    html = models.TextField(blank=True, default='')
    


