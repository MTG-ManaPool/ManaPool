import requests

schema_headers = [
  "id", "multiverse_ids",
  "name", "mana_cost", "cmc", "colors", "color_identity",
  "image_uris", "card_faces",
  "type_line", "set_type", "set", "set_name", "rarity", "artist", 
  "collector_number", "flavor_text", "power", "toughness", "keywords", 
  "layout", "full_art", "textless", "foil", "nonfoil", "oversized", "promo", 
]

def getBulkData(requested_data):
    '''Programmatically retrieves the requested Scryfall Bulk Data JSON file.'''
    resp = requests.get("https://api.scryfall.com/bulk-data")
    available_bulk_data = resp.json()

    for bulk_file in available_bulk_data['data']:
        if(bulk_file['type'] == requested_data):
            scryfall_bulk_data_url = bulk_file['download_uri']

    output_file = f'{requested_data}.json'
    # JSON Bulk File is large, and must be processed in chunks. 
    # Optimal chunk size can be tested/configured later.
    with requests.get(scryfall_bulk_data_url, stream=True) as resp:
        with open(output_file, 'wb') as file:
            for chunk in resp.iter_content(chunk_size=8192): 
                file.write(chunk)
    return output_file