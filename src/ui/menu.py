from consolemenu import * # https://pypi.org/project/console-menu/
from consolemenu.items import *
from . import menu_utils

def menu(inventory):

    # DECLARE MENU's
    menu = ConsoleMenu('Main Menu', 'ManaPool')
    inventory_menu = ConsoleMenu('Inventory Menu', 'ManaPool')
    search_menu = ConsoleMenu('Inventory Search Menu', 'ManaPool')

    # DECLARE MENU ITEMS
    main_import_from_json = FunctionItem('Import from Json File', __importFromJson, [inventory])
    main_export_to_json = FunctionItem('Export to Json FILE', __exportToJson, [inventory])

    inv_add_card = FunctionItem('Add Card to Inventory', __addCard, [inventory])
    inv_remove_card = FunctionItem('Remove Card from Inventory', __removeCard, [inventory])

    inv_set_search = FunctionItem('Search by Set', __searchSet, [inventory])
    inv_block_search = FunctionItem('Search by Block', __searchBlock, [inventory])
    inv_name_search = FunctionItem('Search by Name', __searchName, [inventory]) 
    inv_id_search = FunctionItem('Search by Multiverse ID', __searchMID, [inventory]) 
    
    # CAST SUBMENUS
    inventory_menu_item = SubmenuItem('Inventory', inventory_menu, menu)
    search_menu_item = SubmenuItem('Search Inventory for Cards', search_menu, inventory_menu)

    # APPEND MENU ITEMS
    menu.append_item(main_import_from_json)
    menu.append_item(main_export_to_json)
    menu.append_item(inventory_menu_item)

    inventory_menu.append_item(inv_add_card)
    inventory_menu.append_item(inv_remove_card)
    inventory_menu.append_item(search_menu_item)

    search_menu.append_item(inv_set_search)
    search_menu.append_item(inv_block_search)
    search_menu.append_item(inv_name_search)
    search_menu.append_item(inv_id_search)

    menu.show()


# IMPORTS AND EXPORTS
def __importFromJson(inventory):
    print('Loading from JSON file')
    placeholder = input('Press any key to continue...\n>>')

def __exportToJson(inventory):
    print('Exporting to JSON file')
    placeholder = input('Press any key to continue...\n>>')


def __addCard(inventory):
    print('Adding card to inventory')
    print('Is this card a token or emblem? [Y/N]')
    res = input('\n>')
    if res == 'Y':
        print('Please enter the name of the card.')
        name = input('\n>')
        cards = inventory.searchByName(name)
        card = menu_utils.cardSearchResponseEval(cards)
        if card:
            print('Adding card to inventory')
            inventory.addCard(card)
        else:
            print('Returning to menu')
            placeholder = input('Press any key to continue...\n>>')
    elif res == 'N':
        print('Please enter ID of the card [Front Face ID if double sided].')
        id = input('\n>')
        cards = inventory.searchByID(id)
        card = menu_utils.cardSearchResponseEval(cards)
        if card:
            print('Adding card to inventory')
            inventory.addCard(card)
        else:
            print('Returning to menu')
            placeholder = input('Press any key to continue...\n>>')
    else:
        print('ERROR: Invalid response.')
        placeholder = input('Press any key to continue...\n>>')


def __removeCard(inventory):
    print('Removing card from Inventory')
    print('Is this card a token or emblem? [Y/N]')
    res = input('\n>')
    if res == 'Y':
        print('Please enter the name of the card.')
        name = input('\n>')
        cards = inventory.searchByName(name)
        card = menu_utils.cardSearchResponseEval(cards)
        if card:
            print('Removing card from inventory')
            inventory.removeCard(card)
        else:
            print('Returning to menu')
            placeholder = input('Press any key to continue...\n>>')
    elif res == 'N':
        print('Please enter ID of the card [Front Face ID if double sided].')
        id = input('\n>')
        cards = inventory.searchByID(id)
        card = menu_utils.cardSearchResponseEval(cards)
        if card:
            print('Removing card from inventory')
            inventory.removeCard(card)
        else:
            print('Returning to menu')
            placeholder = input('Press any key to continue...\n>>')
    else:
        print('ERROR: Invalid response.')
        placeholder = input('Press any key to continue...\n>>')



# INVENTORY SEARCH FUNCTIONS
def __searchSet(inventory):
    setname = input('Enter name of set to search by\n>>')
    # settype = input('Enter set type [\'CORE\',\'EXPANSION\',\'COMMANDER\']')
    placeholder = input('Press any key to continue...\n>>')

def __searchBlock(inventory):
    blockname = input('Enter name of block to search by\n>>')
    placeholder = input('Press any key to continue...\n>>')

def __searchName(inventory):
    cardname = input('Enter name of card to search by\n>>')
    placeholder = input('Press any key to continue...\n>>')

def __searchMID(inventory):
    m_id = input('Enter multiverse id of card to search by\n>>')
    placeholder = input('Press any key to continue...\n>>')