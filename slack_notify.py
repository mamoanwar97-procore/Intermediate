from slack_utils.bot_utils import (
    send_translation_delivery_message_to_all,
)
from slack_utils.use_reference_to_list_repos_slack import use_reference_to_list_repos_slack
from slack_utils.use_repo_channel_ids_dict_to_list_prs import (
    use_repo_channel_ids_dict_to_list_prs,
)

def notify_repos(skipped_repos: list[str] = []):
    channel_repos_arr = use_reference_to_list_repos_slack(skipped_repos)
    entries = use_repo_channel_ids_dict_to_list_prs(channel_repos_arr, skipped_repos)
    send_translation_delivery_message_to_all(entries)

if __name__ == "__main__":
    notify_repos()
