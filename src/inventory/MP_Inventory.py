from os import sep
import sqlite3
import pandas as pd
from tqdm import tqdm
import dbUtils

class MP_Inventory:
    def __init__ (self):
        '''Initalizes the connection to the ManaPool-Inventory Database.
        Creates a new Database if one does not exist.'''
        self.connection = sqlite3.connect("ManaPool-Inventory.db")
        self.cursor = self.connection.cursor()

        # First time initialization of inventory Database
        if None ==  self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='MTG-Cards'").fetchone():
            self.__firstTimeSetup()
        else:
            self.__checkForUpdates()

    # TODO... Implement
    def add_card(self, card):
        self.connection.commit()
        return False

    # TODO... Implement
    def remove_card(self, card):
        self.connection.commit()
        return False

    def close (self):
        self.connection.commit()
        self.connection.close()

    # TODO, reimagine each of these find_cards_* methods, as filters methods.
    # Provide them with the list that is to be filtered.
    # This will allow complex chaining, of searches.
    def find_cards_with_set(self,searched_setname):
        '''Returns a list of Dataframes for each card in the ManaPool-Inventory.db matching the provided setname'''
        return f"Stub, but here's {searched_setname}"
        #return self.cursor.execute(f"SELECT * FROM 'MTG-Cards' WHERE set_name={searched_setname}'")

    def find_cards_with_name(self, searched_cardname):
        '''Returns a list of Dataframes for each card in the ManaPool-Inventory.db matching the provided card name'''
        return f"Stub, but here's {searched_cardname}"
        #return self.cursor.execute(f"SELECT * FROM 'MTG-Cards' WHERE name={searched_cardname}'")

    def all_cards(self):
        '''Returns a list of Dataframes for each card in the ManaPool-Inventory.db'''
        return f"Stub, but here's all_cards"
        #return self.cursor.execute("SELECT * FROM 'MTG-Cards'")

    def __firstTimeSetup(self):
        # TODO . . . Create Relational DB Tables
        # Base table of 'MTG-Cards' contains all 60k cards.
        # self.cursor.execute("CREATE TABLE MTG-Cards")

        # Obtaining Inital Card Data
        bulk_json = dbUtils.getBulkData('default_cards')
        inventoryDF = pd.read_json(bulk_json, dtype={"full_art": int, "textless": int, "foil": int, "nonfoil": int, "oversized": int, "promo": int })

        # Removing headers deemed useless for application.
        self.inventoryDF_cleaned = inventoryDF[dbUtils.schema_headers]
        DF_rows = self.inventoryDF_cleaned.shape[0]  

        # Initilizing the stock count for each variant of all cards to 0 or NaN.  
        self.inventoryDF_cleaned = inventoryDF[dbUtils.schema_headers]
        for header in [ "full_art", "textless", "foil", "nonfoil", "oversized", "promo"]:
            self.inventoryDF_cleaned[header] = self.inventoryDF_cleaned[header].replace(0, pd.NA)
            self.inventoryDF_cleaned[header] -= 1

        # Get the first multiverse id from the list they are in or tag the token cards with -1
        for count, df_item in tqdm(self.inventoryDF_cleaned.iterrows(), total=DF_rows):
            ids = self.inventoryDF_cleaned.iloc[count]['multiverse_ids']
 
        # for a later date
        self.token_cards = self.inventoryDF_cleaned[self.inventoryDF_cleaned['multiverse_ids'] == -1]

        print("\nResulting cleaned Dataframe\n")
        print("\n", self.inventoryDF_cleaned, "\n")

            # Insert the current df_item, into the MTG-Cards table.
            # Figure out what other tables the current df_item might need inserted into. (efficient queries later / JOINS on tables.)

    def __checkForUpdates(self):
        '''Checks if the current ManaPool database needs to update with new card data'''
        # get size of current database (#cards).
        # get size of bulk file (#cards).
        # if diff: confirm(y/n) to update
        # if y: re-initalize.
