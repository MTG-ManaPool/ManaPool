
# CLASS FOR CACHING A TEMPORARY LIST TO USE FOR ADDING/REMOVING FROM INVENTORY
# ALSO FOR USE IN CREATING PURCHASE ORDERS TO SUBMIT TO WEB
class CardList():
    def __init__ (self):
        cardlist = None

    # FUNCTION TO SELECT CARDS FROM THE LIST RETURNED BY DB
    def createFromDBResponse(self, cards, groupname, action):
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
                finish = False
                selected = []
                while not quit and not finish:
                    for index, card in enumerate(cards): # https://realpython.com/python-enumerate/
                        print(index+1, '.  ',
                            'MID:', card['multiverse_ids'], ' ',
                            'Name:', card['name'], ' ',
                            'Mana:', card['mana_cost'], ' ',
                            'Type:', card['type_line'], ' ',
                            'Set:', card['set_name'], ' ',
                            'Rarity:', card['rarity'], ' '
                            )
                    print('\n\n\nSelect a card by selecting it\'s number in the list or type [F] to finish or [Q] to quit\n\n')
                    reply = input('>')
                    if reply == 'Q' or reply == 'q':
                        quit = True
                    elif reply == 'F' or reply == 'f':
                        finish = True
                    elif (int(reply)-1) in range(len(cards)):
                        reply = int(reply)-1
                        selected.append(cards[reply])
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
                    else:
                        print('\n\nERROR: Invalid Entry. Pleasy try again.\n\n')
                        placeholder = input('')
                if quit == True:
                    return None
                else:
                    self.cardlist = selected
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
    
    def modifyCardList(self):
        # CARD LIST EMPTY
        if len(self.cardlist) == 0:
            print('Card list currently empty...')
            placeholder = input('Press any key to continue...\n')
            return None
        # CARDS FOUND IN CARDLIST
        else:
            print(f'\n\nCurrent Stored Card List\n\n')
            quit = False
            finish = False
            while not quit or not finish:
                for index, card in enumerate(self.cardlist): # https://realpython.com/python-enumerate/
                    print(index+1, '.  ',
                        'MID:', card['multiverse_ids'], ' ',
                        'Name:', card['name'], ' ',
                        'Mana:', card['mana_cost'], ' ',
                        'Type:', card['type_line'], ' ',
                        'Set:', card['set_name'], ' ',
                        'Rarity:', card['rarity'], ' '
                        )
                print('\n\n\nRemove a card by selecting it\'s number in the list or type [F] to finish or [Q] to quit\n\n')
                print('')
                reply = input('>')
                if reply == 'Q' or reply == 'q':
                    quit = True
                elif reply == 'F' or reply == 'f':
                    finish = True
                elif (int(reply)-1) in range(len(self.cardlist)):
                    reply = int(reply)-1
                    removed = self.cardlist.pop(self.cardlist[reply])+1
                    print(f'\nRemoved Card #{removed}')
                    placeholder = input('')
                else:
                    print('\n\nERROR: Invalid Entry. Pleasy try again.\n\n')
                    placeholder = input('')
                    
            if quit == True:
                return None
            else:
                return self.cardlist.copy()
            return None
        
        




# # FUNCTION TO SELECT CARDS FROM THE LIST RETURNED BY DB
# def searchResponseEval(cards, groupname, action):
#     # NO CARDS FOUND
#     if len(cards) == 0:
#         print('No cards of that name found...')
#         placeholder = input('Press any key to continue...\n')
#         return None
#     # CARDS WERE FOUND IN SET/BLOCK
#     else:
#         if action:
#             print(f'\n\nResulting Cards from Search "{groupname}"\n\n')
#             quit = False
#             selected = []
#             while not quit:
#                 for index, card in enumerate(cards): # https://realpython.com/python-enumerate/
#                     print(index+1, '.  ',
#                         'MID:', card['multiverse_ids'], ' ',
#                         'Name:', card['name'], ' ',
#                         'Mana:', card['mana_cost'], ' ',
#                         'Type:', card['type_line'], ' ',
#                         'Set:', card['set_name'], ' ',
#                         'Rarity:', card['rarity'], ' '
#                         )
#                 print('\n\n\n Select a card by selecting it\'s number in the list or type [Q] to quit')
#                 reply = input('\n\n>')
#                 if reply == 'Q' or reply == 'q':
#                     quit = True
#                 elif (int(reply)-1) in range(len(cards)):
#                     reply = int(reply)-1
#                     selected.append(cards[reply])
#                     print(f'\n\n\nCurrent list of cards to {action}:\n\n')
#                     for card in selected:
#                         print(
#                             'MID:', card['multiverse_ids'], ' ',
#                             'Name:', card['name'], ' ',
#                             'Mana:', card['mana_cost'], ' ',
#                             'Type:', card['type_line'], ' ',
#                             'Set:', card['set_name'], ' ',
#                             'Rarity:', card['rarity'], ' '
#                             )
#                     placeholder = input('\n\n\nPress any key to continue...\n')
#             return selected
#         else:
#             print(f'\n\nResulting Cards from Search "{groupname}"\n\n')
#             for index, card in enumerate(cards): # https://realpython.com/python-enumerate/
#                 print(index+1, '.  ',
#                     'MID:', card['multiverse_ids'], ' ',
#                     'Name:', card['name'], ' ',
#                     'Mana:', card['mana_cost'], ' ',
#                     'Type:', card['type_line'], ' ',
#                     'Set:', card['set_name'], ' ',
#                     'Rarity:', card['rarity'], ' '
#                     )
#             placeholder = input('\n\n\nPress any key to continue...\n')
#         return None