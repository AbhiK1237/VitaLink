# health_analyzer/forms.py
from django import forms
from .models import HealthProfile


class HealthProfileForm(forms.ModelForm):
    """Form for collecting basic health data and personal habits"""
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say')
    ]
    
    ALCOHOL_CHOICES = [
        ('none', 'None'),
        ('occasional', 'Occasional'),
        ('moderate', 'Moderate'),
        ('heavy', 'Heavy')
    ]
    
    EXERCISE_FREQUENCY_CHOICES = [
        ('sedentary', 'Sedentary (No exercise)'),
        ('light', 'Light (1-2 days/week)'),
        ('moderate', 'Moderate (3-5 days/week)'),
        ('active', 'Active (6-7 days/week)'),
        ('very_active', 'Very Active (Multiple times per day)')
    ]
    
    DIET_TYPE_CHOICES = [
        ('balanced', 'Balanced Diet'),
        ('high_protein', 'High Protein'),
        ('low_carb', 'Low Carb'),
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('keto', 'Keto'),
        ('paleo', 'Paleo'),
        ('other', 'Other')
    ]
    
    STRESS_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('very_high', 'Very High')
    ]
    
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    alcohol_consumption = forms.ChoiceField(choices=ALCOHOL_CHOICES)
    exercise_frequency = forms.ChoiceField(choices=EXERCISE_FREQUENCY_CHOICES)
    diet_type = forms.ChoiceField(choices=DIET_TYPE_CHOICES)
    stress_level = forms.ChoiceField(choices=STRESS_LEVEL_CHOICES)
    family_history = forms.CharField(widget=forms.Textarea, required=False, 
                                     help_text="List any significant family health conditions")
    existing_conditions = forms.CharField(widget=forms.Textarea, required=False,
                                         help_text="List any diagnosed health conditions you have")
    medications = forms.CharField(widget=forms.Textarea, required=False,
                                 help_text="List any medications you take regularly")
    
    class Meta:
        model = HealthProfile
        exclude = ['user', 'created_at', 'updated_at']
        widgets = {
            'height': forms.NumberInput(attrs={'step': '0.01'}),
            'weight': forms.NumberInput(attrs={'step': '0.1'}),
            'sleep_hours': forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '24'}),
        }


class FollowUpQuestionForm(forms.Form):
    """Form for asking follow-up health questions"""
    question = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ask a follow-up question about your health analysis...'}),
                              label="Your Question")