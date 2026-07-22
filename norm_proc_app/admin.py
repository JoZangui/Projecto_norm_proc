# norm_proc_app/admin.py
from django.contrib import admin
from .models import Norms, Procedures

admin.site.register(Norms)
admin.site.register(Procedures)
