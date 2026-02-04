from django.contrib import admin

# Register your models here.

from .models import Judgment, JudgmentChunk

admin.site.register(Judgment)
admin.site.register(JudgmentChunk)