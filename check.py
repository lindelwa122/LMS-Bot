import os
import sys
import gitlab
import gitlab.exceptions

gl_server = os.environ.get('GL_SERVER', 'https://gitlab.com')
GITLAB_TOKEN = os.environ.get('GL_TOKEN', 'ueWm2ErbwdtygwJA44sE')



if not GITLAB_TOKEN:
    print("Please set the GL_TOKEN env variable.")
    sys.exit(1)

print(gl_server)

gl = gitlab.Gitlab()
gitignore_templates = gl.gitignores.get('Python')



# print(gitignore_templates.content)

GITLAB_SERVER = os.environ.get('GL_SERVER', 'https://gitlab.com')
# https://gitlab.com/gitlab-de/use-cases/
GROUP_ID = os.environ.get('GL_GROUP_ID', 16058698)

gl = gitlab.Gitlab(GITLAB_SERVER, private_token=GITLAB_TOKEN)

try:
    res = gl.auth()
    print(res)
    print(gl.user.asdict())
    exit('============================')
except gitlab.exceptions.GitlabAuthenticationError as err:
    print(err, 'Try using a correct private token.')
