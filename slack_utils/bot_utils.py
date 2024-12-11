import re
from slack_utils.messages.translation_delivery import translation_delivery_message
from slack_utils.post_message_to_slack import post_message_to_slack

def extract_slack_id_from_text(text: str) -> str:
    pattern = r"slack.com/archives/(\w+)"
    match = re.search(pattern, text)

    if match:
        slack_id = match.group(1)
        return slack_id

    return text


def send_translation_delivery_message_to_all(channels_prs_dict: dict) -> None:
    if len(channels_prs_dict) == 0:
        return
    for channel_id, prs in channels_prs_dict.items():
        message = translation_delivery_message(prs)
        post_message_to_slack(channel_id, message)