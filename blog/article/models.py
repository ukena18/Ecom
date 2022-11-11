from statistics import mode
from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Article(models.Model):
    #point to usr table
    author=models.ForeignKey('auth.User',on_delete=models.CASCADE,verbose_name='АВТОР')
    title = models.CharField(max_length=50)
    content =  RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)
    article_image = models.FileField(blank=True,null=True,verbose_name='Upload_image')

    #in admin ponel chage the name to title
    def __str__(self):
        return self.title;