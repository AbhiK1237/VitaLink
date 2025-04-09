# health_analyzer/admin.py
from django.contrib import admin
from .models import HealthProfile, HealthAnalysis, FollowUpConversation


@admin.register(HealthProfile)
class HealthProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('gender', 'smoker', 'alcohol_consumption', 'exercise_frequency')
    date_hierarchy = 'created_at'


@admin.register(HealthAnalysis)
class HealthAnalysisAdmin(admin.ModelAdmin):
    list_display = ('health_profile', 'created_at')
    search_fields = ('health_profile__user__username', 'health_profile__user__email')
    date_hierarchy = 'created_at'


@admin.register(FollowUpConversation)
class FollowUpConversationAdmin(admin.ModelAdmin):
    list_display = ('health_analysis', 'question', 'created_at')
    search_fields = ('question', 'answer', 'health_analysis__health_profile__user__username')
    date_hierarchy = 'created_at'