from . import menu_utils
import pandas as pd

# MAIN MENU
def Menu(inventory):
    menu_items = {
        '1. Import Inventory from a JSON file': __importFromJson,
        '2. Export Inventory to a JSON file': __exportToJson,
        '3. Access Inventory': __inventoryMenu,
        '4. Search for Cards': __searchMenu,
        '5. Quit': None
    }
    title = 'Welcome to ManaPool'
    __renderMenu(title, menu_items, inventory)


# MAIN MENU FUNCTIONS
# MENU FOR INVENTORY INTERFACE
def __inventoryMenu(inventory):
    menu_items = {
        '1: Add Cards to Inventory': __addCardMenu,
        '2. Remove Cards from Inventory': __removeCardMenu,
        '3. View Inventory': __displayAll,
        '4. Quit': None
    }
    title = 'Inventory Menu'
    __renderMenu(title, menu_items, inventory)

# MENU FOR DATABASE INTERFACE
def __searchMenu(inventory):
    menu_items = {
        '1: Search for Cards by Set': __searchSet,
        '2. Search for Cards by Block': __searchBlock,
        '3. Search for Cards by Name': __searchName,
        '4. Search for Cards by Multiverse ID': __searchMID,
        '5. Quit': None
    }
    title = 'Search Menu'
    __renderMenu(title, menu_items, inventory)

# IMPORTS CURRENT INVENTORY FROM AN EXPORTED JSON FILE
def __importFromJson(inventory):
    json_file = input("Enter path to JSON file you wish to import: ")
    print('\n\nLoading from JSON file')
    json_cards = pd.read_json(json_file)
    inventory.updateTable(json_cards)


# EXPORTS CURRENT INVENTORY TO A JSON FILE
# THIS FILE CAN BE IMPORTED LATER TO SHARE AN INVENTORY ACROSS DEVICES
def __exportToJson(inventory):
    print('\n\nExporting to JSON file')
    dst = input("Please enter the file name you wish the exported cards to be in: ")
    if not dst.endswith('.json'):
                dst += '.json'
    inventory.exportJSON(dst)
    # placeholder = input('Press any key to continue...\n>>')


# INVENTORY MENU FUNCTIONS
def __addCard(inventory):
    print('\n'*30)
    print('*** Card Add ***')
    print('Is this card a token or emblem? [Y/N]')
    reply = input('\n>')
    if reply.lower() == 'y':
        print('Please enter the name of the card.')
        name = input('\n>')
        cards = inventory.searchByName(name)
        card = menu_utils.singleSearchResponseEval(cards)
        if card:
            print('Adding card to inventory')
            inventory.addCard(card)
        else:
            print('\n\nReturning to menu')
            placeholder = input('Press any key to continue...\n>>')
    elif reply.lower() == 'n':
        print('Please enter ID of the card [Front Face ID if double sided].')
        id = input('\n>')
        cards = inventory.searchByMID(id)
        card = menu_utils.singleSearchResponseEval(cards)
        if card:
            print('Adding card to inventory')
            inventory.addCard(card)
        else:
            print('\n\nReturning to menu')
            placeholder = input('Press any key to continue...\n>>')
    else:
        print('\n\nERROR: Invalid response.')
        placeholder = input('')


def __removeCard(inventory):
    print('\n'*30)
    print('*** Card Remove ***')
    print('Is this card a token or emblem? [Y/N]')
    reply = input('\n>')
    if reply.lower() == 'y':
        print('Please enter the name of the card.')
        name = input('\n>')
        cards = inventory.searchByName(name)
        card = menu_utils.singleSearchResponseEval(cards)
        if card:
            print('Removing card from inventory')
            inventory.removeCard(card)
        else:
            print('\n\nReturning to menu')
            placeholder = input('Press any key to continue...\n>>')
    elif reply.lower() == 'n':
        print('Please enter ID of the card [Front Face ID if double sided].')
        id = input('\n>')
        cards = inventory.searchByMID(id)
        card = menu_utils.singleSearchResponseEval(cards)
        if card:
            print('Removing card from inventory')
            inventory.removeCard(card)
        else:
            print('\n\nReturning to menu')
            placeholder = input('Press any key to continue...\n>>')

# INVENTORY MENU FUNCTIONS
# MENU TO INITIATE ADDING CARDS TO INVENTORY
def __addCardMenu(inventory):
    print('\n' * 50)
    menu_items = {
        '1: Search for Cards by Set': __searchSet,
        '2. Search for Cards by Block': __searchBlock,
        '3. Search for Cards by Name': __searchName,
        '4. Search for Cards by Multiverse ID': __searchMID,
        '5. Quit': None
    }
    title = 'Select Method to Search for Cards to Add'
    __renderMenu(title, menu_items, [inventory, 'add'])

# MENU TO INITIATE REMOVING CARDS TO INVENTORY
def __removeCardMenu(inventory):
    print('\n' * 50)
    menu_items = {
        '1: Search for Cards by Set': __searchSet,
        '2. Search for Cards by Block': __searchBlock,
        '3. Search for Cards by Name': __searchName,
        '4. Search for Cards by Multiverse ID': __searchMID,
        '5. Quit': None
    }
    title = 'Select Method to Search for Cards to Remove'
    __renderMenu(title, menu_items, [inventory, 'remove'])

