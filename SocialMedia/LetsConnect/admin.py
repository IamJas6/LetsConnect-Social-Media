from django.contrib import admin
from . models import *
from . models import CustomUser

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CustomUser)