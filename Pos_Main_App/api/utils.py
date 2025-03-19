import requests
import json
import traceback
import logging
from django.conf import settings

def send_slack_error_message(error_message):
    """Send formatted error logs to Slack via Webhook."""
    webhook_url = getattr(settings, "SLACK_WEBHOOK_URL", None)
    
    if not webhook_url:
        logging.warning("⚠️ Slack Webhook URL is not set in settings. Skipping Slack notification.")
        return  # Skip if the webhook URL is not set

    slack_data = {"text": f"🚨 *ERROR ALERT* 🚨\n```{error_message}```"}
    
    try:
        response = requests.post(
            webhook_url, 
            data=json.dumps(slack_data), 
            headers={"Content-Type": "application/json"}
        )

        if response.status_code != 200:
            logging.error(f"❌ Slack notification failed: {response.text}")
    except Exception as e:
        logging.error(f"❌ Failed to send Slack message: {traceback.format_exc()}")
