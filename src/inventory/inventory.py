import sqlite3
import pandas as pd
import json

class MP_Inventory:
    def __init__ (self, database_name="ManaPool-Inventory.db"):
        '''Initalizes the connection to the ManaPool-Inventory Database.'''
        self.connection = sqlite3.connect(database_name)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.table_name = "MTG-Cards"

        # First time initialization of inventory
        if None ==  self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}';").fetchone():
            raise Exception('Database DNE Exception.')
    
    def close (self):
        self.connection.commit()
        self.connection.close()

    def importJSON(self, path):
        with open(path) as f:
            cards = json.load(f)
            f.close()
        updated = 0
        try:
            for card in cards:
                update_query = f"UPDATE '{self.table_name}' SET foil={card['foil']}, nonfoil={card['nonfoil']} WHERE id=='{card['id']}'"
                self.cursor.execute(update_query)
                updated += 1
            self.connection.commit()
        except sqlite3.Error as error:
            print("Failed to update table.\n\n", error, "\n\nThis should never happen.")
        return updated

    def exportJSON(self, path):
        records = 0
        try:
            if self.connection:
                # Make sure there is an empty space at the end of each string
                query = f"SELECT id, name, multiverse_ids, set_name, foil, nonfoil "
                query += f"FROM '{self.table_name}' WHERE foil > 0 OR nonfoil > 0"
                my_inventory = pd.read_sql(query, self.connection)
                my_inventory.to_json(path, orient="records")
                records = my_inventory.shape[0]
        except sqlite3.Error as error:
            print("Failed to read table.\n\n", error, "\n\nThis should never happen")
        return records

    def addCardToInventory(self, card):
        '''Adds the specified card of the given variant to the inventory.

            Args:
                card (SQLiteRow): a dict-addressable card row from the database.
                variant (string): the specified variant of the card to be added.
        '''
        query = f"SELECT * FROM '{self.table_name}' WHERE id='{card['id']}';"
        tempDF = pd.read_sql_query(query, self.connection)
        if tempDF.empty:
            print('\n\nERROR: Cannot add Cards to Inventory.')
            raise Exception(f"{card['name']} does not exist in the {card['variant']} format.")
        total = tempDF[card['variant']][0]
        if total == None:
            print('\n\nERROR: Cannot add Cards to Inventory.')
            raise Exception(f"{card['name']} does not exist in the {card['variant']} format.")

        total += 1
        update = f"UPDATE '{self.table_name}' SET {card['variant']} = {total} WHERE id == '{card['id']}';"
        self.connection.execute(update)
        self.connection.commit()

    def removeCardFromInventory(self, card):
        '''Removes the specified card of the given variant from the inventory.

            Args:
                card (SQLiteRow): a dict-addressable card row from the database.
                variant (string): the specified variant of the card to be added.
        '''
        query = f"SELECT * FROM '{self.table_name}' WHERE id='{card['id']}' AND (foil>0 OR nonfoil>0);"
        tempDF = pd.read_sql_query(query, self.connection)
        if tempDF.empty:
            print('\n\nERROR: Cannot remove Cards from Inventory.')
            raise Exception(f"{card['name']} does not exist in the {card['variant']} format.")
        total = tempDF[card['variant']][0]
        if total == None:
            print('\n\nERROR: Cannot remove Cards from Inventory.')
            raise Exception(f"{card['name']} does not exist in the {card['variant']} format.")

        total -=  1
        if total < 0:
            raise Exception(f"ERROR: Inventory Count for {card['name']} is 0 for {card['variant']}'s")
        update = f"UPDATE '{self.table_name}' SET {card['variant']} = {total} WHERE id == '{card['id']}';"
        self.connection.execute(update)
        self.connection.commit()

    def getInventory(self):
        '''Searches the inventory for cards that are in stock.

            Returns:
                List (cards): a list of cards that whose inventory count of foil or nonfoil is greater than 0.
        '''
        query = f"SELECT * FROM '{self.table_name}' WHERE foil > 0 OR nonfoil > 0;"
        return pd.read_sql_query(query, self.connection)

    def searchBySet(self, setname):
        '''Searches the inventory for cards in stock with the given set name.
        
            Args:
                setname (string): the full set name of a Magic The Gathering expansion set.

            Returns:
                List (cards): a list of cards whose given expansion set name exactly match the input setname.
        '''
        query = f"SELECT * FROM '{self.table_name}' WHERE set_name='{setname}' AND (foil>0 OR nonfoil>0) ORDER BY multiverse_ids;"
        return pd.read_sql_query(query, self.connection)

    def searchByBlock(self, blockname):
        query = f"SELECT * FROM '{self.table_name}' WHERE block='{blockname}' AND (foil>0 OR nonfoil>0) ORDER BY multiverse_ids;"
        return pd.read_sql_query(query, self.connection)

    def searchByName(self, cardname):
        '''Searches the inventory for cards in stock that contain the input string in their printed name.
        
            Args:
                input (string): a card's printed text name.

            Returns:
                List (cards): a list of cards that contain the input text anywhere in their printed card name.
        '''
        query = f"SELECT * FROM '{self.table_name}' WHERE name LIKE '%{cardname}%' AND (foil>0 OR nonfoil>0) ORDER BY multiverse_ids;"
        return pd.read_sql_query(query, self.connection)

    def searchByMID(self, card_mid):
        '''Searches the inventory database for a card in stock that has the given multiverse id.
        
            Args:
                card_mid (Integer): the gatherer multiverse id of a specific Magic The Gathering card.

            Returns:
                List (cards): a list of cards that exactly match the given multiverse id.
        '''
        query = f"SELECT * FROM '{self.table_name}' WHERE multiverse_ids='{card_mid}' AND (foil>0 OR nonfoil>0) ORDER BY multiverse_ids;"
        return pd.read_sql_query(query, self.connection)