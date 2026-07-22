from django.contrib import admin

from .models import (
    Department,
    CustomUserManager,
    CustomUser,
    Subsidiary,
    Profile,
    AcceptedDomain
)

admin.site.register(Department)
admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Subsidiary)
admin.site.register(AcceptedDomain)
