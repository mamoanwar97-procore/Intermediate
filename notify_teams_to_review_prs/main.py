from bot_utils import (
    group_prs_by_channel,
    send_translation_delivery_message_to_all,
)
from use_reference_to_list_repos_slack import use_reference_to_list_repos_slack
from use_repo_channel_ids_dict_to_list_prs import (
    use_repo_channel_ids_dict_to_list_prs,
)

def notify_repos(skipped_repos: list[str] = []):
    channel_repos_arr = use_reference_to_list_repos_slack(skipped_repos)
    entries = use_repo_channel_ids_dict_to_list_prs(channel_repos_arr, skipped_repos)
    channels_prs_dict = group_prs_by_channel(entries)
    send_translation_delivery_message_to_all(channels_prs_dict)

if __name__ == "__main__":
    notify_repos()
