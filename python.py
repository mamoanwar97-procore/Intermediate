import os
import xmltodict
import subprocess

parent_dir = os.getcwd()
default_collection_branch = 'translations-collection'
env = os.environ.copy()
print(env)

# Parse the XML file
with open(f'{parent_dir}/reference.xml') as fd:
    doc = xmltodict.parse(fd.read())

subprocess.run(['git', 'fetch', '--all'])
subprocess.run(['git', 'checkout', f'origin/{default_collection_branch}'])
# subprocess.run(['git', 'config', 'pull.rebase', 'false'])
# # Loop over the project elements in the XML file
# for project in doc['manifest']['project']:
#     repo = project['@name']
#     revision = project.get('@revision', 'main') # This is optional, default to 'main'
#     branch = project.get('@branch')
    
#     # create new branch to collect all translations updates from all repos
#     subprocess.run(['git', 'pull', 'origin', branch])
    
# subprocess.run(['git', 'push', 'origin', default_collection_branch])
# # subprocess.run(['gh', 'pr', 'create', '--base', 'main', '--head', default_collection_branch, '--title', 'Translations Update', '--body', 'Translations Update'])