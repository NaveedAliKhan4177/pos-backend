import os
import traceback
import logging
import requests
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

class SlackErrorMiddleware(MiddlewareMixin):
    """Middleware to catch all exceptions and send error messages to Slack."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception:
            error_message = traceback.format_exc()  # Get full error traceback
            logging.error(f"Unhandled Exception: {error_message}")  # Log error locally
            self.send_slack_error_message(error_message)  # Send error to Slack
            
            return JsonResponse(
                {"error": "An unexpected error occurred. Please try again later."}, 
                status=500
            )

    def send_slack_error_message(self, error_message):
        """Send error messages to Slack if webhook is configured."""
        if not SLACK_WEBHOOK_URL:
            logging.warning("⚠️ Slack Webhook URL is not set. Skipping notification.")
            return  # Skip if webhook URL is missing

        # Slack has a 4000-character message limit, truncate if needed
        max_length = 3900  # Leaving space for formatting
        truncated_error = (error_message[:max_length] + '...') if len(error_message) > max_length else error_message

        payload = {
            "text": f":rotating_light: *ERROR ALERT* :rotating_light:\n```{truncated_error}```"
        }

        try:
            response = requests.post(SLACK_WEBHOOK_URL, json=payload)
            response.raise_for_status()  # Raise exception for failed requests
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Failed to send Slack notification: {e}")
