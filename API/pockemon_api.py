#%%
import requests

# %%
base_url = 'https://pokeapi.co/api/v2/'

def get_pokemon_info(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)
    print(response)
    '''
    Informational responses (100 - 199)
    Successful responses (200 - 299)
    Redirection messages (300 - 399)
    Client error responses (400 - 499)
    Server error responses (500 - 599)
    '''

    if response.status_code == 200:
        pokemon_data = response.json() #convert to jason format
        return pokemon_data #gives all data as a dictionary
    else:
        print(f"Failed to get data {response.status_code}")


pokemon_name = 'pikachu'
pokemon_info = get_pokemon_info(pokemon_name)

if pokemon_info: #if exists
    print(f"Name: {pokemon_info['name']}")
    print(f"ID: {pokemon_info['id']}")
    print(f"Height: {pokemon_info['height']}")
