from user.user import createUser
from user.user import readUser

def login():
    print('Welcome to ManaPool, your multitool tracking your current Magic The Gathering inventory!\n')
    print('Please enter your username\n')
    username_in = input('>')

    path = f'./data/users/{username_in}/{username_in}.json'
    repeat_entry = True
    user = None

    while repeat_entry:
        try:
            return readUser(path)
        except FileNotFoundError: # local user DNE
            legal = False
            print('I\'m sorry, that use does not exist\n\nWould you like to create this user? [Y/N]')
            while not legal:    # loop to validate legal text answer in new user prompt loop
                ans = input('>')
                if ans != 'Y' and ans != 'N': # w
                    print('\nPlease answer with [Y/N]')
                    continue
                elif ans == 'N':                                 # exit program
                    print('\n\n********* Goodbye *********\n\n') 
                    legal = True
                    repeat_entry = False
                else:                                            # create new user
                    legal = True
                    repeat_entry = False
                    user = createUser(username_in)
                    continue
        return user