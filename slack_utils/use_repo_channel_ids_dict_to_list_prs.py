from slack_utils.get_translation_delivery_prs_by_repo_name import (
    get_translation_delivery_prs_by_repo_name,
)

def use_repo_channel_ids_dict_to_list_prs(
    channel_repos_arr: dict[str, list[str]], skipped_repos: list[str] = None
) -> dict[str, list[str]]:
    if skipped_repos is None:
        skipped_repos = []
    slack_prs_dict: dict[str, list[str]] = {}
    for repo, channel_ids in channel_repos_arr.items():
        if repo in skipped_repos:
            continue
        prs = get_translation_delivery_prs_by_repo_name(repo)
        if len(prs) == 0:
            continue
        for channel_id in channel_ids:
            if channel_id in slack_prs_dict:
                slack_prs_dict[channel_id].extend(prs)
            else:
                slack_prs_dict[channel_id] = list(prs)  # Create a new list to avoid sharing references
    return slack_prs_dict
