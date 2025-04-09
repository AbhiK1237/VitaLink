# health_analyzer/apps.py
from django.apps import AppConfig


class HealthAnalyzerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'health_analyzer'
    verbose_name = 'Health Analyzer'