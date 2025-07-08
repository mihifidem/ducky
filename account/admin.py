from django.contrib import admin
from .models import UserProfile, UserJobExperience, SoftSkill, UserSoftSkill, Language, UserLanguage, Hobby, UserHobby

admin.site.register(UserProfile)
admin.site.register(UserJobExperience)
admin.site.register(SoftSkill)
admin.site.register(UserSoftSkill)
admin.site.register(Language)
admin.site.register(UserLanguage)
admin.site.register(Hobby)
admin.site.register(UserHobby)


