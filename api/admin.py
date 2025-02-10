from django.contrib import admin

from .models import User,Doctor,News,Date

# admin.site.register(User)
# admin.site.register(Doctor)
# admin.site.register(News)

@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    list_display = ('user','date','time','status')
    search_fields = ('status',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email','password')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user','location','experience')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title','created_at','img')

    def img(self, obj):
        return format_html(
            f'''<a href="{obj.img.url}" target="_blank">
                          <img src="{obj.img.url}" alt="img" width="150" height="100"
                               style="object-fit: cover;"/>
                      </a>'''
        )




