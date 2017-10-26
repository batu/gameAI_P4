import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)



def spread_to_weak(state):
    try:
        my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)
        strongest = max(my_planets, key= lambda p: p.num_ships)

        neutral_planets = [planet for planet in state.neutral_planets()
                          if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets()) and
                           not any(fleet.destination_planet == planet.ID for fleet in state.enemy_fleets())]

        if not (neutral_planets[0].num_ships < (strongest.num_ships / 4)):
            return False

        for planet in neutral_planets:
            if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets()):
                my_planet = my_planets[0]
                target_planet = planet
                required_ships = target_planet.num_ships + 1
                if my_planet.num_ships > required_ships:
                    return issue_order(state, my_planet.ID, target_planet.ID, required_ships)
    except:
        return False
    return False


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    #if len(state.my_fleets()) >= 1:
        #return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    enemy_planets = sorted(state.enemy_planets(), key=lambda p: p.num_ships)
    # (3) Find the weakest enemy planet.
    for e_planet in enemy_planets:
        if not any(fleet.destination_planet == e_planet.ID for fleet in state.my_fleets()):
            weakest_planet = e_planet

            if not strongest_planet or not weakest_planet:
                # No legal source or destination
                return False
            else:
                # (4) Send half the ships from my strongest planet to the weakest enemy planet.

                dist = state.distance(strongest_planet.ID, weakest_planet.ID)
                growth_rate = weakest_planet.growth_rate
                num_ships = dist * growth_rate + weakest_planet.num_ships + 2
                return issue_order(state, strongest_planet.ID, weakest_planet.ID, num_ships)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest netural planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def abuse_leave_one(state):
    enemy_fleets = state.enemy_fleets()
    for fleet in enemy_fleets:
        fleet_dest = state.planets[fleet.destination_planet]
        fleet_dest_diff = fleet.num_ships - fleet_dest.num_ships
        if fleet_dest_diff < 5:
            source_planet = find_closest_allied_planet(state, fleet_dest)
            source_target_distance = state.distance(source_planet.ID, fleet_dest.ID)
            fleet_target_distance = fleet.turns_remaining
            our_fleet_dests = [state.planets[fleet.destination_planet] for fleet in state.my_fleets()]
            if fleet_dest in our_fleet_dests:
                return False
            if source_target_distance == 1 + fleet_target_distance:
                return issue_order(state, source_planet.ID, fleet_dest.ID, 10)
    return False


###### HELPER FUNCTIONS ######
def find_closest_allied_planet(state, planet):
    my_planets = state.my_planets()
    closest_planet = None
    closest_distance = 999999999
    for my_planet in my_planets:
            curr_dist = state.distance(planet.ID, my_planet.ID)
            if curr_dist < closest_distance:
                closest_planet = my_planet
    return closest_planet
