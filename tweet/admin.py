from django.contrib import admin
from .models import Tweet, Message

# Register your models here.
admin.site.register(Tweet)

# <profile>

from django.contrib import admin
from .models import Profile, Team, TeamMember

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'department', 'bio')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember)
admin.site.register(Message)

