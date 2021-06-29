from pathlib import Path
import json
import os

def createUser(username):
    mode = 0o777
    # https://stackoverflow.com/questions/22230250/creating-files-folders-recursively-in-python
    new_user_folder_path = Path(os.getcwd() + os.path.join(f'/users/{username}')) # abs path
    if not os.path.exists(new_user_folder_path):   # create folders if not exists
        os.mkdir(new_user_folder_path, mode)

    new_user_file_path = os.path.join(new_user_folder_path, f'/{username}.json')
    # new_user_file_path = f'./users/{username}/{username}.json'
    exists = True
    while exists:
        try: 
            new_user_obj = {
                'userName': username
            }
            with open(new_user_file_path, 'x') as new_user_file: # open file in 'create' mode/will be db write later
                json.dump(new_user_file, new_user_obj)
            new_user_file.close()
            print(new_user_obj)
            return new_user_obj
        except FileExistsError:
            print('\nThis username already exists!')
            print('\nPlease enter username:\n\n')
            username = input('>')
            continue


def readUser(path):
    with open(path) as json_file:
        user = json.load(json_file) # pull in json as python dict/will be db read later
    json_file.close()
    return user