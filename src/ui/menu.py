from . import menu_utils
import pandas as pd

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
def __inventoryMenu(inventory):
    menu_items = {
        '1: Add Cards to Inventory': __addCard,
        '2. Remove Cards from Inventory': __removeCard,
        '3. View Inventory': __displayAll,
        '4. Quit': None
    }
    title = 'Inventory Menu'
    __renderMenu(title, menu_items, inventory)

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

def __importFromJson(inventory):
    json_file = input("Enter path to JSON file you wish to import: ")
    print('\n\nLoading from JSON file')
    json_cards = pd.read_json(json_file)
    inventory.updateTable(json_cards)


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
    else:
        print('ERROR: Invalid response.')
        placeholder = input('')

def __displayAll(inventory):
    print('\n\nDisplaying all Cards')
    placeholder = input('Press any key to continue...\n>>')

# SEARCH MENU FUNCTIONS
def __searchSet(inventory):
    print('\n'*30)
    setname = input('Enter name of set to search by\n>>')
    # settype = input('Enter set type [\'CORE\',\'EXPANSION\',\'COMMANDER\']')
    try:
        set = inventory.searchBySet(setname)
        menu_utils.multiSearchResponseEval(set, setname)
    except Exception as e:
        print('ERROR: Program encountered exception: ', e)
        placeholder = input('')
        return

# TODO: Implement search by block functionality in db
def __searchBlock(inventory):
    print('\n'*30)
    blockname = input('Enter name of block to search by\n>>')
    print('\n\nSearching...')
    placeholder = input('Press any key to continue...\n>>')

def __searchName(inventory):
    print('\n'*30)
    cardname = input('Enter name of card to search by\n>>')
    try:
        cards = inventory.searchByName(cardname)
    except Exception as e:
        print('ERROR: Program encountered exception: ', e)
        placeholder = input('')
        return
    card = menu_utils.singleSearchResponseEval(cards)
    print(card)

def __searchMID(inventory):
    print('\n'*30)
    m_id = input('Enter multiverse id of card to search by\n>>')
    try:
        cards = inventory.searchByMID(m_id)
    except Exception as e:
        print('ERROR: Program encountered exception: ', e)
        placeholder = input('')
        return
    card = menu_utils.singleSearchResponseEval(cards)
    print(card)


# RENDERS MENU FOR SELECT MENU's
def __renderMenu(menu_title, menu_items, params):
    quit = False
    legal = False
    while not quit:
        print('\n'*30)
        print(menu_title)
        print('\n\nSelect and option:\n')
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
            print('ERROR: Invalid Input. Please try again')
            err = input('')
