from os import path

def get_activity_id():
    exercises_path = '.lms/exercises.toml'
    if not (path.exists(exercises_path) and path.isfile(exercises_path)):
        exit('Could\'t find \'.lms/exercises.toml\'.')
        
    exercises_file = open(exercises_path, 'r')
    info = exercises_file.readlines()
    for line in info:
        if 'activity_id' in line:
            activity_id = line.split('=')[1]
            activity_id = activity_id.replace('\n', '')
            activity_id = activity_id.strip()
            
            if '"' in activity_id:
                activity_id = activity_id.replace('"', '')
            elif "'" in activity_id:
                activity_id = activity_id.replace("'", "'")
                
    return activity_id
