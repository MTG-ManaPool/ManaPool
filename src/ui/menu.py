from .menu_utils import CardList

class Menu():
    def __init__ (self):
        self.main_menu_title = 'Welcome to ManaPool'
        self.main_menu_items = {
            '1: Import Inventory from a JSON file': self.__importFromJson,
            '2. Export Inventory to a JSON file': self.__exportToJson,
            '3. Access Inventory': self.__inventoryMenu,
            '4. Search for Cards': self.__searchMenu,
            '5. Quit ManaPool': None
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


    # PUBLIC MENU's
    def mainMenu(self, inventory):
        self.__renderMenu(self.main_menu_title, self.main_menu_items, inventory)
    
    # PRIVATE MENU's
    def __inventoryMenu(self, inventory):
        self.__renderMenu(self.inv_menu_title, self.inv_menu_items, inventory)
    
    def __searchMenu(self, inventory):
        self.__renderMenu(self.search_menu_title, self.search_menu_items, inventory)

    def __addCardMenu(self, inventory):
        print('\n' * 50)
        self.__renderMenu(self.add_menu_title, self.search_menu_items, [inventory, 'add'])

    def __removeCardMenu(self, inventory):
        print('\n' * 50)
        self.__renderMenu(self.remove_menu_title, self.search_menu_items, [inventory, 'remove'])
    
    # IMPORTS CURRENT INVENTORY FROM AN EXPORTED JSON FILE
    def __importFromJson(self, inventory):
        print('\n\nLoading from JSON file')
        placeholder = input('Press any key to continue...\n')

    # EXPORTS CURRENT INVENTORY TO A JSON FILE
    # THIS FILE CAN BE IMPORTED LATER TO SHARE AN INVENTORY ACROSS DEVICES
    def __exportToJson(self, inventory):
        print('\n\nExporting to JSON file')
        placeholder = input('Press any key to continue...\n')

    # WRAPPER FUNCTION TO DISPLAY ALL OWNED CARDS
    def __displayAll(self, inventory):
        print('\n\nDisplaying all Cards...\n')
        cards = inventory.displayInventory()
        count = 0
        for card in cards:
            print(
                'MID:', card['multiverse_ids'], ' ',
                'Name:', card['name'], ' ',
                'Mana:', card['mana_cost'], ' ',
                'Type:', card['type_line'], ' ',
                'Set:', card['set_name'], ' ',
                'FA:', card['full_art'], ' ',
                'T:', card['textless'], ' ',
                'F:', card['foil'], ' ',
                'NF:', card['nonfoil'], ' ',
                'O:', card['oversized'], ' ',
                'P:', card['promo'], ' ',
                )
            count += 1
        print(f'Displayed {count} cards')
        placeholder = input('\n\nPress any key to continue...\n')

    # WRAPPER FUNCTION TO ADD CARDS TO INVENTORY
    def __addCards(self, inventory, cards):
        print(f'\nAttempting to Add {len(cards)} Cards...\n\n')
        count = 0
        for card in cards:
            cardtype = card[1]
            print(
                'MID:', card[0]['multiverse_ids'], ' ',
                'Name:', card[0]['name'], ' ',
                'Mana:', card[0]['mana_cost'], ' ',
                'Type:', card[0]['type_line'], ' ',
                'Set:', card[0]['set_name'], ' ',
                'Rarity:', card[0]['rarity'], ' ',
                'Variant:', cardtype, ' '
                )
            try:
                inventory.addCardToInventory(card[0], cardtype)
                count += 1
            except Exception as e:
                print(e)
                placeholder = input('')
                continue
        print(f'\n{count} Cards added.')
        placeholder = input('Press any key to continue...\n')

    # WRAPPER FUNCTION TO REMOVE CARDS FROM INVENTORY
    def __removeCards(self, inventory, cards):
        print(f'\nAttempting to Remove {len(cards)} Cards...\n\n')
        count = 0
        for card in cards:
            cardtype = card[1]
            print(
                'MID:', card[0]['multiverse_ids'], ' ',
                'Name:', card[0]['name'], ' ',
                'Mana:', card[0]['mana_cost'], ' ',
                'Type:', card[0]['type_line'], ' ',
                'Set:', card[0]['set_name'], ' ',
                'Rarity:', card[0]['rarity'], ' '
                'Variant:', cardtype, ' '
                )
            try:
                inventory.removeCardFromInventory(card[0], cardtype)
                count += 1
            except Exception as e:
                print(e)
                placeholder = input('')
                continue
        print('\nCards removed.')
        placeholder = input('Press any key to continue...\n')

    # SEARCH MENU FUNCTIONS
    # TODO: Implement search by block functionality in db
    def __searchBlock(self, params):
        print('\n' * 50)
        blockname = input('Enter name of block to search by\n\n>')
        print('\n\nSearching...')
        placeholder = input('Press any key to continue...\n')

    def __searchSet(self, params):
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
            selected_cards = self.cache.createFromDBResponse(set, setname, action)
            if selected_cards:
                if action == 'add':
                    self.__addCards(inventory, selected_cards)
                elif action == 'remove':
                    self.__removeCards(inventory, selected_cards)
        except Exception as e:
            print(e)
            placeholder = input('')
            
    def __searchName(self, params):
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
            selected_cards = self.cache.createFromDBResponse(cards, cardname, action)
            if selected_cards:
                if action == 'add':
                    self.__addCards(inventory, selected_cards)
                elif action == 'remove':
                    self.__removeCards(inventory, selected_cards)
        except Exception as e:
            print('ERROR: Program encountered exception: ', e)
            placeholder = input('')

    def __searchMID(self, params):
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
            selected_cards = self.cache.createFromDBResponse(cards, m_id, action)
            if selected_cards:
                if action == 'add':
                    self.__addCards(inventory, selected_cards)
                elif action == 'remove':
                    self.__removeCards(inventory, selected_cards)
        except Exception as e:
            print('ERROR: Invalid input.')
            placeholder = input('')


    # RENDERS MENU FOR SELECT MENU's
    # MENU's CANNOT RETURN VALUES, THEREFORE FUNCTIONS CALLED BY MENU's ALSO CANNOT RETURN VALUES
    def __renderMenu(self, menu_title, menu_items, params):
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