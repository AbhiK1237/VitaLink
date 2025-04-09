# health_analyzer/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class HealthProfile(models.Model):
    """Store basic user health data and personal habits"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='health_profile')
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")
    blood_pressure_systolic = models.IntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    cholesterol_level = models.CharField(max_length=20, null=True, blank=True)
    blood_sugar = models.CharField(max_length=20, null=True, blank=True)
    family_history = models.TextField(null=True, blank=True)
    existing_conditions = models.TextField(null=True, blank=True)
    medications = models.TextField(null=True, blank=True)
    
    # Personal habits
    smoker = models.BooleanField(default=False)
    alcohol_consumption = models.CharField(max_length=50, null=True, blank=True)
    exercise_frequency = models.CharField(max_length=50, null=True, blank=True)
    exercise_intensity = models.CharField(max_length=50, null=True, blank=True)
    diet_type = models.CharField(max_length=50, null=True, blank=True)
    sleep_hours = models.FloatField(null=True, blank=True)
    stress_level = models.CharField(max_length=50, null=True, blank=True)
    water_intake = models.CharField(max_length=50, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Health Profile"


class HealthAnalysis(models.Model):
    """Store results of health analysis from Gemini"""
    health_profile = models.ForeignKey(HealthProfile, on_delete=models.CASCADE, related_name='analyses')
    current_health_assessment = models.TextField()
    potential_health_issues = models.TextField()
    risk_minimization_recommendations = models.TextField()
    full_analysis = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Health Analysis for {self.health_profile.user.username} ({self.created_at.strftime('%Y-%m-%d')})"


class FollowUpConversation(models.Model):
    """Store follow-up conversations related to health analysis"""
    health_analysis = models.ForeignKey(HealthAnalysis, on_delete=models.CASCADE, related_name='conversations')
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Follow-up Q&A for {self.health_analysis.health_profile.user.username}"