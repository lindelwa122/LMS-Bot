from setuptools import setup, find_packages

setup(
    name='lms-grader',
    version='0.0.1',
    packages=find_packages(),
    install_requirements=[
        'certifi',
        'charset-normalizer',
        'colorful-test',
        'idna',
        'python-gitlab',
        'requests',
        'requests-toolbelt',
        'urllib3',
    ],
    entry_points={
        'console_scripts': [
            'lms-grader=lms.grader:main',
        ]
    },
    description="A Learning Management System Grader",
    author="Nqabenhle Mlaba",
    author_email="nqabenhlemlaba22@gmail.com",
)