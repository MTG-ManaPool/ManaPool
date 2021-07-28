# FUNCTION TO SELECT CARDS FROM THE LIST RETURNED BY DB
def searchResponseEval(cards, groupname, action):
    # NO CARDS FOUND
    if len(cards) == 0:
        print('No cards of that name found...')
        placeholder = input('Press any key to continue...\n')
        return None
    # CARDS WERE FOUND IN SET/BLOCK
    else:
        if action:
            print(f'\n\nResulting Cards from Search "{groupname}"\n\n')
            quit = False
            selected = []
            while not quit:
                for index, card in enumerate(cards): # https://realpython.com/python-enumerate/
                    print(index+1, '.  ',
                        'MID:', card['multiverse_ids'], ' ',
                        'Name:', card['name'], ' ',
                        'Mana:', card['mana_cost'], ' ',
                        'Type:', card['type_line'], ' ',
                        'Set:', card['set_name'], ' ',
                        'Rarity:', card['rarity'], ' '
                        )
                print('\n\n\n Select a card by selecting it\'s number in the list or type [Q] to quit')
                to_add = input('\n\n>')
                if to_add == 'Q' or to_add == 'q':
                    quit = True
                elif (int(to_add)-1) in range(len(cards)):
                    to_add = int(to_add)-1
                    selected.append(cards[to_add])
                    print(f'\n\n\nCurrent list of cards to {action}:\n\n')
                    for card in selected:
                        print(
                            'MID:', card['multiverse_ids'], ' ',
                            'Name:', card['name'], ' ',
                            'Mana:', card['mana_cost'], ' ',
                            'Type:', card['type_line'], ' ',
                            'Set:', card['set_name'], ' ',
                            'Rarity:', card['rarity'], ' '
                            )
                    placeholder = input('\n\n\nPress any key to continue...\n')
            return selected
        else:
            print(f'\n\nResulting Cards from Search "{groupname}"\n\n')
            for index, card in enumerate(cards): # https://realpython.com/python-enumerate/
                print(index+1, '.  ',
                    'MID:', card['multiverse_ids'], ' ',
                    'Name:', card['name'], ' ',
                    'Mana:', card['mana_cost'], ' ',
                    'Type:', card['type_line'], ' ',
                    'Set:', card['set_name'], ' ',
                    'Rarity:', card['rarity'], ' '
                    )
            placeholder = input('\n\n\nPress any key to continue...\n')
        return None