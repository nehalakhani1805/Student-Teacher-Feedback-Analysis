from django.contrib import admin
from .models import Skill, SkillQuestion, SkillAnswer
# Register your models here.
admin.site.register(Skill)
admin.site.register(SkillQuestion)
admin.site.register(SkillAnswer)