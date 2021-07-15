import os
import sqlite3
import pandas as pd
from tqdm import tqdm
from . import db_utils
# import db_utils # USED FOR LOCAL TESTING


class MP_Inventory:
    def __init__ (self):
        '''Initalizes the connection to the ManaPool-Inventory Database.
        Creates a new Database if one does not exist.'''
        self.connection = sqlite3.connect("ManaPool-Inventory.db")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.table_name = "MTG-Cards"

        # First time initialization of inventory Database
        if None ==  self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='MTG-Cards'").fetchone():
            self.__firstTimeSetup()
        else:
            self.__checkForUpdates()

   # TODO: Implement
    def addCardToInventory(self, card, to_add):
        print('adding card')
        placeholder = input('')
        # self.connection.commit()
        # total = card.count + to_add
        # query = f"UPDATE 'MTG-Cards count' = {total} FROM WHERE id = {card.ID};"
        # self.connection.execute(query)

   # TODO: Implement
    def removeCardFromInventory(self, card, to_remove):
        print('removing card')
        placeholder = input('')
        # self.connection.commit()
        # total = card.count - to_remove
        # if total < 0:
        #     total = 0
        # query = f"UPDATE 'MTG-Cards count' = {total} FROM WHERE id = {card.ID};"
        # self.connection.execute(query)

    def updateTable(self, cards):
        try:
            updated = 0
            rows = cards.shape[0]
            for r in range(rows):
                for card_type in ["full_art", "textless", "foil", "nonfoil", "oversized", "promo"]:
                    if cards.at[r, card_type]:
                        update_query = f"UPDATE '{self.table_name}' SET {card_type} = {cards.at[r, card_type]} WHERE id == '{cards.at[r, 'id']}'"
                        self.cursor.execute(update_query)
                        updated += 1
            self.connection.commit()
            print(f"Updated {updated} records successfully ")
            # Should we be getting a new cursor at each method?
            # self.cursor.close()

        except sqlite3.Error as error:
            print("Failed to update sqlite table", error)



   # TODO: Implement
    def displayInventory():
        print('Displaying inventory')
        placeholder = input('')

    def close (self):
        self.connection.commit()
        self.connection.close()

    def searchBySet(self, setname):
        query = f"SELECT * FROM '{self.table_name}' WHERE set_name='{setname}'"
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def searchByBlock(self, blockname):
        query = f"SELECT * FROM '{self.table_name}' WHERE block='{blockname}'"
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def searchByName(self, cardname):
        query = f"SELECT * FROM '{self.table_name}' WHERE name='{cardname}'"
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def searchByMID(self, card_mid):
        query = f"SELECT * FROM '{self.table_name}' WHERE multiverse_ids='{card_mid}'"
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def all_cards(self):
        '''Returns a list of Dataframes for each card in the ManaPool-Inventory.db'''
        return f"Stub, but here's all_cards"
        #return self.cursor.execute("SELECT * FROM 'MTG-Cards'")

    def __firstTimeSetup(self):
        # TODO . . . Create Relational DB Tables
        # Base table of 'MTG-Cards' contains all 60k cards.
        # self.cursor.execute("CREATE TABLE MTG-Cards")

        # Obtaining Inital Card Data
        bulk_json = db_utils.getBulkData('default_cards')

        self.inventoryDF = pd.read_json(bulk_json, dtype={"full_art": int,
                                                          "textless": int,
                                                          "foil": int,
                                                          "nonfoil": int,
                                                          "oversized": int,
                                                          "promo": int }
                                        )


        # Filter by the defined Schema
        self.inventoryDF = self.inventoryDF[db_utils.schema_headers]

        DF_rows = self.inventoryDF.shape[0]


        # COLOR Identities
        color_id = self.inventoryDF['color_identity']
        # Didnt find any NaN values but better safe than sorry
        for row in self.inventoryDF.loc[color_id.isnull(), 'color_identity'].index:
            self.inventoryDF.at[row, 'color_identity'] = []

        # concatenate the strings representing different color into one strin (e.g. 'UWB')
        self.inventoryDF['color_identity'] = color_id.agg(''.join)



        # COLOR
        colors = self.inventoryDF['colors']
        # replace NaN/None with empty list in preparatio for join
        for row in self.inventoryDF.loc[colors.isnull(), 'colors'].index:
            self.inventoryDF.at[row, 'colors'] = []

        # concatenate the strings representing different color into one strin (e.g. 'UWB')
        self.inventoryDF['colors'] = colors.agg(''.join)



        # IMAGE URIS
        new_img_uris = ['small_img', 'normal_img', 'large_img', 'png_img', 'art_crop_img', 'border_crop_img']
        old_img_uris = self.inventoryDF['image_uris']
        data_as_list = []
        index_without_image = self.inventoryDF.loc[self.inventoryDF.image_uris.isnull()].index
        for row in range(DF_rows):

            temp = []

            # replace NaN/None with empty list
            if row in index_without_image:
                # FIXME still need to account for second face. Talked about making a seperate Table for these cards
                if self.inventoryDF.loc[row]['card_faces'] and 'image_uris' in self.inventoryDF.loc[row]['card_faces'][0]:
                    face1_img_uris = self.inventoryDF.loc[row]['card_faces'][0]['image_uris']
                    small = face1_img_uris["small"]
                    temp.append(small)
                    normal = face1_img_uris["normal"]
                    temp.append(normal)
                    large = face1_img_uris["large"]
                    temp.append(large)
                    png = face1_img_uris["png"]
                    temp.append(png)
                    art_crop = face1_img_uris["art_crop"]
                    temp.append(art_crop)
                    border_crop = face1_img_uris["border_crop"]
                    temp.append(border_crop)
                #else not two faced but still null make them NaN
                else:
                    temp = [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]
            else:
                card_image = self.inventoryDF.at[row, 'image_uris']
                small = card_image["small"]
                temp.append(small)
                normal = card_image["normal"]
                temp.append(normal)
                large = card_image["large"]
                temp.append(large)
                png = card_image["png"]
                temp.append(png)
                art_crop = card_image["art_crop"]
                temp.append(art_crop)
                border_crop = card_image["border_crop"]
                temp.append(border_crop)



            data_as_list.append(temp)

        # insert the new DF after making the all the columns first
        self.inventoryDF[new_img_uris] = pd.DataFrame(data_as_list, columns=new_img_uris)



        # KEYWORDS
        keywords = self.inventoryDF['keywords']
        # replace NaN/None with empty list in preparatio for join
        for row in self.inventoryDF.loc[keywords.isnull(), 'keywords'].index:
            self.inventoryDF.at[row, 'keywords'] = []

        # concatenate the strings representing different color into one strin (e.g. 'UWB')
        self.inventoryDF['keywords'] = keywords.agg(', '.join)




        # These columns have been expanded into 4 or 5 columns so we do not need the original any longer
        self.inventoryDF = self.inventoryDF.drop(columns=['image_uris', 'card_faces'])


        # Initilizing the stock count for each variant of all cards to 0 or NaN.
        for header in [ "full_art", "textless", "foil", "nonfoil", "oversized", "promo"]:
            self.inventoryDF[header] = self.inventoryDF[header].replace(0, pd.NA)
            self.inventoryDF[header] -= 1


        # Get the first multiverse id from the list they are in or tag the token cards with -1
        for r in tqdm(range(DF_rows)):
            ids = self.inventoryDF.iloc[r]['multiverse_ids']
            self.inventoryDF['multiverse_ids'].iloc[r] = -1 if ids == [] else ids[0]


        # for a later date
        self.token_cards = self.inventoryDF[self.inventoryDF['multiverse_ids'] == -1]

        print("\nResulting cleaned Dataframe\n")
        print("\n", self.inventoryDF, "\n")
        self.inventoryDF.info(verbose=False, memory_usage="deep")

        # Insert the current df_item, into the MTG-Cards table.
        # Figure out what other tables the current df_item might need inserted into. (efficient queries later / JOINS on tables.)

        # CREATE SQL TABLE with Schema from DATAFRAME
        self.inventoryDF.to_sql(self.table_name, self.connection)
        os.remove(bulk_json)


    def __checkForUpdates(self):
        '''Checks if the current ManaPool database needs to update with new card data'''
        # get size of current database (#cards).
        # get size of bulk file (#cards).
        # if diff: confirm(y/n) to update
        # if y: re-initalize.

# Only instanciate MP_Inventory when working in this script directly
if __name__ == '__main__':
    x = MP_Inventory()
    res = ''

    while res.lower() != 'y':
        cards = x.searchByMID('109722')
        print(cards)
        print('Done testing? [Y/N]')
        res = input('>')