import sqlite3
import pandas as pd
from database import db_utils

class MP_Inventory:
    def __init__ (self):
        '''Initalizes the connection to the ManaPool-Inventory Database.'''
        self.connection = sqlite3.connect("ManaPool-Inventory.db")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.table_name = "MTG-Cards"

        # First time initialization of inventory Database
        if None ==  self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}';").fetchone():
            raise Exception('Database DNE Exception.')
    
    def close (self):
        self.connection.commit()
        self.connection.close()

    def importJSON(self, cards):
        try:
            updated = 0
            rows = cards.shape[0]
            for r in range(rows):
                for card_type in db_utils.stock_headers:
                    if cards.at[r, card_type]:
                        update_query = f"UPDATE '{self.table_name}' SET {card_type} = {cards.at[r, card_type]} WHERE id == '{cards.at[r, 'id']}'"
                        self.cursor.execute(update_query)
                        updated += 1
            self.connection.commit()
            print(f"Updated {updated} records successfully ")
            # Should we be getting a new cursor at each method?
            # self.cursor.close()

        except sqlite3.Error as error:
            print("Failed to update table", error)

    def exportJSON(self, dst):
        try:
            if self.connection:
                # Make sure there is an empty space at the end of each string
                query = f"SELECT name, set_name, full_art, textless, foil, nonfoil, oversized, promo "
                query += f"FROM '{self.table_name}' "
                query += f"WHERE 'foil' > 0 OR 'nonfoil' > 0 "

                # FIXME REMOVE THE LIMIT AFTER VERIFYING
                query += f"LIMIT 3"

                my_inventory = pd.read_sql(query, self.connection)

                my_inventory.to_json(dst, orient="records")
                records = my_inventory.shape[0]
                print(f"Retrieved {records} records successfully ")

                # importing here since this is the only function that uses it. If it is used more often make global
                import time
                time.sleep(5)

        except sqlite3.Error as error:
            print("Failed to read table", error)

    def addCardToInventory(self, card, variant):
        '''Adds the specified card of the given variant to the inventory.

            Args:
                card (SQLiteRow): a dict-addressable card row from the database.
                variant (string): the specified variant of the card to be added.
        '''
        total = card[f'{variant}']
        if total == None:
            print('\n\nERROR: Cannot add Cards to Inventory.')
            raise Exception(f"{card['name']} does not exist in the {variant} format.")

        total += 1
        query = f"UPDATE '{self.table_name}' SET {variant} = {total} WHERE id == '{card['id']}';"
        self.connection.execute(query)
        self.connection.commit()

    def removeCardFromInventory(self, card, variant):
        '''Removes the specified card of the given variant from the inventory.

            Args:
                card (SQLiteRow): a dict-addressable card row from the database.
                variant (string): the specified variant of the card to be added.
        '''
        total = card[f'{variant}']
        if total == None:
            print('\n\nERROR: Cannot remove Cards from Inventory.')
            raise Exception(f"{card['name']} does not exist in the {variant} format.")

        total -=  1
        if total < 0:
            raise Exception(f"ERROR: Inventory Count for {card['name']} is 0 for {variant}'s")
        query = f"UPDATE '{self.table_name}' SET {variant} = {total} WHERE id == '{card['id']}';"
        self.connection.execute(query)
        self.connection.commit()

    def getInventory(self):
        '''Searches the inventory for cards that are in stock.

            Returns:
                List (cards): a list of cards that whose inventory count of foil or nonfoil is greater than 0.
        '''
        query = f"SELECT * FROM '{self.table_name}' WHERE foil > 0 OR nonfoil > 0;"
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def searchBySet(self, setname):
        '''Searches the inventory for cards in stock with the given set name.
        
            Args:
                setname (string): the full set name of a Magic The Gathering expansion set.

            Returns:
                List (cards): a list of cards whose given expansion set name exactly match the input setname.
        '''
        query = f"SELECT * FROM '{self.table_name}' WHERE set_name='{setname}' AND (foil>0 OR nonfoil>0);"
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def searchByBlock(self, blockname):
        query = f"SELECT * FROM '{self.table_name}' WHERE block='{blockname}' AND (foil>0 OR nonfoil>0);"
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def searchByName(self, cardname):
        '''Searches the inventory for cards in stock that contain the input string in their printed name.
        
            Args:
                input (string): a card's printed text name.

            Returns:
                List (cards): a list of cards that contain the input text anywhere in their printed card name.
        '''
        query = f"SELECT * FROM '{self.table_name}' WHERE name LIKE '%{cardname}%' AND (foil>0 OR nonfoil>0);"
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def searchByMID(self, card_mid):
        '''Searches the inventory database for a card in stock that has the given multiverse id.
        
            Args:
                card_mid (Integer): the gatherer multiverse id of a specific Magic The Gathering card.

            Returns:
                List (cards): a list of cards that exactly match the given multiverse id.
        '''
        query = f"SELECT * FROM '{self.table_name}' WHERE multiverse_ids='{card_mid}' AND (foil>0 OR nonfoil>0);"
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res