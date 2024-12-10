import subprocess
import json

def get_translation_delivery_prs_by_repo_name(repo: str) -> list[str]:
    procore_repo = f"mamoanwar97-procore/{repo}"
    command = f'gh pr list --repo {procore_repo} --search "Changes from " --json url'  # Can be filtered by label after it gets merged
    result = subprocess.run(
        command, shell=True, check=True, text=True, capture_output=True
    )
    prs = json.loads(result.stdout)

    urls = []

    if len(prs) == 0:
        return urls

    for pr in prs:
        urls.append(pr["url"])

    return urls
