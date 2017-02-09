
import os
import sys


c.JupyterHub.services = [
    {
        'name': 'jh-save',
        'url': 'http://127.0.0.1:10149',
        'command': [sys.executable, './jh-save.py'],
        'environment': {
        	#The path to user folders, where their notebooks are stored.
        	#You can use {user} which will be replaced by the user's name, eg. '/home/{user}'
        	'JUPYTERHUB_USER_PATH': '/home/{user}',

            #The regular expression corresponding to the files that should be saved
            #from the server. By default this is all non-hidden .ipynb files.
            #Case is ignored in matching.
            'JUPYTERHUB_SAVE_REGEX': r'[^.].*\.ipynb$',

        }
    }
]