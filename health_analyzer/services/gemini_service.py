# health_analyzer/services/gemini_service.py
import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class GeminiHealthService:
    """Service for interacting with Google Gemini API for health analysis"""
    
    def __init__(self):
        """Initialize the Gemini service with API key from settings"""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        except Exception as e:
            logger.error(f"Failed to initialize Gemini service: {str(e)}")
            raise
    
    def _format_health_data(self, health_profile):
        """Format health profile data into a structured string for the prompt"""
        health_data = (
            f"Age: {health_profile.age}\n"
            f"Gender: {health_profile.gender}\n"
            f"Height: {health_profile.height} cm\n"
            f"Weight: {health_profile.weight} kg\n"
            f"BMI: {(health_profile.weight / ((health_profile.height/100) ** 2)):.2f}\n"
        )
        
        # Add optional health metrics if available
        if health_profile.blood_pressure_systolic and health_profile.blood_pressure_diastolic:
            health_data += f"Blood Pressure: {health_profile.blood_pressure_systolic}/{health_profile.blood_pressure_diastolic} mmHg\n"
        if health_profile.heart_rate:
            health_data += f"Heart Rate: {health_profile.heart_rate} bpm\n"
        if health_profile.cholesterol_level:
            health_data += f"Cholesterol: {health_profile.cholesterol_level}\n"
        if health_profile.blood_sugar:
            health_data += f"Blood Sugar: {health_profile.blood_sugar}\n"
        if health_profile.family_history:
            health_data += f"Family History: {health_profile.family_history}\n"
        if health_profile.existing_conditions:
            health_data += f"Existing Conditions: {health_profile.existing_conditions}\n"
        if health_profile.medications:
            health_data += f"Medications: {health_profile.medications}\n"
            
        return health_data
    
    def _format_personal_habits(self, health_profile):
        """Format personal habits data into a structured string for the prompt"""
        habits = (
            f"Smoking: {'Yes' if health_profile.smoker else 'No'}\n"
            f"Alcohol Consumption: {health_profile.alcohol_consumption}\n"
            f"Exercise Frequency: {health_profile.exercise_frequency}\n"
            f"Diet Type: {health_profile.diet_type}\n"
        )
        
        # Add optional habits if available
        if health_profile.exercise_intensity:
            habits += f"Exercise Intensity: {health_profile.exercise_intensity}\n"
        if health_profile.sleep_hours:
            habits += f"Sleep: {health_profile.sleep_hours} hours per night\n"
        if health_profile.stress_level:
            habits += f"Stress Level: {health_profile.stress_level}\n"
        if health_profile.water_intake:
            habits += f"Water Intake: {health_profile.water_intake}\n"
            
        return habits
    
    def analyze_health_data(self, health_profile):
        """
        Analyze health data using Gemini API
        
        Args:
            health_profile: HealthProfile instance containing user health data
            
        Returns:
            dict: Dictionary containing structured analysis results
        """
        health_data = self._format_health_data(health_profile)
        personal_habits = self._format_personal_habits(health_profile)
        
        prompt = f"""
        You are a health analysis assistant that helps identify potential health issues based on basic health data. 
        You are not a doctor and your analysis is not medical advice, but helpful insights based on general health knowledge.
        
        Based on the following health data and personal habits, please provide:
        
        1. CURRENT HEALTH ASSESSMENT: A brief assessment of the person's current health status based on the provided metrics.
        
        2. POTENTIAL HEALTH ISSUES: List and explain potential health concerns that may arise based on the data provided. 
           Consider both current metrics and long-term risks from habits.
        
        3. RISK MINIMIZATION RECOMMENDATIONS: Provide specific, actionable recommendations to minimize health risks 
           and improve overall wellbeing. Prioritize recommendations based on impact.
        
        HEALTH DATA:
        {health_data}
        
        PERSONAL HABITS:
        {personal_habits}
        
        Format your response with clear section headers for each of the three requested analyses.
        Start each section with "## SECTION_NAME" (e.g., "## CURRENT HEALTH ASSESSMENT").
        """
        
        try:
            response = self.model.generate_content(prompt)
            full_text = response.text
            print(full_text)
            # Parse the response into sections
            sections = {
                'current_health_assessment': '',
                'potential_health_issues': '',
                'risk_minimization_recommendations': '',
                'full_analysis': full_text
            }
            
            # Extract sections using markers
            if "## CURRENT HEALTH ASSESSMENT" in full_text and "## POTENTIAL HEALTH ISSUES" in full_text:
                sections['current_health_assessment'] = full_text.split("## CURRENT HEALTH ASSESSMENT")[1].split("## POTENTIAL HEALTH ISSUES")[0].strip()
            
            if "## POTENTIAL HEALTH ISSUES" in full_text and "## RISK MINIMIZATION RECOMMENDATIONS" in full_text:
                sections['potential_health_issues'] = full_text.split("## POTENTIAL HEALTH ISSUES")[1].split("## RISK MINIMIZATION RECOMMENDATIONS")[0].strip()
            
            if "## RISK MINIMIZATION RECOMMENDATIONS" in full_text:
                sections['risk_minimization_recommendations'] = full_text.split("## RISK MINIMIZATION RECOMMENDATIONS")[1].strip()
            
            return sections
            
        except Exception as e:
            logger.error(f"Error analyzing health data with Gemini: {str(e)}")
            raise
    
    def follow_up_question(self, health_profile, health_analysis, question, previous_conversations=None):
        """
        Send a follow-up question to Gemini based on previous health analysis
        
        Args:
            health_profile: HealthProfile instance
            health_analysis: HealthAnalysis instance 
            question: User's follow-up question
            previous_conversations: Optional list of previous FollowUpConversation objects
            
        Returns:
            str: Gemini's response to the follow-up question
        """
        # Format previous conversation context if available
        conversation_context = ""
        if previous_conversations:
            conversation_context = "Previous questions and answers:\n\n"
            for conv in previous_conversations:
                conversation_context += f"Q: {conv.question}\nA: {conv.answer}\n\n"
        
        health_data = self._format_health_data(health_profile)
        personal_habits = self._format_personal_habits(health_profile)
        
        # Include the previous analysis content
        previous_analysis = (
            f"## Previous Health Assessment:\n{health_analysis.current_health_assessment}\n\n"
            f"## Previous Potential Health Issues:\n{health_analysis.potential_health_issues}\n\n"
            f"## Previous Recommendations:\n{health_analysis.risk_minimization_recommendations}\n\n"
        )
        
        prompt = f"""
        You are a health analysis assistant that helps answer follow-up questions about health analysis.
        You are not a doctor and your responses are not medical advice, but helpful insights based on general health knowledge.
        
        HEALTH DATA:
        {health_data}
        
        PERSONAL HABITS:
        {personal_habits}
        
        PREVIOUS ANALYSIS:
        {previous_analysis}
        
        {conversation_context}
        
        Please answer the following follow-up question thoroughly and helpfully:
        
        USER QUESTION: {question}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error processing follow-up question with Gemini: {str(e)}")
            raise