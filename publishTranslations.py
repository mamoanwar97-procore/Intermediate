import os
import sys
import requests
import logging
from github import Github
import xmltodict
import subprocess
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

doc = None
parent_dir = os.getcwd()
with open(f'{parent_dir}/reference.xml') as fd:
    doc = xmltodict.parse(fd.read())

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

# Decode and strip the GitHub token to remove any unwanted characters (such as \n or extra spaces)
if isinstance(github_token, bytes):
    github_token = github_token.decode('utf-8')

# Ensure the token is stripped of any extra whitespace
github_token = github_token.strip()

# Function to get the folders in a pull request
def get_folders_in_pr(pr_number, repo_name, github_token):
    # GitHub API URL to get PR files
    pr_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files"
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
    pr_files = response_data
    
    # If there are no files, log and return an empty list
    if not pr_files:
        logging.info("No files found in the PR.")
        return []

    # Get the folders in the PR by extracting folder names from file paths
    folders = []
    for pr_file in pr_files:
        folder = os.path.dirname(pr_file['filename'])
        if folder not in folders:
            folders.append(folder)
    
    # this is the folders example ['MFE1/translations', 'MFE1/translations/lvl2/v1', 'MFE2/translations/src/locales', 'MFE3/translations/src/dummy/es']
    # group by the first slice of the folder like MFE1 or MFE2
    targetRepoNames = [folder.split('/')[0] for folder in folders]
    targetRepoNames = list(set(targetRepoNames))
    
    logging.info(f"Target Repos: {targetRepoNames}")
    # TODO: split this in a seperate function 
    # Create PRs in the target repositories
    for targetRepoName in targetRepoNames:
        current_pr_files = [pr_file for pr_file in pr_files if pr_file['filename'].startswith(targetRepoName)]
        logging.info(f"Creating PR in {targetRepoName}, with files {current_pr_files}")
        create_pr_in_target_repo(targetRepoName, current_pr_files, github_token)

    return targetRepoNames


def extract_json_from_patch(patch):
    # Remove lines that start with diff markers like '@@' and '-'
    json_lines = []
    for line in patch.splitlines():
        if line.startswith('+') and not line.startswith('+++'):  # Only get added lines, ignore the diff header lines
            json_lines.append(line[1:]+'\n')  # Remove the '+' from the start of each added line

    # Combine all added lines into a single string and return it as JSON content
    json_content = ''.join(json_lines)
    return json_content

# Function to create a PR in the target repo
def create_pr_in_target_repo(targetRepoName, pr_files, github_token):
    try:
        # Authenticate with GitHub using the token
        g = Github(github_token)

        # Get the target repository
        target_repo = g.get_repo(f"{repo_owner}/{targetRepoName}")

        project_xml_data = next((project for project in doc['manifest']['project'] if project['@name'] == targetRepoName ), None)

        # Generate a new branch in the target repo (e.g., 'feature/pr-26')
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        new_branch_name = f"feature/pr-{pr_number}-{current_time}"
        # TODO: make this dynamic
        revision = project_xml_data.get('@revision', 'main')
        logging.info('final el final',project_xml_data)
        base_branch = target_repo.get_branch(revision)
        target_repo.create_git_ref(ref=f"refs/heads/{new_branch_name}", sha=base_branch.commit.sha)

        
        # Add files to the new branch
        for pr_file in pr_files:
            pr_file['filename'] = pr_file['filename'].replace("/translations/", "/")
            json_content = extract_json_from_patch(pr_file['patch'])

            target_repo.create_file(
                pr_file['filename'],
                f"Add changes from PR {pr_number}",
                json_content,  # The file patch (content)
                branch=new_branch_name
            )

        # Create the pull request in the target repo
        pr_title = f"PR {pr_number}: Changes from {repo_name}"
        pr_body = f"Pull request automatically created from PR {pr_number} in {repo_name}."
        target_repo.create_pull(
            title=pr_title,
            body=pr_body,
            head=new_branch_name,
            base=revision
        )

        logging.info(f"Successfully created PR in {targetRepoName}")
    except Exception as e:
        logging.error(f"Error creating PR in {targetRepoName}: {str(e)}")


# Main function to execute the process
def run():
    get_folders_in_pr(pr_number, repo_name, github_token)





if __name__ == "__main__":
    run()
