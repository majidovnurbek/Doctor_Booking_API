from django.contrib import admin

from .models import User,Doctor,News,Booking

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(News)

@admin.register(Booking)
class PostAdmin(admin.ModelAdmin):
    list_display = ('doctor','status','date_time','created_at')



