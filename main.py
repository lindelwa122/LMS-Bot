from argparse import ArgumentParser
from lms import LMS


def main():
    parser = ArgumentParser(prog='Learning Management System (LMS)',
        description='The aim of this program is to create a management \
            system that runs tests that are stored on the server \
            somewhere and output results on the user console. When you use \
            the submit commands it also submit the grade of the \
            assignment to the server.',
    )
    
    parser.add_argument(
        'instruction',
        choices=['check', 'submit'],
        help='Specifies if the program must check your project or submit it.'
    )
    
    parser.add_argument(
        '-m',
        '--message',
        help='Specifies the commit message before pushing to Gitlab.',
        default='Submitting.'
    )
    
    parser.add_argument(
        '-r',
        '--runner',
        help='Specifies the test runner. By default colorful-test is used.',
        default='colorful_test'
    )
    
    parser.add_argument(
        '-f',
        '--filename',
        help='Specifies the temporary test filename to use.',
        default='test_temp_file.py'
    )
    
    parser.add_argument(
        '-p',
        '--path',
        help='Specifies the path where to find the exercises.toml file.',
        default='.lms/exercises.toml'
    )
    
    # Get arguments
    args = parser.parse_args()
    
    # Create an LMS object
    lms = LMS(
        'https://lms-api-l0ua.onrender.com',
        args.path,
        args.filename,
        args.runner,
    )
    
    match args.instruction:
        case 'check':
            lms.check()
            
        case 'submit':
            lms.submit(args.message)
            
        case _:
            print('Unrecognized instruction. Expected "check" or "submit"')
    
main()