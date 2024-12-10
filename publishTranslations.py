# Description: This script is used to publish the translations to the server
# this is the python script should get all the changes filed and path from the PR 

import os
import sys
import json
import requests
import logging
import argparse
import subprocess
import re
import time
import shutil
from datetime import datetime
from requests.auth import HTTPBasicAuth

# Constants
TRANSLATION_PATH = 'translations'
TRANSLATION_FILE = 'translations.json'
TRANSLATION_API = 'https://api.crowdin.com/api/project/{}'
TRANSLATION_API_KEY = os.environ['CROWDIN_API_KEY']
TRANSLATION_PROJECT_ID = os.environ['CROWDIN_PROJECT_ID']
TRANSLATION_BRANCH = 'master'
TRANSLATION_COMMIT_MESSAGE = 'Update translations'
TRANSLATION_COMMIT_AUTHOR = ''
TRANSLATION_COMMIT_EMAIL = ''
TRANSLATION_COMMIT_NAME = ''
TRANSLATION_COMMIT_DATE = ''
TRANSLATION_COMMIT_HASH = ''
TRANSLATION_COMMIT_BRANCH = ''
TRANSLATION_COMMIT_MESSAGE = ''

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Functions
def getTranslations():
    logger.info('Getting translations')
    url = TRANSLATION_API.format(TRANSLATION_PROJECT_ID)
    params = {
        'key': TRANSLATION_API_KEY,
        'json': ''
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    translations = response.json()
    with open(TRANSLATION_FILE, 'w') as file:
        json.dump(translations, file, indent=4)
    logger.info('Translations saved to {}'.format(TRANSLATION_FILE))

def publishTranslations():
    logger.info('Publishing translations')
    url = TRANSLATION_API.format(TRANSLATION_PROJECT_ID) + '/export'
    params = {
        'key': TRANSLATION_API_KEY
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    logger.info('Translations published')

def commitTranslations():
    logger.info('Committing translations')
    os.chdir(TRANSLATION_PATH)
    subprocess.run(['git', 'config', 'user.name', TRANSLATION_COMMIT_NAME])
    subprocess.run(['git', 'config', 'user.email', TRANSLATION_COMMIT_EMAIL])
    subprocess.run(['git', 'config', 'commit.gpgSign', 'false'])
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', TRANSLATION_COMMIT_MESSAGE])
    subprocess.run(['git', 'push', 'origin', TRANSLATION_BRANCH])
    os.chdir('..')
    logger.info('Translations committed')

def main():
    getTranslations()
    publishTranslations()
    commitTranslations()

    