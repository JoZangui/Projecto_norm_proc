from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import (
    Department,
    CustomUser,
    Subsidiary,
    Profile,
    AcceptedDomain
)


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("email", "username", "first_name", "last_name", "is_active", "is_staff")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As passwords não coincidem.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Password")

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ("email", "username", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "is_superuser", "groups")
    ordering = ("email",)
    search_fields = ("email", "username", "first_name", "last_name")
    filter_horizontal = ("groups", "user_permissions")
    fieldsets = (
        (None, {"fields": ("email", "password")} ),
        ("Informação pessoal", {"fields": ("username", "first_name", "last_name")} ),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")} ),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "first_name", "last_name", "password1", "password2", "is_active", "is_staff"),
        }),
    )

admin.site.register(Department)
admin.site.register(Profile)
admin.site.register(Subsidiary)
admin.site.register(AcceptedDomain)
