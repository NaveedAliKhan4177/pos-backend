import os
import logging
import requests

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_error_message(error_message):
    """Send properly formatted error messages to Slack."""
    if not SLACK_WEBHOOK_URL:
        logging.warning("⚠️ Slack Webhook URL is not set. Skipping notification.")
        return

    # Slack has a 4000-character limit; we truncate at 3900 to be safe
    max_length = 3900  
    truncated_error = (error_message[:max_length] + '...') if len(error_message) > max_length else error_message

    payload = {
        "text": ":rotating_light: *ERROR ALERT* :rotating_light:\n```" + truncated_error + "```"
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()  # Raise an error if request fails
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Failed to send Slack notification: {e}")
