
import pandas as pd
import numpy as np
from ui.menu_utils import clear_screen
# CLASS FOR CACHING A TEMPORARY LIST TO USE FOR ADDING/REMOVING FROM INVENTORY
# ALSO FOR USE IN CREATING PURCHASE ORDERS TO SUBMIT TO WEB
class CardList():
    def __init__ (self):
        self.cardlist = None

    # FUNCTION TO SELECT CARDS FROM THE LIST RETURNED BY DB
    def createFromDBResponse(self, cards, groupname, action):
        # NO CARDS FOUND
        if cards.empty:
            print('\n\nNo cards found...\n')
            self.cardlist = pd.DataFrame(columns=np.append(cards.columns.values, 'variant'), dtype=object)
            placeholder = input('Press any key to continue...\n')
            return self.cardlist
        # CARDS WERE FOUND IN SET/BLOCK
        else:
            self.cardlist = pd.DataFrame(columns=np.append(cards.columns.values, 'variant'), dtype=object)
            if action:
                quit = False
                finish = False
                count = 0
                while not quit and not finish:
                    clear_screen()
                    print(f'\n\nResulting Cards from Search "{groupname}"\n\n')
                    for index, card in cards.iterrows():
                        print(index+1, '.  ',
                            'MID:', card['multiverse_ids'], ' ',
                            'Name:', card['name'], ' ',
                            'Mana:', card['mana_cost'], ' ',
                            'Type:', card['type_line'], ' ',
                            'Set:', card['set_name'], ' ',
                            'Rarity:', card['rarity'], ' ',
                            'Foils:', card['foil'], ' ',
                            'Nonfoils:', card['nonfoil'], ' '
                            )
                    print('\n\n\nSelect a card by selecting it\'s number in the list or type [F] to finish or [Q] to quit\n\n')
                    reply = input('>')
                    if reply == 'Q' or reply == 'q':
                        quit = True
                    elif reply == 'F' or reply == 'f':
                        finish = True
                    elif (int(reply)-1) in range(len(cards)):
                        reply = int(reply)-1
                        variant = self.__selectVariant(cards.iloc[reply], action)
                        if variant == None:
                            continue
                        self.cardlist = pd.concat([self.cardlist, cards.loc[[reply]]], ignore_index=True)
                        self.cardlist.loc[count, "variant"] = variant
                        clear_screen()
                        print(f'\n\n\nCurrent list of cards to {action}:\n\n')
                        for index, card in self.cardlist.iterrows():
                            print(
                                'MID:', card['multiverse_ids'], ' ',
                                'Name:', card['name'], ' ',
                                'Mana:', card['mana_cost'], ' ',
                                'Type:', card['type_line'], ' ',
                                'Set:', card['set_name'], ' ',
                                'Rarity:', card['rarity'], ' '
                                'Variant:', card['variant'], ' '
                                )
                        placeholder = input('\n\n\nPress any key to continue...\n')
                        count += 1
                    else:
                        print('\n\nERROR: Invalid Entry. Pleasy try again.\n\n')
                        placeholder = input('')
                if quit == True:
                    # clear all data from cardlist: https://stackoverflow.com/questions/39173992/drop-all-data-in-a-pandas-dataframe/39174024
                    self.cardlist.iloc[0:0]
                    return self.cardlist
                else:
                    return self.cardlist
            else:
                print(f'\n\nResulting Cards from Search "{groupname}"\n\n')
                for index, card in cards.iterrows():
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
    
    def modifyCardList(self):
        # CARD LIST EMPTY
        if self.cardlist.empty:
            print('Card list currently empty...')
            placeholder = input('Press any key to continue...\n')
            return self.cardlist
        # CARDS FOUND IN CARDLIST
        else:
            print(f'\n\nCurrent Stored Card List\n\n')
            quit = False
            finish = False
            while not finish:
                for index, card in self.cardlist.iterrows():
                    print(index+1, '.  ',
                        'MID:', card['multiverse_ids'], ' ',
                        'Name:', card['name'], ' ',
                        'Mana:', card['mana_cost'], ' ',
                        'Type:', card['type_line'], ' ',
                        'Set:', card['set_name'], ' ',
                        'Rarity:', card['rarity'], ' ',
                        'Variant:', card['variant'], ' '
                        )
                print('\n\n\nRemove a card by selecting it\'s number in the list or type [F] to finish\n')
                print('NOTE: CHANGES MADE HERE CANNOT BE REVERSED!!\n\n')
                reply = input('>')
                if reply == 'F' or reply == 'f':
                    finish = True
                elif (int(reply)-1) in range(len(self.cardlist)):
                    reply = int(reply)-1
                    removed = self.cardlist.pop(self.cardlist[reply])+1
                    print(f'\nRemoved Card #{removed}')
                    placeholder = input('')
                else:
                    print('\n\nERROR: Invalid Entry. Pleasy try again.\n\n')
                    placeholder = input('')
            else:
                return self.cardlist.copy()
    
    # MENU TO INQUIRE TYPE OF CARDS TO ADD/REMOVE FROM INVENTORY
    def __selectVariant(self, card, action):
        variant = None
        menu_items = {
            '1. Foil': 'foil',
            '2. Nonfoil (normal card)': 'nonfoil',
            '3. Quit': None
        }
        print(f"\n\nSelect Card type for {card['name']} to {action}\n")
        for action in menu_items.keys():
            print(action)
        reply = input('\n>')
        for index, key in enumerate(menu_items.keys()): # https://realpython.com/python-enumerate/
            if reply == str(index+1):
                if menu_items[key] == None:
                    break
                else:
                    variant = menu_items[key]
                    break
        return variant