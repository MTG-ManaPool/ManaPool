
def cardSearchResponseEval(cards):
    # No cards found
    if len(cards) == 0:
        print('No cards of that name found...')
        placeholder = input('Press any key to continue...\n>>')
    # Exactly one card found
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
    # Multiple Cards found
    else:
        print('More than one card found for search')
        for index, card in cards:
            print(index,'.  ', card)
            print('\n\n')
        print('Select card to choose or enter [N] to return to menu')
        res = input('\n>')
        try:
            if res == 'N':
                print('Returning to menu')
                return None
            elif int(res) in range(len(cards)):
                return card[int(res)]
                return None
            else:
                print('ERROR: Invalid response.')
        except Exception:
            print('ERROR: Invalid response.')
            return None