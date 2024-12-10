import requests
import json
import os

slack_webhook_url = os.getenv('SLACK_HOOK_URL');

def post_message_to_slack(channel_id: str, message: str):

    payload = {
        "channel_id": channel_id,
        "message": message,
    }

    # Convert the payload to JSON format
    payload_json = json.dumps(payload)

    # Send the POST request to the Slack webhook URL
    response = requests.post(
        slack_webhook_url,
        headers={"Content-Type": "application/json"},
        data=payload_json,
    )

    # Check the response status
    if response.status_code == 200:
        print(
            f"Message posted successfully for channel https://procore.enterprise.slack.com/archives/{channel_id}."
        )
    else:
        print(
            f"Failed to post message. Status code: {response.status_code}, for channel https://procore.enterprise.slack.com/archives/{channel_id}, with message of {message}"
        )
