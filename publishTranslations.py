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


# print all the folders in the PR
def get_folders_in_pr(pr_number, repo_name, repo_owner, github_token):
    # Use the correct GitHub API endpoint for PR details
    pr_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}"
    logging.info(f"PR URL: {pr_url}")

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Make the request to GitHub API
    response = requests.get(pr_url, headers=headers)
    
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
    pr_files = response_data.get('files', [])
    
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
    
    logging.info(f"Found folders: {folders}")
    return folders

def run():
    logging.info(f"PR_NUMBER: {pr_number}")
    folders = get_folders_in_pr(pr_number, repo_name, repo_owner, github_token)
    logging.info(f"Folders in PR: {folders}")

if __name__ == "__main__":
    run()
