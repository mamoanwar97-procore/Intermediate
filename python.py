import os
import xmltodict
import subprocess

main_branch = 'main'
username='mamoanwar97-procore'
repo='Intermediate'
parent_dir = os.getcwd()
default_collection_branch = 'translations-collection'

# Parse the XML file
with open(f'{parent_dir}/reference.xml') as fd:
    doc = xmltodict.parse(fd.read())

#git clone the current repo
subprocess.run(['git', 'clone', '-b', main_branch, f'git@github.com:{username}/{repo}', f'{parent_dir}'])
subprocess.run(['ls', '-la', f'{parent_dir}'])