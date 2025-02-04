from subprocess import run
import requests
from pathlib import Path
from json import loads
from os import path, remove
import sys

from utils import *


def main():
    activity_id = get_activity_id()
            
    # Get project gist link
    response = requests.get(f'http://127.0.0.1:8000/projects/get/{activity_id}')
    if response.status_code != 200:
        exit('Project link is not found')
    
    content = response.content
    data = loads(content.decode())
    
    response = requests.get(data['url'])
    
    if response.status_code == 200:
        tmp_test_file = Path('test_file_tmp.py')
        tmp_test_file.touch()
        
        f = open(tmp_test_file, 'wb')
        f.write(response.content)
        f.close()
        
    else:
        print('Bro, something wrong happened!!')
    
    results = run(['python3', '-m', 'colorful_test', 'test_file_tmp.py'], capture_output=True, text=True)
    if results.stdout:
        print(results.stdout)
    else:
        print(results.stderr)
        
    remove(tmp_test_file)
        
if __name__ == '__main__':
    main()
