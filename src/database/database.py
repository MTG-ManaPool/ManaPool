import os
import sqlite3
import pandas as pd
from tqdm import tqdm
from . import db_utils


class MP_Database:
    def __init__ (self, database_name="ManaPool-Inventory.db"):
        '''Initalizes the connection to the ManaPool-Inventory Database.
        Creates a new Database if one does not exist.'''
        self.connection = sqlite3.connect(database_name)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.table_name = "MTG-Cards"

        # First time initialization of inventory Database
        if None ==  self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}';").fetchone():
            self.__firstTimeSetup()
        else:
            self.__checkForUpdates()

    def close (self):
        self.connection.commit()
        self.connection.close()

    def searchBySet(self, setname):
        '''Searches the database for cards in the given set name.
        
            Args:
                setname (string): the full set name of a Magic The Gathering expansion set.

            Returns:
                List (cards): a list of cards whose given expansion set name exactly match the input setname.
        '''
        query = f"SELECT * FROM '{self.table_name}' WHERE set_name='{setname}';"
        return pd.read_sql_query(query, self.connection)

    def searchByBlock(self, blockname):
        query = f"SELECT * FROM '{self.table_name}' WHERE block='{blockname}';"
        return pd.read_sql_query(query, self.connection)

    def searchByName(self, cardname):
        '''Searches the database for cards that contain the input string in their printed name.
        
            Args:
                input (string): a card's printed text name.

            Returns:
                List (cards): a list of cards that contain the input text anywhere in their printed card name.
        '''
        query = f"SELECT * FROM '{self.table_name}' WHERE name LIKE '%{cardname}%';"
        return pd.read_sql_query(query, self.connection)

    def searchByMID(self, card_mid):
        '''Searches the database for a cards that has the given multiverse id.
        
            Args:
                card_mid (Integer): the gatherer multiverse id of a specific Magic The Gathering card.

            Returns:
                List (cards): a list of cards that exactly match the given multiverse id.
        '''
        query = f"SELECT * FROM '{self.table_name}' WHERE multiverse_ids='{card_mid}';"
        return pd.read_sql_query(query, self.connection)

    def all_cards(self):
        '''All cards recognized by the database."
        
            Returns:
                List (cards): a list of all cards recognized by the database.
        '''
        query =f"SELECT * FROM '{self.table_name}'"
        return pd.read_sql_query(query, self.connection)

    def __firstTimeSetup(self):
        # Obtaining Inital Card Data
        bulk_json = db_utils.getBulkData('default_cards')
        self.inventoryDF = pd.read_json(bulk_json)
        os.remove(bulk_json)

        # Filter by the defined Schema
        self.inventoryDF = self.inventoryDF[db_utils.schema_headers]

        DF_rows = self.inventoryDF.shape[0]

        color_identities = self.inventoryDF['color_identity']
        # replace all 'Falsey' values with empty list.
        self.inventoryDF['color_identity'] = color_identities.where(color_identities.astype(bool), '[]')
        # concatenate the list of characters representing different colors into one string (e.g. 'UWB')
        self.inventoryDF['color_identity'] = self.inventoryDF['color_identity'].agg(''.join)

        colors = self.inventoryDF['colors']
        # replace NaN/None with empty list
        self.inventoryDF['colors'] = colors.where(colors.notnull(), '[]')
        # concatenate the strings representing different colors into one string (e.g. 'UWB')
        self.inventoryDF['colors'] = colors.agg(''.join)

        mana_cost = self.inventoryDF['mana_cost']
        # replace NaN/None with empty string, keep already present empty strings.
        self.inventoryDF['mana_cost'] = mana_cost.where(mana_cost.notnull(), '')

        flavor_text = self.inventoryDF['flavor_text']
        # replace NaN/None with empty string, keep already present empty strings.
        self.inventoryDF['flavor_text'] = flavor_text.where(flavor_text.notnull(), '')

        keywords = self.inventoryDF['keywords']
        # replace NaN/None with empty list
        self.inventoryDF['keywords'] = keywords.where(keywords.notnull(), '[]')
        # concatenate the strings representing different keywords into one string (e.g. 'UWB')
        self.inventoryDF['keywords'] = self.inventoryDF['keywords'].agg(', '.join)


        # replace all 'Truthy' values with first multiverse ID'.
        # replace all 'Falsey' values with '-1'.
        def clean(id):
            if id:
                return id[0]
            else:
                return -1
        self.inventoryDF['multiverse_ids'] = self.inventoryDF['multiverse_ids'].map(lambda id: clean(id))

        print("Initalizing Empty Inventory . . .")
        for header in tqdm(["foil", "nonfoil"], total=2):
            self.inventoryDF[header] = self.inventoryDF[header].astype(int)
            self.inventoryDF[header] = self.inventoryDF[header].replace(0, pd.NA)
            self.inventoryDF[header] -= 1

        print("Adjusting card images . . .")
        double_faced_cards =self.inventoryDF.loc[self.inventoryDF['image_uris'].isnull()].index
        new_image_headers = ['small_img', 'normal_img', 'large_img', 'png_img', 'art_crop_img', 'border_crop_img']
        old_image_headers = ["small", "normal", "large", "png", "art_crop", "border_crop"]
        
        updated_cards = []
        for card in tqdm(range(DF_rows)):
            current_image_data = []
            if card in double_faced_cards:
                if 'image_uris' in self.inventoryDF.loc[card]['card_faces'][0]:
                    card_front = self.inventoryDF.loc[card]['card_faces'][0]['image_uris']
                    #TODO card_back = self.inventoryDF.loc[card]['card_faces'][1]['image_uris']
                    for header in old_image_headers:
                        current_image_data.append(card_front[header])
            else:
                card_front = self.inventoryDF.at[card, 'image_uris']
                #TODO card_back = placeholder MTG Image
                for header in old_image_headers:
                    current_image_data.append(card_front[header])
            updated_cards.append(current_image_data)

        # insert the DF containing the updated image headers
        self.inventoryDF[new_image_headers] = pd.DataFrame(updated_cards, columns=new_image_headers)
        # These columns have been expanded into 4 or 5 columns so we do not need the original any longer
        self.inventoryDF = self.inventoryDF.drop(columns=['image_uris', 'card_faces'])


        # Transform Pandas Dataframe into SQL table representing an Inventory Management System.
        self.inventoryDF.to_sql(self.table_name, self.connection)


    def __checkForUpdates(self):
        '''Checks if the current ManaPool database needs to update with new card data'''
        # get size of current database (#cards).
        # get size of bulk file (#cards).
        # if diff: confirm(y/n) to update
        # if y: re-initalize.