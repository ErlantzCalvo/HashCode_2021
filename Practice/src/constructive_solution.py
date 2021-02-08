#!/usr/bin/env python3

import sys

def read_input(filename):
    pizzas = []
    teams = {2: None, 3: None, 4:None}
    
    f = open(filename, "r")
    first_line = f.readline().rstrip('\n').split(' ')
    n_pizzas = int(first_line[0])
    
    for i in [1, 2, 3]:
        teams[i + 1] = int(first_line[i])
    
    while True:
        line = f.readline()
        if line == "":
            break
        pizzas.append(line.rstrip('\n').split(' ')[1:])
    
    f.close()
    if len(pizzas) != n_pizzas:
        raise ValueError(f"Number of read pizzas ({len(pizzas)}) does not equal expected number of pizzas ({n_pizzas}).")

    return pizzas, teams

def write_output(filename, deliveries, n_deliveries):
    f = open(filename, "w")
    f.write(f"{n_deliveries}\n")

    for i in range(len(deliveries)):
        for j in range(len(deliveries[i])):
            f.write(f"{i + 2}")
            for p in deliveries[i][j]:
                f.write(f" {p}")
            f.write("\n")
    
    f.close()

def heuristic_sort(pizzas, ingredient_set):
    global pizza_database
    pizza_map = []
    for i in pizzas:
        heuristic_value = 0
        for j in pizza_database[i]:
            heuristic_value += -0.5 if j in ingredient_set else 1
        pizza_map.append((i, heuristic_value))
    
    sorted_pizzas = sorted(pizza_map, key=lambda x: x[1], reverse=True)
    return [x[0] for x in sorted_pizzas]

def get_delivery_team_index(deliveries, teams):
    for i in reversed(range(len(deliveries))):
        if len(deliveries[i]) < teams[i + 2]:
            return i, i + 2
    return None, None

'''
Algorithm intuition: Generate deliveries for 4-member teams, 
                     then 3-member ones and finally 2-member teams.

    1. Sort pizzas according to most non-used & non-overlapping ingredients.
    2. Select the first pizza in the sorted list and assign it to a team.
    3. Repeat until every team is delivered or no more pizza left.
'''
def solve(pizzas, teams):
    global pizza_database
    deliveries = [[], [], []]
    used_ingredients = set()
    n_deliveries = 0
    n_teams = 0
    
    for i in teams.keys():
        n_teams += teams[i]
    
    while (n_deliveries < n_teams and len(pizzas) > 0):
        current_delivery = []
        delivery_index, pizza_amount = get_delivery_team_index(deliveries, teams)
        
        if delivery_index is None:
            break

        while (len(current_delivery) < pizza_amount and len(pizzas) > 0):
            pizzas = heuristic_sort(pizzas, used_ingredients)
            current_delivery.append(pizzas[0])
            for i in pizza_database[pizzas[0]]:
                used_ingredients.add(i)
            pizzas = pizzas[1:]
        deliveries[delivery_index].append(current_delivery)
        n_deliveries += 1
    
    return deliveries, n_deliveries

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError("Filename needs to be passed as command-line argument.")

    filename = sys.argv[1]
    pizza_database, teams = read_input(filename)
    deliveries, n_deliveries = solve(list(range(len(pizza_database))), teams)

    if ".in" in filename:
        filename = filename.replace('.in', '.out')
    else:
        filename += ".out"

    write_output(filename, deliveries, n_deliveries)
