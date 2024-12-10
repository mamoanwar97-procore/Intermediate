# print all the folders in the PR
# this will be run on the workflow

import os
import sys
import requests


# Get the PR number
pr_number = os.getenv('PR_NUMBER')
if pr_number == None:
    print("PR_NUMBER not found")
    sys.exit(1)

# Get the repo name it will the same repo where the PR is raised
repo_name = os.getenv('REPO_NAME')
if repo_name == None:
    print("REPO_NAME not found")
    sys.exit(1)

# Get the repo owner
repo_owner = os.getenv('REPO_OWNER')
if repo_owner == None:
    print("REPO_OWNER not found")
    sys.exit(1)

# Get the GITHUB_TOKEN
github_token = os.getenv('GITHUB_TOKEN')
if github_token == None:
    print("GITHUB_TOKEN not found")
    sys.exit(1)

# print all the folders in the PR
def get_folders_in_pr(pr_number, repo_name, repo_owner, github_token):
    # Get the PR details
    pr_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(pr_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to get PR details: {response.status_code}")
        sys.exit(1)
    pr_data = response.json()
    pr_files = pr_data['files']

    # Get the folders in the PR
    folders = []
    for pr_file in pr_files:
        folder = os.path.dirname(pr_file['filename'])
        if folder not in folders:
            folders.append(folder)
    return folders

def main():
    folders = get_folders_in_pr(pr_number, repo_name, repo_owner, github_token)
    print(folders)

