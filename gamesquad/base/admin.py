from django.contrib import admin

# Register your models here.
from .models import Room, Game, Message, Profile
from accounts.models import User

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Game)
admin.site.register(Message)
admin.site.register(Profile)
