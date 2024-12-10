import json
import os
import xmltodict
from get_translation_delivery_prs_by_repo_name import (
    get_translation_delivery_prs_by_repo_name,
)
from bot_utils import extract_slack_id_from_text, build_channel_id_prs_dict

parent_dir = os.getcwd()

# Parse the XML file
def use_reference_to_list_repos_slack(
    skipped_repos: list[str] = [],
) -> dict[str, list[str]]:
    with open(f"{parent_dir}/reference.xml") as fd:
        doc = xmltodict.parse(fd.read())

    repo_slack_ids: dict[str, list[str]] = {}

    # Loop over the project elements in the XML file
    for project in doc["manifest"]["project"]:
        # Get the repo name and revision
        repo = project["@name"]

        if repo in skipped_repos:
            print(f"Skipping {repo}")
            continue

        prs = get_translation_delivery_prs_by_repo_name(repo)

        if len(prs) == 0:
            print(f"No PRs found for {repo}")
            continue

        slack_urls_stringified = project.get("@slack", False)

        if slack_urls_stringified == False:
            continue

        slack_urls = slack_urls_stringified.split(',')

        channel_ids = []

        for url in slack_urls:
            channel_id = extract_slack_id_from_text(url)
            channel_ids.append(channel_id)

        if len(channel_ids) == 0:
            continue

        repo_slack_ids[repo] = channel_ids

    return repo_slack_ids
