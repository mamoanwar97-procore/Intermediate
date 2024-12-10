import os
import xmltodict
import subprocess

def run():
    parent_dir = os.environ.get('PWD')
    default_collection_branch = os.environ.get('BRANCH')
    env = os.environ.copy()
    print(env)
    print(default_collection_branch)
    subprocess.run(['ls'], cwd=f'{parent_dir}/.git/refs/heads')
    subprocess.run(['git', 'fetch'], cwd=f'{parent_dir}')
    subprocess.run(['git', 'checkout', 'main'], cwd=f'{parent_dir}')
    subprocess.run(['git', 'checkout', '-b', default_collection_branch], cwd=f'{parent_dir}')
    subprocess.run(['git', 'config', 'pull.rebase', 'false'], cwd=f'{parent_dir}')
    subprocess.run(['git', 'pull', 'origin', 'update-translations-mfe1'], cwd=f'{parent_dir}')
    

if __name__ == "__main__":
    run()