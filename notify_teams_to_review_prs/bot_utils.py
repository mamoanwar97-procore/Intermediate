import re
from messages.translation_delivery import translation_delivery_message
from post_message_to_slack import post_message_to_slack


def build_channel_id_prs_dict(channel_id: str, prs: list[str]) -> dict[str, list[str]]:
    return {channel_id: prs}


def group_prs_by_channel(entries: list[dict[str, list[str]]]):
    slack_prs_dict: dict[str, list[str]] = {}
    for entry in entries:
        for channel_id, prs in entry.items():
            if channel_id in slack_prs_dict:
                # Concatenate the new array with the existing one
                slack_prs_dict[channel_id].extend(prs)
            else:
                # Save the ID as the key and the array as the value in the dictionary
                slack_prs_dict[channel_id] = prs
    return slack_prs_dict


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