from django.db import models

# Create your models here.


initial_html = u'''<p>
Fist paragraph... 
</p>

<p>
Second paragraph...
</p>

<h2> Sub-title </h2>
<p>
Evem more text...
</p>'''

class Page(models.Model):
    class Meta:
        ordering = ['title']

    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title
    def __unicode__(self):          # for Python 2 
        return unicode(self.title)

    top_page = models.BooleanField(default=True)
    sort_under = models.ForeignKey('Page', null=True, blank=True, on_delete=models.SET_NULL)
    html = models.TextField(blank=True, default='')
    

class Home(models.Model):
    title = models.CharField(max_length=50, default='WebSiteName')
    def __str__(self):
        return self.title
    def __unicode__(self):          # for Python 2 
        return unicode(self.title)

    html = models.TextField(blank=True, default=initial_html)

