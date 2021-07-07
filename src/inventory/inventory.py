import sqlite3
import pandas as pd
from tqdm import tqdm
from . import db_utils

class Inventory:
    def __init__ (self):
        '''Initalizes the connection to the ManaPool-Inventory Database.
        Creates a new Database if one does not exist.'''
        self.connection = sqlite3.connect("ManaPool-Inventory.db")
        self.cursor = self.connection.cursor()

        # First time initialization of inventory Database
        # if None ==  self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='MTG-Cards'").fetchone():
        #     self.__firstTimeSetup()

        self.__checkForUpdates()

    # TODO... Implement
    def addCard(self, card):
        self.connection.commit()
        return False

    # TODO... Implement
    def removeCard(self, card):
        self.connection.commit()
        return False

    def close (self):
        self.connection.commit()
        self.connection.close()

    # TODO, reimagine each of these find_cards_* methods, as filters methods.
    # Provide them with the list that is to be filtered.
    # This will allow complex chaining, of searches.
    def searchBySet(self, searched_setname):
        '''Returns a list of Dataframes for each card in the ManaPool-Inventory.db matching the provided setname'''
        return []
        #return self.cursor.execute(f"SELECT * FROM 'MTG-Cards' WHERE set_name={searched_setname}'")

    def searchByName(self, searched_cardname):
        '''Returns a list of Dataframes for each card in the ManaPool-Inventory.db matching the provided card name'''
        return []
        #return self.cursor.execute(f"SELECT * FROM 'MTG-Cards' WHERE name={searched_cardname}'")

    def searchByID(self, searched_cardID):
        '''Returns a list of Dataframes for each card in the ManaPool-Inventory.db matching the provided card name'''
        return []
        #return self.cursor.execute(f"SELECT * FROM 'MTG-Cards' WHERE name={searched_cardname}'")

    def all_cards(self):
        '''Returns a list of Dataframes for each card in the ManaPool-Inventory.db'''
        return []
        #return self.cursor.execute("SELECT * FROM 'MTG-Cards'")

    def __firstTimeSetup(self):
        # TODO . . . Create Relational DB Tables
        # Base table of 'MTG-Cards' contains all 60k cards.
        # self.cursor.execute("CREATE TABLE MTG-Cards")

        bulk_json = db_utils.getBulkData('default_cards')
        inventoryDF = pd.read_json(bulk_json)
        self.inventoryDF_cleaned = inventoryDF[db_utils.schema_headers]

        print("\nResulting cleaned Dataframe\n")
        self.inventoryDF_cleaned.info(verbose=False, memory_usage="deep")
        print("\n", self.inventoryDF_cleaned, "\n")

        DF_rows = self.inventoryDF_cleaned.shape[0]

        # Get the first multiverse id from the list they are in or tag the token cards with -1
        for r in range(DF_rows):
            ids = self.inventoryDF_cleaned.iloc[r]['multiverse_ids']
            self.inventoryDF_cleaned['multiverse_ids'].iloc[r] = -1 if ids == [] else ids[0]

        # for a later date
        self.token_cards = self.inventoryDF_cleaned[self.inventoryDF_cleaned['multiverse_ids'] == -1]

        # A useless iteration, just to show everything is in the Dataframes.
        # for count, df_item in tqdm(self.inventoryDF_cleaned.iterrows(), total=DF_rows):
        #     print(count)
            # Insert the current df_item, into the MTG-Cards table.
            # Figure out what other tables the current df_item might need inserted into. (efficient queries later / JOINS on tables.)

    def __checkForUpdates(self):
        '''Checks if the current ManaPool database needs to update with new card data'''
        # get size of current database (#cards).
        # get size of bulk file (#cards).
        # if diff: confirm(y/n) to update
        # if y: re-initalize.

# Likely will invoke this from some client GUI class.
inventory = Inventory()
