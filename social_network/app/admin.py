from django.contrib import admin
from .models import FriendRequest, CustomUser

admin.site.register(FriendRequest)
admin.site.register(CustomUser)
