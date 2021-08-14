import os 

 # https://www.tutorialspoint.com/how-to-clear-screen-in-python
def clear_screen():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # for windows platfrom
        _ = os.system('cls')
