import requests

def get_pokemon_data(name):
    """Fetch Pokémon data from PokeAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get data for {name}")

def calculate_stat(base, level):
    """Calculate general stat (attack/defense/speed)."""
    return int(((2 * base) * level / 100) + 5)

def calculate_hp(base, level):
    """Calculate HP."""
    return int(((2 * base) * level / 100) + level + 10)

def extract_stats(pokemon_json, level):
    stats = {}
    for stat in pokemon_json["stats"]:
        name = stat["stat"]["name"]
        base = stat["base_stat"]
        if name == "hp":
            stats["hp"] = calculate_hp(base, level)
        elif name == "attack":
            stats["attack"] = calculate_stat(base, level)
        elif name == "defense":
            stats["defense"] = calculate_stat(base, level)
        elif name == "speed":
            stats["speed"] = calculate_stat(base, level)
    return stats

def simulate_battle(name1, name2, level=50):
    print(f"\n⚔️ Battle Start: {name1} vs {name2} at level {level} ⚔️")

    poke1_data = get_pokemon_data(name1)
    poke2_data = get_pokemon_data(name2)

    stats1 = extract_stats(poke1_data, level)
    stats2 = extract_stats(poke2_data, level)

    print(f"{name1} stats: {stats1}")
    print(f"{name2} stats: {stats2}")

    hp1, hp2 = stats1["hp"], stats2["hp"]

    if stats1["speed"] > stats2["speed"]:
        attacker, defender = name1, name2
        att_stats, def_stats = stats1, stats2
        att_hp, def_hp = hp1, hp2
    else:
        attacker, defender = name2, name1
        att_stats, def_stats = stats2, stats1
        att_hp, def_hp = hp2, hp1

    print(f"\n🕐 {attacker} is faster and attacks first!\n")

    round_num = 1
    while att_hp > 0 and def_hp > 0:
        print(f"🔁 Round {round_num}")
        damage = max(1, att_stats["attack"] - def_stats["defense"])
        def_hp -= damage
        print(f"{attacker} attacks {defender} for {damage} damage.")
        print(f"{defender} HP left: {max(def_hp, 0)}\n")

        if def_hp <= 0:
            print(f"🏆 {defender} fainted. {attacker} wins in {round_num} rounds!")
            return

        # Swap attacker and defender
        attacker, defender = defender, attacker
        att_stats, def_stats = def_stats, att_stats
        att_hp, def_hp = def_hp, att_hp
        round_num += 1

# Example run (can be replaced with input() for custom battles)
simulate_battle("pikachu", "bulbasaur", level=50)
