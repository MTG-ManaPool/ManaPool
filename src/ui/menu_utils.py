
def singleSearchResponseEval(cards):
    # NO CARDS FOUND
    if len(cards) == 0:
        print('No cards of that name found...')
        placeholder = input('Press any key to continue...\n>>')
    # EXACTLY ONE CARD FOUND
    elif len(cards) == 1:
        print(cards[0])
        print('Select Card? [Y/N]')
        res = input('\n>')
        if res == 'Y':
            return cards[0]
        elif res == 'N':
            return None
        else:
            print('ERROR: Invalid response.')
            return None
    # MULTIPLE CARDS FOUND
    else:
        print('More than one card found for search\n\n')
        for index, card in enumerate(cards): # https://realpython.com/python-enumerate/
            print(index+1, '.  ',
                  'MID:', card['MULTIVERSE ID'], ' ',
                  'Name:', card['NAME'], ' ',
                  'Mana:', card['MANA COST'], ' ',
                  'Type:', card['CARD TYPES'], ' ',
                  'Set:', card['SET'], ' ',
                  'Rarity:', card['RARITY'], ' '
                 )
            print('\n')

        print('Select card to choose or enter [N] to return to menu')
        res = input('\n>')
        if res == 'N' or res == 'n':
            print('Returning to menu')
            return None
        elif isinstance(res, str): # https://www.geeksforgeeks.org/python-check-if-a-variable-is-string/
            print('ERROR: Invalid response.')
            placeholder = input('Press any key to continue...\n>>')
        elif int(res) in range(1,len(cards)):
            card = cards[int(res)-1]
            print(card)
            placeholder = input('Press any key to continue...\n>>')
            return card

def multiSearchResponseEval(cards, groupname):
    # NO CARDS FOUND
    if len(cards) == 0:
        print('No cards of that name found...')
        placeholder = input('Press any key to continue...\n>>')
    # CARDS WERE FOUND IN SET/BLOCK
    else:
        print(f'Found Cards in {groupname}\n\n')
        for index, card in enumerate(cards): # https://realpython.com/python-enumerate/
            print(index+1, '.  ',
                  'MID:', card['MULTIVERSE ID'], ' ',
                  'Name:', card['NAME'], ' ',
                  'Mana:', card['MANA COST'], ' ',
                  'Type:', card['CARD TYPES'], ' ',
                  'Set:', card['SET'], ' ',
                  'Rarity:', card['RARITY'], ' '
                 )
            print('\n')
        print('\n\n')
        placeholder = input('Press any key to continue...\n>>')