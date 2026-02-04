from django.contrib import admin
from .models import DraftType, Draft, DraftFact

admin.site.register(DraftType)
admin.site.register(Draft)
admin.site.register(DraftFact)