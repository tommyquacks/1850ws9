import requests
import random

def calculate_hp(base_hp):
    """Calculate HP based on base stat."""
    return base_hp + 50

def calculate_stat(base_stat):
    """Calculate attack, defense, or speed based on base stat."""
    return base_stat + 10

def fetch_pokemon_data(pokemon_name):
    """Fetch Pokémon data from PokeAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching data for {pokemon_name}: {response.status_code}")
        return None
    return response.json()

def get_pokemon_stats(pokemon_data, pokemon_name):
    """Extract and calculate stats from Pokémon data."""
    if not pokemon_data:
        return None
    stats = pokemon_data['stats']
    base_hp = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'hp')
    base_attack = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'attack')
    base_defense = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'defense')
    base_speed = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'speed')
    
    return {
        'name': pokemon_name.capitalize(),
        'hp': calculate_hp(base_hp),
        'attack': calculate_stat(base_attack),
        'defense': calculate_stat(base_defense),
        'speed': calculate_stat(base_speed)
    }

def calculate_damage(attacker, defender):
    """Calculate damage dealt by attacker to defender."""
    base_damage = attacker['attack'] - (defender['defense'] // 2)
    return max(1, base_damage)  # Ensure at least 1 damage

def battle_simulation(pokemon1_name, pokemon2_name):
    """Simulate a Pokémon battle."""
    # Fetch Pokémon data
    pokemon1_data = fetch_pokemon_data(pokemon1_name)
    pokemon2_data = fetch_pokemon_data(pokemon2_name)
    
    if not pokemon1_data or not pokemon2_data:
        print("Battle cannot proceed due to missing Pokémon data.")
        return
    
    # Calculate stats
    pokemon1 = get_pokemon_stats(pokemon1_data, pokemon1_name)
    pokemon2 = get_pokemon_stats(pokemon2_data, pokemon2_name)
    
    if not pokemon1 or not pokemon2:
        print("Battle cannot proceed due to invalid stats.")
        return
    
    # Initialize battle display
    print(f"\n=== {pokemon1['name']} vs {pokemon2['name']} ===")
    print(f"{pokemon1['name']} HP: {pokemon1['hp']}")
    print(f"{pokemon2['name']} HP: {pokemon2['hp']}\n")
    
    # Determine first attacker
    if pokemon1['speed'] > pokemon2['speed']:
        attacker, defender = pokemon1, pokemon2
    elif pokemon2['speed'] > pokemon1['speed']:
        attacker, defender = pokemon2, pokemon1
    else:
        # Randomly choose if speeds are equal
        attacker, defender = random.choice([(pokemon1, pokemon2), (pokemon2, pokemon1)])
    
    print(f"{attacker['name']} is faster and attacks first!\n")
    
    # Battle loop
    round_count = 1
    while pokemon1['hp'] > 0 and pokemon2['hp'] > 0:
        print(f"--- Round {round_count} ---")
        
        # Calculate and apply damage
        damage = calculate_damage(attacker, defender)
        defender['hp'] = max(0, defender['hp'] - damage)
        
        print(f"{attacker['name']} deals {damage} damage to {defender['name']}!")
        
        # Check if defender fainted
        if defender['hp'] <= 0:
            print(f"{defender['name']} has fainted!")
            break
        
        # Display remaining HP
        print(f"{pokemon1['name']} HP: {pokemon1['hp']}")
        print(f"{pokemon2['name']} HP: {pokemon2['hp']}\n")
        
        # Swap roles
        attacker, defender = defender, attacker
        round_count += 1
    
    # End battle
    winner = pokemon1 if pokemon1['hp'] > 0 else pokemon2
    print(f"\n=== Battle Over ===")
    print(f"{winner['name']} wins with {winner['hp']} HP remaining!")

if __name__ == "__main__":
    # Example usage
    battle_simulation("pikachu", "charmander")
