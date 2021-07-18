import os
import requests

schema_headers = [
  # Unique Database ID
  "id",

  # Card Information Headers
  # (Strings) 
  "name",
  "mana_cost",
  "colors",
  "color_identity",
  "type_line",
  "set_type",
  "set",
  "set_name",
  "rarity",
  "artist",
  "flavor_text",
  # (Integers)
  "cmc",
  "power",
  "toughness",
  "multiverse_ids",
  # Complex Data
  "keywords",
  "image_uris",
  "card_faces",
  
  # Card Art Detail Headers 
  # (Boolean) The card either Has this property for it's art, or it Does Not Have.
  # A card can be multiples of these properties.
  # A card's uniqueness in the database is retained by the set/collection_number of the card, not these properties.
  "layout",
  "full_art",
  "textless",
  "oversized",
  "promo",

  # Stock Count Headers
  # (Integer) The current stock count of this card in the given property. 
  "foil",
  "nonfoil",

  # If card condition is chosen to be tracked in a future implementation,
  # one will need to consider the concepts such as 'near_mint_foil.' 
  # near_mint
  # lightly_played
  # moderately_played
  # heavily_played
  # damaged
]

def getBulkData(requested_data):
    '''Programmatically retrieves the requested Scryfall Bulk Data JSON file.'''
    resp = requests.get("https://api.scryfall.com/bulk-data")
    available_bulk_data = resp.json()

    for bulk_file in available_bulk_data['data']:
        if(bulk_file['type'] == requested_data):
            scryfall_bulk_data_url = bulk_file['download_uri']
            break

    output_file = f'{requested_data}.json'
    # JSON Bulk File is large, and must be processed in chunks.
    # Optimal chunk size can be tested/configured later.
    with requests.get(scryfall_bulk_data_url, stream=True) as resp:
        with open(output_file, 'wb') as file:
            for chunk in resp.iter_content(chunk_size=8192):
                file.write(chunk)
    return os.path.realpath(output_file)