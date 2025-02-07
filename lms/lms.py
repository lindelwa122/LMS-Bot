# Learning Management System (LMS)
from json import loads
from gitlab import exceptions as gl_exc, Gitlab
from os import environ, path, remove, system
from pathlib import Path
from requests import get, post
from subprocess import run
from sys import exit
from time import sleep

class LMS:
    def __init__(self, server_link: str, exercises_path: str = '.lms/exercises.toml', test_filename: str = 'test_temp_file.py', test_runner: str = 'colorful_test'):
        # Path where the activity is supposed to be stored
        self.exercises_path = exercises_path
        self.server_link = server_link
        self.test_runner = test_runner
        self.temp_test_filename = test_filename
    
    
    def get_activity_id(self):
        """
        Looks inside ".lms/exercises.toml" and tries to find the activity id.
        
        A typical toml file should look like this:
        
        ```toml
        _version = 0.1

        [calculator]
        activity_id = "calculator"
        ```
        
        "calculator" will be used as a project id in this case.
        """
        
        # If the '.lms/exercises.toml' path is not found or is not a file
        if not (path.exists(self.exercises_path) and path.isfile(self.exercises_path)):
            exit('Could\'t find ".lms/exercises.toml".')
            
        file = open(self.exercises_path, 'r')
        info = file.readlines()
        for line in info:
            # Find the line with 'activity_id'
            if 'activity_id' in line:
                activity_id = line.split('=')[1]
                
                # Clean up activity id
                activity_id = activity_id.replace('\n', '')
                activity_id = activity_id.strip()
                
                # Remove the quotation marks
                if '"' in activity_id:
                    activity_id = activity_id.replace('"', '')
                elif "'" in activity_id:
                    activity_id = activity_id.replace("'", "'")
            
                file.close()
                            
                return activity_id
            
        exit('activity_id was not found in ".lms/exercises.toml".')
    
    
    def get_project_link(self, activity_id: str):
        """
        Sends a get server request to get the project link using the activity_id. 
        """
        
        response = get(f'{self.server_link}/projects/get/{activity_id}')
        if response.status_code != 200:
            print('Project link is not found')
            exit(1)
        
        content = response.content
        data = loads(content.decode())
        
        return data['url']
    
    
    def download_test_file(self, project_link: str):
        """
        Downloads the test file using the project link.
        """
        
        response = get(project_link)
    
        if response.status_code == 200:
            return response.content
            
        else:
            print('Could\'t download the test file. Please check your \
                internet connection. If the problem persists, report to \
                the LMS team.')
            exit(1)
            
    
    def create_temp_test_file(self, content: bytes):
        """Creates a temporary test file and writes the content inside."""
        
        tmp_test_file = Path(self.temp_test_filename)
        tmp_test_file.touch()
        
        file = open(tmp_test_file, 'wb')
        file.write(content)
        file.close()
        
        return tmp_test_file
        
    
    def run_test_file_and_output_results(self):
        """Runs the test file and output results. This method assumes the test file exists."""
        
        results = run(['python3', '-m', self.test_runner, self.temp_test_filename], capture_output=True, text=True)
        if results.stdout:
            print(results.stdout)
        else:
            print(results.stderr)
            
        return results
    
            
    def delete_test_file(self, path: str | Path):
        """Deletes the test file. It assumes the test file exists."""
        remove(path)
        
        
    def get_grade(self, stdout: str):
        """
        This method inspects the standard output received from the 
        CompletedProcess and tries to find the grade.
        """
        
        output = stdout.split('\n')
        for line in output:
            if 'Grade' in line:
                grade = line.split(':')[1]
                grade = grade.strip()
                grade = float(grade[:-1])
        return grade
    
    
    def check(self):
        """
        Downloads the test file from the server, runs the test file, and
        output the results in the console.
        """
        
        print('Getting the activity id...\n')
        sleep(1)
        
        # Get activity id
        activity_id = self.get_activity_id()
        
        print('Connecting...\n')
        sleep(3)
        
        # Get project link
        project_link = self.get_project_link(activity_id)
        
        # Download the test file
        content = self.download_test_file(project_link)
        
        # Create the temporary test file
        path = self.create_temp_test_file(content)
        
        # Run the test file
        results = self.run_test_file_and_output_results()
        
        # Delete the temporary test file
        self.delete_test_file(path)
        
        return results
    
    
    def submit(self, commit_msg: str='Submitting.'):
        """
        Downloads the test file from the server, runs the test file,
        output the results in the console, submit the results to the
        server, and push the code to github.
        """
        
        print('Authorizing...\n')
        sleep(3)
        
        GL_SERVER = 'https://gitlab.wethinkco.de'
        GITLAB_TOKEN = environ.get('GL_TOKEN')
        
        if not GITLAB_TOKEN:
            print('Please set the GL_TOKEN env variable.')
            exit(1)
            
        gl = Gitlab(GL_SERVER, GITLAB_TOKEN)
        
        try:
            gl.auth()
        except gl_exc.GitlabAuthenticationError as err:
            print(err, 'Try using a correct private token.')
            exit(1)
            
        results = self.check()
        
        grade = self.get_grade(results.stdout)
        
        # Get username of the authenticated student
        user = gl.user.asdict()
        username = user['username']
        
        # Get activity id
        activity_id = self.get_activity_id()
        
        # Prepare payload
        payload = {
            'username': username,
            'grade': grade,
            'project_id': activity_id,
        }
        
        response = post(f'{self.server_link}/projects/submit', data=payload)
        if response.status_code != 200:
            print(f'Error: {response.status_code}',
                'We couldn\'t establish a connection with the server. \
                Please check your internet connection and try again.\n')
            exit()
            
        print('Submitted.\n')
        sleep(1)
        
        print('Trying to push to Gitlab...\n')
        sleep(3)
        
        system(f'git add . && git commit -m "{commit_msg}" && git push')
        
        print('Process completed successfully!')
        
        
    