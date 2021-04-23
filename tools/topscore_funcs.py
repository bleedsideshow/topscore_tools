"""This script provides functions to retrieve a list of players for a given TopScore site"""
import json
import pathlib
import subprocess
import csv
from math import ceil

# CHANGE THESE
CONFIG_FILENAME = "/home/kevin/bulblytics/pada/config.yml"
DATA_PATH = "/home/kevin/bulblytics/pada/data/"

PAGE_LIMIT = 100

def parse_config(config_filename: str) -> dict:
    """Reads configuration file, parses it, and returns a dictionary of string variables

    Args:
        config_filename (str): path to configuration file with parameters for accessing TopScore API

    Returns:
        list: a dictionary of configuration parameters
    """
    config_file = open(config_filename, 'r')
    return {
        'auth_url' : config_file.readline().rstrip(),
        'client_id' : config_file.readline().rstrip(),
        'client_secret' : config_file.readline().rstrip(),
        'username' : config_file.readline().rstrip(),
        'password' : config_file.readline().rstrip(),
    }

def run_query(config: dict, query: str) -> dict:
    """Runs a query through TopScore API using parameters stored in config

    Args:
        config (dict): a dictionary of configuration parameters for connecting to TopScore's API
        query (str): a query to run

    Returns:
        dict: A JSON-formatted dictionary with the resulting query
    """
    api_script = str(pathlib.Path(__file__).parent.absolute()) + "/tools/topscore_api.sh"
    json_str = subprocess.check_output(' '.join([api_script, config['auth_url'], config['client_id'],
                                                 config['client_secret'], config['username'], config['password'],
                                                 query]), shell = True)
    json_obj = json.loads(json_str)
    return json_obj

def save_query(config: dict, query: str, filename: str):
    """Runs a query through TopScore API using parameters stored in config

    Args:
        config (dict): a dictionary of configuration parameters for connecting to TopScore's API
        query (str): a query to run
        filename (str): the string filepath to redirect the filepath

    Returns:
        dict: A JSON-formatted dictionary with the resulting query
    """
    api_script = str(pathlib.Path(__file__).parent.absolute()) + "/tools/topscore_api.sh"
    sys_args = [api_script, config['auth_url'], config['client_id'], config['client_secret'],
                config['username'], config['password'], query]
    with open(filename, 'w') as outfile:
        subprocess.run(sys_args, stdout = outfile)

def get_products(config: dict) -> list:
    """Retrieves list of products

    Args:
        config (dict): a dictionary of configuration parameters for connecting to TopScore's API

    Returns:
        list: a list of dictionary items representing TopScore products
    """
    # Change in future to use wrapper function
    num_products_json = run_query(config, 'products?site_list_scope=network&per_page=1')
    num_products = num_products_json['count']
    num_product_pages = ceil(num_products / PAGE_LIMIT)
    for page in range(num_product_pages):
        json_file = DATA_PATH + "productsPage" + str(page+1).zfill(5) + ".json"
        save_query(config, 'products?site_list_scope=network&fields=ProductVariations&per_page=' +
                   str(PAGE_LIMIT) + '&page=' + str(page+1),
                   json_file)
    products_to_return = []
    # Investigate why products being added (1851 total instead of 1835 in json)
    for page in range(num_product_pages):
        products_json_file = DATA_PATH + "productsPage" + str(page + 1).zfill(5) + ".json"
        with open(products_json_file) as f:
            products_json = json.load(f)
        products_list = products_json['result']
        for product in products_list:
            if product['ProductVariations'] == []:
                parent_product_id = product['id']
            else:
                parent_product_id = product['ProductVariations'][0]['family_product_id']
            products_to_return.append({
                    'product': product['name'],
                    'product_id': product['id'],
                    'parent_product_id': parent_product_id,
                    'cost': product['cost'],
                })
    # Add year to products
    return products_to_return

def write_products_to_file(products_filename: str):
    """Calls get_products and writes result to output file

    Args:
        products_filename (str): The path to the output file for the product names
    """
    config = parse_config(CONFIG_FILENAME)
    products = get_products(config)
    with open(products_filename, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, products[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(products)

def get_players(config: dict) -> list:
    """Retrieves list of players

    Args:
        config (dict): a dictionary of configuration parameters for connecting to TopScore's API

    Returns:
        list: a list of dictionary items representing players
    """
    # Change in future to use wrapper function
    num_players_json = run_query(config, 'persons?per_page=1')
    num_players = num_players_json['count']
    num_player_pages = ceil(num_players / PAGE_LIMIT)
    for page in range(num_player_pages):
        json_file = DATA_PATH + "playersPage" + str(page+1).zfill(5) + ".json"
        save_query(config, 'persons?fields=Location&per_page=' + str(PAGE_LIMIT) + '&page=' + str(page+1),
                   json_file)
    players_to_return = []
    for page in range(num_player_pages):
        players_json_file = DATA_PATH + "playersPage" + str(page + 1).zfill(5) + ".json"
        with open(players_json_file) as f:
            players_json = json.load(f)
        players_list = players_json['result']
        for player in players_list:
            try:
                zip = player['Location']['postal_code']
            except (KeyError, TypeError):
                zip = "unknown"
            # Pad zeroes to zip codes and reduce to 5 digits
            try:
                birth_date = player['birth_date']
            except (KeyError, TypeError):
                birth_date = "unknown"
            try:
                email = player['email_address']
            except (KeyError, TypeError):
                email = "unknown"
            players_to_return.append({
                'player_id': player['id'],
                'email': email,
                'first_name': player['first_name'],
                'last_name': player['last_name'],
                'full_name': player['full_name'],
                'gender': player['gender'],
                'birth_date': birth_date,
                'zip': zip,
            })
    return players_to_return

def write_players_to_file(players_filename: str):
    """Calls get_players and writes result to output file

    Args:
        players_filename (str): The path to the output file for the player names
    """
    config = parse_config(CONFIG_FILENAME)
    players = get_players(config)
    with open(players_filename, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, players[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(players)
