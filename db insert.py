import csv
import pprint
import pandas as pd
from tqdm import tqdm
from mongoclient import mongo
import numpy as np

DB_READY = False    # remove when DB server is ready to use
DROP_TABLE = False  # set True if need to reload data



drop_col = ["frame_effects", "life_modifier", "hand_modifier"]


print("Building Dataframes")
inventoryDF = pd.read_json("tests/data/examplecards/layout_test_set.json")
inventoryDF.info(verbose=False, memory_usage="deep")

## preprocessing, clean data
inventoryDF_cleaned = inventoryDF.drop(columns=drop_col)

print(inventoryDF_cleaned)



if DB_READY:
  # Set up database connection
  db_client = mongo()


  # Drop collection contents if needed
  if(DROP_TABLE):
    print("Dropping existing table.")
    db_client.db_collection.drop()



  # Process loopdata items
  print("Inserting rows...")
  total_rows = inventoryDF.shape[0]

  to_insert = []
  for count, df_item in tqdm(inventoryDF.iterrows(), total=total_rows):
      to_insert.append(df_item)

      if count % db_client.batch_limit == 0:
          db_client.db_collection.insert_many(to_insert)
          to_insert = []


  print("Showing sample entry.")
  results = db_client.db_collection.find().limit(1)
  pp = pprint.PrettyPrinter(indent=2)
  for x in results:
      pp.pprint(x)
