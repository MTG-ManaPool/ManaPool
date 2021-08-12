from ui.menu_utils import clear_screen
from cardlist.cardlist import CardList
from orders.purchaselist import PurchaseList
import os.path

class Menu():
    def __init__ (self):

        self.main_menu_title = 'Welcome to ManaPool'
        self.main_menu_items = {
            '1: Import Inventory from a JSON file': self.__importFromJson,
            '2. Export Inventory to a JSON file': self.__exportToJson,
            '3. Access Inventory': self.__inventoryMenu,
            '4. Search for Cards': self.__searchMenu,
            '5. Purchase Cards': self.__purchaseMenu,
            '6. Quit ManaPool': None
        }
        self.inv_menu_title = 'Inventory Menu'
        self.inv_menu_items = {
            '1: Add Cards to Inventory': self.__addCardMenu,
            '2. Remove Cards from Inventory': self.__removeCardMenu,
            '3. View Inventory': self.__displayAll,
            '4. Main Menu': None
        }
        self.search_menu_title = 'Search Menu'
        self.search_menu_items = {
            '1: Search for Cards by Set': self.__searchSet,
            '2. Search for Cards by Block': self.__searchBlock,
            '3. Search for Cards by Name': self.__searchName,
            '4. Search for Cards by Multiverse ID': self.__searchMID,
            '5. Quit': None
        }
        self.add_menu_title = 'Select Method to Search for Cards to Add'
        self.remove_menu_title = 'Select Method to Search for Cards to Remove'
        self.cache = CardList()


    def mainMenu(self, inventory, database):
        self.__renderMenu(self.main_menu_title, self.main_menu_items, [inventory, database, None])
    
    def __inventoryMenu(self, params):
        self.__renderMenu(self.inv_menu_title, self.inv_menu_items, params)

    def __searchMenu(self, params):
        self.__renderMenu(self.search_menu_title, self.search_menu_items, params)

    def __purchaseMenu(self, params):
        clear_screen()
        inventory = params[0]
        database = params[1]
        self.__renderMenu(self.add_menu_title, self.search_menu_items, [inventory, database, 'buy'])

    def __addCardMenu(self, params):
        clear_screen()
        inventory = params[0]
        database = params[1]
        self.__renderMenu(self.add_menu_title, self.search_menu_items, [inventory, database, 'add'])

    def __removeCardMenu(self, params):
        clear_screen()
        inventory = params[0]
        database = params[1]
        self.__renderMenu(self.remove_menu_title, self.search_menu_items, [inventory, database, 'remove'])
    
    def __importFromJson(self, params):
        clear_screen()
        inventory = params[0]
        quit = False
        legal = False
        while not legal and not quit:
            try:
                print('WARNING! This action will overwrite saved changes to your inventory!')
                print('\t To save current changes, export the current inventory, then copy')
                print('\t and paste the contents of your exported file to the end of file you wish to import.')
                print('\n\nPlease enter the path of the JSON file you want to import from. Or type [Q] to quit\n\n')
                path = input('>')
                if path == 'Q' or path == 'q':
                    quit = True
                elif not path.endswith('.json'):
                    raise Exception('Specified file must be a JSON file.')
                else:
                    print('\n\nAttempting import from JSON file')
                    count = inventory.importJSON(path)
                    print(f'\n\nImport successful! Imported {count} cards\n')
                    legal = True
            except Exception as e:
                print(f'ERROR: There was a problem importing your file. {e}')
        placeholder = input('Press any key to continue...\n')

    def __exportToJson(self, params):
        clear_screen()
        inventory = params[0]
        quit = False
        legal = False
        while not legal and not quit:
            try:
                print('\n\nPlease enter the path of the JSON file you want to export to. Or type [Q] to quit.\n')
                path = input('>')
                if path == 'Q' or path == 'q':
                    quit = True
                elif not path.endswith('.json'):
                    raise Exception('Specified file must be a JSON file.')
                elif os.path.isfile(path) == True:
                    raise Exception('Specified file already exists.')
                else:
                    print('\n\nAttempting export to JSON file...')
                    count = inventory.exportJSON(path)
                    print(f'\n\nExport successful. Inventory exported {count} cards')
                    legal = True
            except Exception as e:
                print(f'\n\nERROR: There was a problem exporting your file. {e}')
        placeholder = input('Press any key to continue...\n')

    def __displayAll(self, params):
        inventory = params[0]
        cards = inventory.getInventory()
        count = 0
        if not cards.empty:
            print('\n\nDisplaying all Cards...\n')
            for index, card in cards.iterrows():
                print(
                    'MID:', card['multiverse_ids'], ' ',
                    'Name:', card['name'], ' ',
                    'Mana:', card['mana_cost'], ' ',
                    'Type:', card['type_line'], ' ',
                    'Set:', card['set_name'], ' ',
                    'Rarity:', card['rarity'], ' ',
                    'Foils:', card['foil'], ' ',
                    'Nonfoils:', card['nonfoil'], ' '
                    )
                count += 1
            print(f'\n\nDisplayed {count} cards')
        else:
            print("\n\nNo Cards found...\n")
        placeholder = input('\n\nPress any key to continue...\n')

    def __addCards(self, inventory, cards):
        print(f'\nAttempting to Add {len(cards.index)} Cards...\n\n')
        count = 0
        if not cards.empty:
            for index, card in cards.iterrows():
                print(
                    'MID:', card['multiverse_ids'], ' ',
                    'Name:', card['name'], ' ',
                    'Mana:', card['mana_cost'], ' ',
                    'Type:', card['type_line'], ' ',
                    'Set:', card['set_name'], ' ',
                    'Rarity:', card['rarity'], ' ',
                    'Variant:', card['variant'], ' ',
                    )
                try:
                    inventory.addCardToInventory(card)
                    count += 1
                except Exception as e:
                    print(e)
                    placeholder = input('')
                    continue
            print(f'\n\n{count} Cards added.')
        else:
           print("\n\nNo cards specified to add...\n") 
        placeholder = input('Press any key to continue...\n')

    def __removeCards(self, inventory, cards):
        print(f'\nAttempting to Remove {len(cards)} Cards...\n\n')
        count = 0
        if not cards.empty:
            for index, card in cards.iterrows():
                print(
                    'MID:', card['multiverse_ids'], ' ',
                    'Name:', card['name'], ' ',
                    'Mana:', card['mana_cost'], ' ',
                    'Type:', card['type_line'], ' ',
                    'Set:', card['set_name'], ' ',
                    'Rarity:', card['rarity'], ' ',
                    'Variant:', card['variant'], ' ',
                    )
                try:
                    inventory.removeCardFromInventory(card)
                    count += 1
                except Exception as e:
                    print(e)
                    placeholder = input('')
                    continue
            print(f'\n\n{count} Cards removed.')
        else:
           print("\n\nNo cards specified to remove...\n") 
        placeholder = input('Press any key to continue...\n')

    # TODO: Implement search by block functionality in db
    def __searchBlock(self, params):
        clear_screen()
        blockname = input('Enter name of block to search by\n\n>')
        print('\n\nSearching...')
        placeholder = input('Press any key to continue...\n')

    def __searchSet(self, params):
        clear_screen()
        inventory = params[0]
        database = params[1]
        action = params[2]
        setname = input('Enter name of set to search by\n\n>')
        try:
            if action == 'remove':
                set = inventory.searchBySet(setname)
            else:
                set = database.searchBySet(setname)
            self.__handleResponse(inventory, setname, set, action)
        except Exception as e:
            print(e)
            placeholder = input('')
            
    def __searchName(self, params):
        inventory = params[0]
        database = params[1]
        action = params[2]
        clear_screen()
        cardname = input('Enter name of card to search by\n\n>')
        try:
            if action == 'remove':
                cards = inventory.searchByName(cardname)
            else:
                cards = database.searchByName(cardname)
            self.__handleResponse(inventory, cardname, cards, action) 
        except Exception as e:
            print('ERROR: Program encountered exception: ', e)
            placeholder = input('')

    def __searchMID(self, params):
        inventory = params[0]
        database = params[1]
        action = params[2]
        clear_screen()
        m_id = input('Enter multiverse id of card to search by\n\n>')
        try:
            if action == 'remove':
                cards = inventory.searchByMID(m_id)
            else:
                cards = database.searchByMID(m_id)
            self.__handleResponse(inventory, m_id, cards, action) 
        except Exception as e:
            print('ERROR: Invalid input.')
            placeholder = input('')
    
    def __handleResponse(self, inventory, groupname, cards, action):
        selected = self.cache.createFromDBResponse(cards, groupname, action)
        if not selected.empty:
            if action == 'add':
                self.__addCards(inventory, selected)
            elif action == 'remove':
                self.__removeCards(inventory, selected)
            elif action == 'buy':
                order = PurchaseList(self.cache)
                order.submitOrder()

    def __renderMenu(self, menu_title, menu_items, params):
        quit = False
        while not quit:
            legal = False
            clear_screen()
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