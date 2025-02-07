from django.contrib import admin

from .models import User,Doctor,News,Date

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(News)

@admin.register(Date)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user','date','time','status')



