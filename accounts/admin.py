from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import User, Agreement

admin.site.register(User)
admin.site.site_header = "VOLT"

admin.site.register(Agreement, TranslatableAdmin)
