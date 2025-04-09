# health_analyzer/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse

from .models import HealthProfile, HealthAnalysis, FollowUpConversation
from .forms import HealthProfileForm, FollowUpQuestionForm
from .services.gemini_service import GeminiHealthService

import json
import logging

logger = logging.getLogger(__name__)


@login_required
def health_profile_view(request):
    """View for creating or updating health profile"""
    try:
        # Try to get existing profile
        profile = HealthProfile.objects.get(user=request.user)
        is_new = False
    except HealthProfile.DoesNotExist:
        # Create a new profile if none exists
        profile = None
        is_new = True
    
    if request.method == 'POST':
        form = HealthProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Health profile saved successfully!")
            return redirect('health_analyzer:analyze')
    else:
        form = HealthProfileForm(instance=profile)
    
    return render(request, 'health_analyzer/analyze_form.html', {
        'form': form,
        'is_new': is_new
    })


@login_required
def analyze_health_data(request):
    """View for analyzing health data and showing results"""
    try:
        profile = HealthProfile.objects.get(user=request.user)
    except HealthProfile.DoesNotExist:
        messages.warning(request, "Please complete your health profile first.")
        return redirect('health_analyzer:profile')
    
    # Check if we already have a recent analysis
    latest_analysis = HealthAnalysis.objects.filter(health_profile=profile).order_by('-created_at').first()
    
    # If the form was submitted, generate a new analysis
    if request.method == 'POST':
        try:
            gemini_service = GeminiHealthService()
            analysis_results = gemini_service.analyze_health_data(profile)
            
            # Save the analysis results
            analysis = HealthAnalysis(
                health_profile=profile,
                current_health_assessment=analysis_results['current_health_assessment'],
                potential_health_issues=analysis_results['potential_health_issues'],
                risk_minimization_recommendations=analysis_results['risk_minimization_recommendations'],
                full_analysis=analysis_results['full_analysis']
            )
            analysis.save()
            
            messages.success(request, "Health analysis completed successfully!")
            return redirect('health_analyzer:analysis_results', analysis_id=analysis.id)
            
        except Exception as e:
            logger.error(f"Error during health analysis: {str(e)}")
            messages.error(request, "An error occurred during analysis. Please try again later.")
    
    return render(request, 'health_analyzer/analyze.html', {
        'profile': profile,
        'latest_analysis': latest_analysis
    })


@login_required
def analysis_results(request, analysis_id):
    """View for displaying analysis results and follow-up conversation"""
    analysis = get_object_or_404(HealthAnalysis, id=analysis_id)
    
    # Security check - make sure the analysis belongs to the current user
    if analysis.health_profile.user != request.user:
        messages.error(request, "You don't have permission to view this analysis.")
        return redirect('health_analyzer:profile')
    
    # Get previous conversations for this analysis
    conversations = FollowUpConversation.objects.filter(health_analysis=analysis).order_by('created_at')
    
    # Form for follow-up questions
    form = FollowUpQuestionForm()
    
    return render(request, 'health_analyzer/analysis.html', {
        'analysis': analysis,
        'conversations': conversations,
        'form': form
    })


@login_required
@require_http_methods(["POST"])
def follow_up_question(request, analysis_id):
    """Handle follow-up questions via AJAX"""
    analysis = get_object_or_404(HealthAnalysis, id=analysis_id)
    
    # Security check
    if analysis.health_profile.user != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    # Get the question from POST data
    question = request.POST.get('question', '').strip()
    if not question:
        return JsonResponse({'error': 'Question cannot be empty'}, status=400)
    
    # Get previous conversations for context
    previous_conversations = FollowUpConversation.objects.filter(health_analysis=analysis).order_by('created_at')
    
    try:
        # Get answer from Gemini
        gemini_service = GeminiHealthService()
        answer = gemini_service.follow_up_question(
            analysis.health_profile, 
            analysis, 
            question,
            previous_conversations
        )
        
        # Save the conversation
        conversation = FollowUpConversation(
            health_analysis=analysis,
            question=question,
            answer=answer
        )
        conversation.save()
        
        return JsonResponse({
            'success': True,
            'question': question,
            'answer': answer,
            'conversation_id': conversation.id
        })
        
    except Exception as e:
        logger.error(f"Error processing follow-up question: {str(e)}")
        return JsonResponse({'error': 'An error occurred processing your question'}, status=500)