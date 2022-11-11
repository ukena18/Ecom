from pyexpat import model
from django.contrib import admin

# Register your models here.
from .models import Article

#to show in admmin panel
#admin.site.register(Article)

#write as decorater

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    #to show more info on admin panel write list_display
    list_display = ["title","author","created_date"]
    
    #connect the link to the list display object
    list_display_links= ['title','created_date']

    #search filed help forr search
    search_fields = ['title']

    #filter 
    list_filter = ['title','created_date']

    class Meta:
        model=Article