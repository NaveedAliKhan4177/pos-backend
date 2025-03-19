import traceback
import logging
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .api.utils import send_slack_error_message  # Import the function

class SlackErrorMiddleware(MiddlewareMixin):
    """Middleware to catch all exceptions and send error messages to Slack."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            error_message = traceback.format_exc()  # Get full error traceback
            logging.error(f"Unhandled Exception: {error_message}")  # Log error locally
            send_slack_error_message(error_message)  # Send error to Slack
            
            return JsonResponse(
                {"error": "An unexpected error occurred. Please try again later."}, 
                status=500
            )