# MENU TO INQUIRE TYPES OF CARDS TO ADD/REMOVE FROM INVENTORY
def __selectCardType(inventory, selected_cards, action):
    if action == 'add':
        action = __addCards
    elif action == 'remove':
        action = __removeCards
    else:
        raise('No action specified') 

    menu_items = {
        '1: full_art': action,
        '2. textless': action,
        '3. foil': action,
        '4. nonfoil': action,
        '5. oversized': action,
        '6. promo': action,
        '7. Quit': None
    }
    print('\n\nSelect Card type\n')
    for action in menu_items.keys():
        print(action)
    reply = input('\n>')
    for index, key in enumerate(menu_items.keys()): # https://realpython.com/python-enumerate/
        if reply == str(index+1):
            if menu_items[key] == None:
                break
            else:
                index, cardtype = key.split()
                menu_items[key](inventory, selected_cards, cardtype)
                break

# WRAPPER FUNCTION TO DISPLAY ALL OWNED CARDS
def __displayAll(inventory):
    print('\n\nDisplaying all Cards...\n')
    inventory.displayInventory()
    placeholder = input('\n\nPress any key to continue...\n')

# WRAPPER FUNCTION TO ADD CARDS TO INVENTORY
def __addCards(inventory, cards, cardtype):
    print('\nAdding Cards...\n\n')
    for card in cards:
        print(
            'MID:', card['multiverse_ids'], ' ',
            'Name:', card['name'], ' ',
            'Mana:', card['mana_cost'], ' ',
            'Type:', card['type_line'], ' ',
            'Set:', card['set_name'], ' ',
            'Rarity:', card['rarity'], ' '
            )
    inventory.addCardToInventory(cards, cardtype)
    print('\nCards added.')
    placeholder = input('Press any key to continue...\n')

# WRAPPER FUNCTION TO REMOVE CARDS FROM INVENTORY
def __removeCards(inventory, cards, cardtype):
    print('\nRemoving Cards...\n\n')
    for card in cards:
        print(
            'MID:', card['multiverse_ids'], ' ',
            'Name:', card['name'], ' ',
            'Mana:', card['mana_cost'], ' ',
            'Type:', card['type_line'], ' ',
            'Set:', card['set_name'], ' ',
            'Rarity:', card['rarity'], ' '
            )
    inventory.removeCardFromInventory(cards, cardtype)
    print('\nCards removed.')
    placeholder = input('Press any key to continue...\n')


# SEARCH MENU FUNCTIONS
# TODO: Implement search by block functionality in db
def __searchBlock(params):
    print('\n' * 50)
    blockname = input('Enter name of block to search by\n\n>')
    print('\n\nSearching...')
    placeholder = input('Press any key to continue...\n')


def __searchSet(params):
    print('\n' * 50)
    setname = input('Enter name of set to search by\n\n>')
    if isinstance(params, list):
        inventory = params[0]
        action = params[1]
    else:
        inventory = params
        action = None

    try:
        set = inventory.searchBySet(setname)
        selected_cards = menu_utils.searchResponseEval(set, setname, action)
        if action and selected_cards:
            __selectCardType(inventory, selected_cards, action)
    except Exception as e:
        print('ERROR: Program encountered exception: ', e)
        placeholder = input('')
        
def __searchName(params):
    print('\n' * 50)
    cardname = input('Enter name of card to search by\n\n>')
    if isinstance(params, list):
        inventory = params[0]
        action = params[1]
    else:
        inventory = params
        action = None

    try:
        cards = inventory.searchByName(cardname)
        selected_cards = menu_utils.searchResponseEval(cards, cardname, action)
        if action and selected_cards:
            __selectCardType(inventory, selected_cards, action)
    except Exception as e:
        print('ERROR: Program encountered exception: ', e)
        placeholder = input('')

def __searchMID(params):
    print('\n' * 50)
    m_id = input('Enter multiverse id of card to search by\n\n>')
    if isinstance(params, list):
        inventory = params[0]
        action = params[1]
    else:
        inventory = params
        action = None

    try:
        cards = inventory.searchByMID(m_id)
        selected_cards = menu_utils.searchResponseEval(cards, m_id, action)
        if action and selected_cards:
            __selectCardType(inventory, selected_cards, action)
    except Exception as e:
        print('ERROR: Invalid input.')
        placeholder = input('')


# RENDERS MENU FOR SELECT MENU's
# MENU's CANNOT RETURN VALUES, THEREFORE FUNCTIONS CALLED BY MENU's ALSO CANNOT RETURN VALUES
def __renderMenu(menu_title, menu_items, params):
    quit = False
    while not quit:
        legal = False
        print('\n' * 50)
        print(menu_title, '\n\n')
        for key in menu_items.keys():
            print(key)
        reply = input('\n>')
        for index, key in enumerate(menu_items.keys()): # https://realpython.com/python-enumerate/
            if reply == str(index+1):
                if menu_items[key] == None:
                    legal = True
                    quit = True
                    break
                else:
                    legal = True
                    menu_items[key](params)
                    break
        if not legal:
            print('\n\nERROR: Invalid Input. Please try again')
            err = input('')
    