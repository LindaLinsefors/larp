from django.db import models

# Create your models here.



class BasicModel(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Group(BasicModel):
    group_description = models.TextField(blank=True, default='')


class Character(BasicModel):
    character_description = models.TextField(blank=True, default='')
    comments_from_God = models.TextField(blank=True, default='')

    group = models.ForeignKey(  Group,  null=True, on_delete=models.SET_NULL )
    #group = models.ManyToManyField(  Group,  null=True  )


class Plot_line(BasicModel):
    summery = models.TextField()


class Plot(BasicModel):
    group = models.ForeignKey(  Group,  
                                null=True, 
                                on_delete=models.SET_NULL )

    character = models.ForeignKey(  Character, 
                                    null=True, 
                                    on_delete=models.SET_NULL )

    plot_line = models.ForeignKey(  Plot_line, 
                                    null=True, 
                                    on_delete=models.SET_NULL )

    plot = models.TextField(blank=True, default='')


    def group_plot(self):
        return not self.group
    group_plot.boolean = True

    def del_av_plot_line(self):
        return not self.plot_line
    group_plot.boolean = True
