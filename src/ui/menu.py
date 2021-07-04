from consolemenu import * # https://pypi.org/project/console-menu/
from consolemenu.items import *

def menu(scryfall, inventory):

    # EXAMPLES
    # Menu items
    # MenuItem is the base class for all items, it doesn't do anything when selected
    # menu_item = MenuItem('Menu Item')
    # A FunctionItem runs a Python function when selected
    # function_item = FunctionItem('Call a Python function', input, ['Enter an input'])
    # A CommandItem runs a console command
    # command_item = CommandItem('Run a console command',  'touch hello.txt')
    # A SubmenuItem lets you add a menu (the search_menu above, for example)
    # as a submenu of another menu
    # submenu_item = SubmenuItem('Search for Cards', search_menu, menu) # (menu name, sub menu, parent menu)
    # Finally, we call show to show the menu and allow the user to interact
    # menu.show()

    # MAIN MENU
    menu = ConsoleMenu('Main Menu', 'ManaPool')

    # IMPORT AND EXPORT MENU ITEMS
    import_from_json = FunctionItem('Import from Json File', _importFromJson, [inventory])
    export_to_json = FunctionItem('Export to Json FILE', _exportToJson, [inventory])

    # INVENTORY MENU
    inventory_menu = ConsoleMenu('Inventory Menu', 'ManaPool')
    inv_set_search = FunctionItem('Search by Set', _invSearchSet, [inventory])
    inv_block_search = FunctionItem('Search by Block', _invSearchBlock, [inventory])
    inv_name_search = FunctionItem('Search by Name', _invSearchName, [inventory]) 
    inv_id_search = FunctionItem('Search by Multiverse ID', _invSearchMID, [inventory]) 

    inventory_menu.append_item(inv_set_search)
    inventory_menu.append_item(inv_block_search)
    inventory_menu.append_item(inv_name_search)
    inventory_menu.append_item(inv_id_search)

    # SCRYFALL SEARCH MENU
    search_menu = ConsoleMenu('Search Menu', 'ManaPool')
    set_search = FunctionItem('Search by Set', _scrySearchSet, [scryfall])
    block_search = FunctionItem('Search by Block', _scrySearchBlock, [scryfall])
    name_search = FunctionItem('Search by Name', _scrySearchName, [scryfall]) 
    id_search = FunctionItem('Search by Multiverse ID', _scrySearchMID, [scryfall]) 

    search_menu.append_item(set_search)
    search_menu.append_item(block_search)
    search_menu.append_item(name_search)
    search_menu.append_item(id_search)

    # CAST SUBMENUS
    inventory_menu_item = SubmenuItem('Search Inventory for Cards', inventory_menu, menu)
    search_menu_item = SubmenuItem('Search Scryfall for Cards', search_menu, menu) 

    # APPEND MAIN MENU ITEMS
    menu.append_item(import_from_json)
    menu.append_item(export_to_json)
    menu.append_item(inventory_menu_item)
    menu.append_item(search_menu_item)

    menu.show()


# INVENTORY SEARCH FUNCTIONS
def _invSearchSet(inventory):
    setname = input('Enter name of set to search by\n>>')
    # settype = input('Enter set type [\'CORE\',\'EXPANSION\',\'COMMANDER\']')
    placeholder = input('Press any key to continue...\n>>')

def _invSearchBlock(inventory):
    blockname = input('Enter name of block to search by\n>>')
    placeholder = input('Press any key to continue...\n>>')

def _invSearchName(inventory):
    cardname = input('Enter name of card to search by\n>>')
    placeholder = input('Press any key to continue...\n>>')

def _invSearchMID(inventory):
    m_id = input('Enter multiverse id of card to search by\n>>')
    placeholder = input('Press any key to continue...\n>>')


# SCRYFALL SEARCH FUNCTIONS
def _scrySearchSet(scryfall):
    print(scryfall)
    setname = input('Enter name of set to search by\n>>')
    # settype = input('Enter set type [\'CORE\',\'EXPANSION\',\'COMMANDER\']')
    scryfall.search([setname], 'set')

def _scrySearchBlock(scryfall):
    blockname = input('Enter name of block to search by\n>>')
    scryfall.search([blockname], 'block')

def _scrySearchName(scryfall):
    cardname = input('Enter name of card to search by\n>>')
    scryfall.search([cardname], 'fuzzyname')

def _scrySearchMID(scryfall):
    m_id = input('Enter multiverse id of card to search by\n>>')
    scryfall.search([m_id], 'm_id')


# IMPORTS AND EXPORTS
def _importFromJson(inventory):
    print('Loading from JSON file')
    placeholder = input('Press any key to continue...\n>>')

def _exportToJson(inventory):
    print('Exporting to JSON file')
    placeholder = input('Press any key to continue...\n>>')