import os
import xmltodict

parent_dir = os.getcwd()
default_collection_branch = 'translations-collection'

git_token = os.environ['GITHUB_TOKEN']
git_url = os.environ['GIT_ORIGIN_URL']
print(git_token)
print(git_url)

# Parse the XML file
with open(f'{parent_dir}/reference.xml') as fd:
    doc = xmltodict.parse(fd.read())

os.system(f'git remote set-url origin {git_url}')
os.system(f'git checkout origin {default_collection_branch}')
os.system('git config pull.rebase false')

# Loop over the project elements in the XML file
for project in doc['manifest']['project']:
    repo = project['@name']
    revision = project.get('@revision', 'main') # This is optional, default to 'main'
    branch = project.get('@branch')
    
    # create new branch to collect all translations updates from all repos
    os.system(f'git pull origin {branch}')
    
os.system(f'git push origin {default_collection_branch}')
os.system('gh pr create --base main --head translations-collection --title "Translations Update" --body "Translations Update"')