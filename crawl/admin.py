from django.contrib import admin
from childsearch.crawl.models import *

class Crawl_URLAdmin(admin.ModelAdmin):  
    list_display = ('name','url','stype',)  
    ordering = ('-id',)  
    fields = ('url','name','stype',)  

admin.site.register(Crawl_URL, Crawl_URLAdmin) 
