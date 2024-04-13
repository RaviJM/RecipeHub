from django.contrib import admin

# Register your models here.

from .models import Recipe, Topic, Message

admin.site.register(Recipe)
admin.site.register(Topic)
admin.site.register(Message)
