import requests
import time

def calculate_hp(base_hp):
    return ((2 * base_hp) * 100 // 100) + 100 + 10

def calculate_stat(base_stat):
    return (2 * base_stat * 100 // 100) + 5

def get_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data for {pokemon_name}")
        return None
    
    data = response.json()
    stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
    
    return {
        'name': pokemon_name.capitalize(),
        'hp': calculate_hp(stats['hp']),
        'attack': calculate_stat(stats['attack']),
        'defense': calculate_stat(stats['defense']),
        'speed': calculate_stat(stats['speed'])
    }

def display_battle_start(pokemon1, pokemon2):
    print("\n=== Pokémon Battle Start! ===")
    print(f"{pokemon1['name']} vs {pokemon2['name']}")
    print(f"{pokemon1['name']} HP: {pokemon1['hp']}")
    print(f"{pokemon2['name']} HP: {pokemon2['hp']}\n")

def calculate_damage(attacker, defender):
    # Simple damage calculation: (Attack / Defense) * 10
    damage = (attacker['attack'] / defender['defense']) * 10
    return max(1, int(damage))  # Minimum 1 damage

def battle_simulation(pokemon1_name, pokemon2_name):
    # Step 1: Fetch Pokémon Data
    pokemon1 = get_pokemon_data(pokemon1_name)
    pokemon2 = get_pokemon_data(pokemon2_name)
    
    if not pokemon1 or not pokemon2:
        return
    
    # Step 2: Calculate Initial Stats (already done in get_pokemon_data)
    
    # Step 3: Initialize Battle Display
    display_battle_start(pokemon1, pokemon2)
    
    # Step 4: Determine First Attacker
    if pokemon1['speed'] >= pokemon2['speed']:
        attacker, defender = pokemon1, pokemon2
    else:
        attacker, defender = pokemon2, pokemon1
    
    # Step 5: Battle Loop
    round_num = 1
    while pokemon1['hp'] > 0 and pokemon2['hp'] > 0:
        print(f"Round {round_num}")
        
        # Calculate and deal damage
        damage = calculate_damage(attacker, defender)
        defender['hp'] -= damage
        
        # Display attack results
        print(f"{attacker['name']} attacks {defender['name']} for {damage} damage!")
        
        # Check if defender fainted
        if defender['hp'] <= 0:
            defender['hp'] = 0
            print(f"{defender['name']} has fainted!")
            break
        
        # Display remaining HP
        print(f"{pokemon1['name']} HP: {pokemon1['hp']}")
        print(f"{pokemon2['name']} HP: {pokemon2['hp']}\n")
        
        # Swap roles
        attacker, defender = defender, attacker
        round_num += 1
        time.sleep(1)  # Add delay for readability
    
    # Step 6: End Battle
    winner = pokemon1 if pokemon1['hp'] > 0 else pokemon2
    print("\n=== Battle Ended! ===")
    print(f"{winner['name']} wins!")
    print(f"Final HP: {winner['hp']}")

# Example usage
if __name__ == "__main__":
    battle_simulation("pikachu", "charmander")
