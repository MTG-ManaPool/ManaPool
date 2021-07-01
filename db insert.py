import csv
import pprint
import pandas as pd
from tqdm import tqdm
from mongoclient import mongo
import numpy as np

DB_READY = False    # remove when DB server is ready to use
DROP_TABLE = False  # set True if need to reload data



keep_col = [
  "object", "id", "multiverse_ids",
  "name", "mana_cost", "cmc", "colors", "color_identity",
  "image_uris", "card_faces",
  "type_line", "set_type", "set", "set_name", "rarity", "artist", 
  "collector_number", "flavor_text", "power",  "toughness",  "keywords", 
  "layout", "full_art", "textless", "foil", "nonfoil", "oversized", "promo", 
]
# If a card contains one of the fields <"full_art", "textless", "foil", "nonfoil", "oversized", "promo"> then there is a variant of that type, for this card.
# We need the column created in the Database for this variant:
# to have the value NaN - if the JSON field was False. ( there is no variant of this type. cannot be an int.)
# to have the value of an int 0-999 - if the JSON field was True.  (how many copies of this variant are owned.)
drop_col = [
  "oracle_id","mtgo_id", "arena_id", "tcgplayer_id", "cardmarket_id", "mtgo_foil_id",  "illustration_id", "artist_ids", "card_back_id", "set_id",
  "oracle_text", "all_parts", "lang", "released_at", "booster", "story_spotlight", "edhrec_rank", "legalities", "games", "reserved", 
  "color_indicator", "frame", "border_color", "produced_mana",
  "related_uris", "purchase_uris", "prices", "preview", "uri", "scryfall_uri", "rulings_uri", "prints_search_uri", "set_uri", "set_search_uri", "scryfall_set_uri",
  "frame_effects","life_modifier", "hand_modifier", "highres_image", "digital", "image_status", "reprint", "variation"
  ]

print("\nBuilding inital Dataframes\n")
inventoryDF = pd.read_json("tests/data/examplecards/layout_test_set.json")
inventoryDF.info(verbose=False, memory_usage="deep")

## preprocessing, clean data
inventoryDF_cleaned = inventoryDF.drop(columns=drop_col)
print("\nResulting cleaned Dataframe\n")
inventoryDF_cleaned.info(verbose=False, memory_usage="deep")
print("\n", inventoryDF_cleaned, "\n")



if DB_READY:
  # Set up database connection
  db_client = mongo()
  cards_collection = db_client.inventory.cards

  # Drop collection contents if needed
  if(DROP_TABLE):
    print("Dropping existing table.")
    cards_collection.drop()



  # Process loopdata items
  print("Inserting rows...")
  total_rows = inventoryDF.shape[0]

  to_insert = []
  for count, df_item in tqdm(inventoryDF.iterrows(), total=total_rows):
      to_insert.append(df_item)

      if count % db_client.batch_limit == 0:
          cards_collection.insert_many(to_insert)
          to_insert = []


  print("Showing sample entry.")
  results = cards_collection.find().limit(1)
  pp = pprint.PrettyPrinter(indent=2)
  for x in results:
      pp.pprint(x)
