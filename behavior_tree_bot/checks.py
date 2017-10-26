import planet_wars

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def is_enemy_trying_for_leave_one_attack(state : planet_wars.PlanetWars):
    enemy_fleets = state.enemy_fleets()
    if not enemy_fleets: return False
    for fleet in enemy_fleets:
        fleet_dest = state.planets[fleet.destination_planet]
        fleet_dest_diff = fleet.num_ships - fleet_dest.num_ships
        if fleet_dest_diff < 5:
            return True
    return False
