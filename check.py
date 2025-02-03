from subprocess import run
import requests
from pathlib import Path


def main():
    response = requests.get('https://gist.githubusercontent.com/lindelwa122/12c9a25ff8250b2949bb36baebf035d5/raw/194e5cdd320644ff0436d93e0c287b91d32cbf6e/calculator.py')
    
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


if __name__ == '__main__':
    main()
