from get_translation_delivery_prs_by_repo_name import (
    get_translation_delivery_prs_by_repo_name,
)
from bot_utils import build_channel_id_prs_dict, extract_slack_id_from_text


def use_repo_channel_ids_dict_to_list_prs(
    channel_repos_arr: dict[str, list[str]], skipped_repos: list[str] = str
) -> list[dict[str, list[str]]]:
    slack_prs_arr = []

    for repo, channel_ids in channel_repos_arr.items():
        if repo in skipped_repos:
            continue
        prs = get_translation_delivery_prs_by_repo_name(repo)
        if len(prs) == 0:
            continue
        for channel_id in channel_ids:
            slack_prs_arr.append(
                build_channel_id_prs_dict(extract_slack_id_from_text(channel_id), prs)
            )

    return slack_prs_arr
