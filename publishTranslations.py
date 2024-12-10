import os
import sys
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Get the PR number
pr_number = os.getenv('PR_NUMBER')
if pr_number is None:
    logging.info("PR_NUMBER not found")
    sys.exit(1)

# Get the repo name it will the same repo where the PR is raised
repo_name = os.getenv('REPO_NAME')
if repo_name is None:
    logging.info("REPO_NAME not found")
    sys.exit(1)

# Get the repo owner
repo_owner = os.getenv('REPO_OWNER')
if repo_owner is None:
    logging.info("REPO_OWNER not found")
    sys.exit(1)

# Get the GITHUB_TOKEN
github_token = os.getenv('GITHUB_TOKEN')
if github_token is None:
    logging.info("GITHUB_TOKEN not found")
    sys.exit(1)

if isinstance(github_token, bytes):
    logging.info("GITHUB_TOKEN is bytes")
    github_token = github_token.decode('utf-8')


# print all the folders in the PR
def get_folders_in_pr(pr_number, repo_name, github_token):
    # Use the correct GitHub API endpoint for PR details
    pr_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files"
    logging.info(f"PR URL: {pr_url}")

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    headers = {k: str(v) for k, v in headers.items()}


    # Make the request to GitHub API
    response = requests.get(pr_url, headers)
    
    # Log the response status and JSON content
    logging.info(f"Response Status Code: {response.status_code}")
    
    try:
        response_data = response.json()  # Get the response JSON content
        logging.info(f"Response Data: {response_data}")  # Log the response data
    except ValueError:
        logging.error("Failed to parse response as JSON")
        sys.exit(1)

    if response.status_code != 200:
        logging.error(f"Failed to get PR details: {response.status_code} - {response_data.get('message', 'No additional info')}")
        sys.exit(1)

    # Check if the 'files' key exists in the response
    pr_files = response_data
    
    # If there are no files, log and return an empty list
    if not pr_files:
        logging.info("No files found in the PR.")
        return []

    # Get the folders in the PR by extracting folder names from file paths
    folders = []
    for pr_file in pr_files:
        # Get the directory (folder) from the file path
        folder = os.path.dirname(pr_file['filename'])
        if folder not in folders:
            folders.append(folder)
    
    # this is the folders example ['MFE1/translations', 'MFE1/translations/lvl2/v1', 'MFE2/translations/src/locales', 'MFE3/translations/src/dummy/es']
    # group by the first slice of the folder like MFE1 or MFE2
    targetRepoNames = [folder.split('/')[0] for folder in folders]
    targetRepoNames = list(set(targetRepoNames))
    
    print(f"Target Repos: {pr_files}")
    # TODO: split this in a seperate function 
    # create a pr in the target repo names with the changes under it 
    for targetRepoName in targetRepoNames:
        # create a PR in the target repo
        current_pr_files = [pr_file for pr_file in pr_files if pr_file['filename'].startswith(targetRepoName)]
        print(f"Creating PR in {targetRepoName}, with files {current_pr_files}")
        # create a PR in the target repo
        create_pr_in_target_repo(targetRepoName, current_pr_files, github_token)

    return targetRepoNames


def create_pr_in_target_repo(targetRepoName, pr_files, github_token):
    # create a new branch in the target repo
    url = f"https://api.github.com/repos/{repo_owner}/{targetRepoName}/git/refs"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    headers = {k: str(v) for k, v in headers.items()}
    data = {
        "ref": "refs/heads/translations",
        "sha": "master"
    }
    response = requests.post(url, headers=headers, json=data)
    print('final',response.json())

    # create a new PR in the target repo



def run():
    get_folders_in_pr(pr_number, repo_name, github_token)

if __name__ == "__main__":
    run()
