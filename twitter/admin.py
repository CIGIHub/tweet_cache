from django.contrib import admin
from twitter.models import User, Tweet

class UserAdmin(admin.ModelAdmin):
    list_display = ('screen_name', 'current_followers')

admin.site.register(User, UserAdmin)
admin.site.register(Tweet)
