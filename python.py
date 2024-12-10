import os
import xmltodict
import subprocess

parent_dir = os.getcwd()
with open(f'{parent_dir}/reference.xml') as fd:
    doc = xmltodict.parse(fd.read())

def run():
    default_collection_branch = os.environ.get('BRANCH')
    main_dir = os.environ.get('PWD')
    subprocess.run(['git', 'fetch'], cwd=f'{main_dir}')
    subprocess.run(['git', 'checkout', 'main'], cwd=f'{main_dir}')
    subprocess.run(['git', 'checkout', '-b', default_collection_branch], cwd=f'{main_dir}')
    subprocess.run(['git', 'config', 'pull.rebase', 'false'], cwd=f'{main_dir}')
    
    # Loop over the project elements in the XML file
    for project in doc['manifest']['project']:
        branch = project.get('@branch')
    
        # create new branch to collect all translations updates from all repos
        subprocess.run(['git', 'pull', 'origin', branch], cwd=f'{main_dir}')
    
    subprocess.run(['git', 'push', 'origin', default_collection_branch] , cwd=f'{main_dir}')

if __name__ == "__main__":
    run()