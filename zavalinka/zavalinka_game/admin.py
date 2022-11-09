from django.contrib import admin

from .models import Profile, UserInZavalinkaGame, ZavalinkaGame, ZavalinkaWord

admin.site.register(Profile)
admin.site.register(UserInZavalinkaGame)
admin.site.register(ZavalinkaGame)
admin.site.register(ZavalinkaWord)