from os import sep
import sqlite3
import pandas as pd
from tqdm import tqdm
import db_utils


class MP_Inventory:
    def __init__ (self):
        '''Initalizes the connection to the ManaPool-Inventory Database.
        Creates a new Database if one does not exist.'''
        self.connection = sqlite3.connect("ManaPool-Inventory.db")
        self.cursor = self.connection.cursor()
        self.table_name = "MTG-Cards"

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
        new_color_id_cols = ['color_id1', 'color_id2', 'color_id3', 'color_id4', 'color_id5']
        old_color_id_col = self.inventoryDF['color_identity']
        # Didnt find any NaN values but better safe than sorry
        for row in self.inventoryDF.loc[old_color_id_col.isnull(), 'color_identity'].index:
            self.inventoryDF.at[row, 'color_identity'] = []
        self.inventoryDF[new_color_id_cols] = pd.DataFrame(old_color_id_col.to_list(), index=old_color_id_col.index)

        # COLOR
        new_color_cols = ['Color1', 'Color2', 'Color3', 'Color4', 'Color5']
        old_color_col = self.inventoryDF['colors']
        # replace NaN/None with empty list
        for row in self.inventoryDF.loc[self.inventoryDF.colors.isnull(), 'colors'].index:
            self.inventoryDF.at[row, 'colors'] = []
        self.inventoryDF[new_color_cols] = pd.DataFrame(old_color_col.to_list(), index=old_color_col.index)


        # IMAGE URIS
        new_img_uris = ['small_img', 'normal_img', 'large_img', 'png_img', 'art_crop_img', 'border_crop_img']
        old_img_uris = self.inventoryDF['image_uris']
        data_as_list = []
        is_null = self.inventoryDF.loc[self.inventoryDF.image_uris.isnull()].index
        for row in range(DF_rows):
            # replace NaN/None with empty list
            temp = []
            if row in is_null:
                # TODO check for two faced cards here as anothe condition
                #else not two faced but still null
                temp = [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]
            else:
                small = self.inventoryDF.at[row, 'image_uris']["small"]
                temp.append(small)
                normal = self.inventoryDF.at[row, 'image_uris']["normal"]
                temp.append(normal)
                large = self.inventoryDF.at[row, 'image_uris']["large"]
                temp.append(large)
                png = self.inventoryDF.at[row, 'image_uris']["png"]
                temp.append(png)
                art_crop = self.inventoryDF.at[row, 'image_uris']["art_crop"]
                temp.append(art_crop)
                border_crop = self.inventoryDF.at[row, 'image_uris']["border_crop"]
                temp.append(border_crop)

            data_as_list.append(temp)

        # insert the new DF after making the all the columns first
        self.inventoryDF[new_img_uris] = pd.DataFrame(data_as_list, columns=new_img_uris)



        # KEYWORDS
        new_leywords = ['keyword1', 'keyword2', 'keyword3', 'keyword4', 'keyword5','keyword6', 'keyword7', 'keyword8', 'keyword9', 'keyword10']
        old_leyword = self.inventoryDF['keywords']
        # replace NaN/None with empty list
        for row in self.inventoryDF.loc[self.inventoryDF.keywords.isnull(), 'keywords'].index:
            self.inventoryDF.at[row, 'keywords'] = []
        self.inventoryDF[new_leywords] = pd.DataFrame(old_leyword.to_list(), index=old_leyword.index)



        # These columns have been expanded into 4 or 5 columns so we do not need the original any longer
        self.inventoryDF = self.inventoryDF.drop(columns=['colors', 'color_identity', 'image_uris', 'keywords'])


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

    def __checkForUpdates(self):
        '''Checks if the current ManaPool database needs to update with new card data'''
        # get size of current database (#cards).
        # get size of bulk file (#cards).
        # if diff: confirm(y/n) to update
        # if y: re-initalize.

# Only instanciate MP_Inventory when working in this script directly
if __name__ == '__main__':
    x = MP_Inventory()