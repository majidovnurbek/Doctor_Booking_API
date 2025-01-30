from django.contrib import admin

from .models import User,Doctor,News

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(News)

