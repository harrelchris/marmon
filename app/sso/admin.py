from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Character


class CharacterInline(admin.StackedInline):
    model = Character
    can_delete = False
    verbose_name_plural = "characters"


class UserAdmin(BaseUserAdmin):
    inlines = (CharacterInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
