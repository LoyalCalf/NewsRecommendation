from django.contrib import admin
from .models import user_tag_score, user_behavior, user_profile, user_recommendation
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(user_tag_score)
admin.site.register(user_behavior)
admin.site.register(user_recommendation)
admin.site.register(user_profile)
