# health_analyzer/urls.py
from django.urls import path
from . import views

app_name = 'health_analyzer'

urlpatterns = [
    path('profile/', views.health_profile_view, name='profile'),
    path('analyze/', views.analyze_health_data, name='analyze'),
    path('analysis/<int:analysis_id>/', views.analysis_results, name='analysis_results'),
    path('analysis/<int:analysis_id>/ask/', views.follow_up_question, name='follow_up'),
]