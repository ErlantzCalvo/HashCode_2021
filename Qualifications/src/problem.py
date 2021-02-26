#!/usr/env/bin python3

import sys
import math
import numpy as np

street_map = {} # id = street name -> value = street id number
id2street = [] # street objects indexed by their id
inter_list = [] # list of intersections, at each position a dictionary 
                # key is incoming street id, value is traffic light time
car_dict = {}
street_density = {}
traffic_ligths = []
traffic_order = []
current_timestamp = 0

D = 0 # time of simulation
I = 0 # amount of intersections
S = 0 # amount of streets
V = 0 # amount of cars
F = 0 # bonus points

def write_output(filename):
    global inter_list
    f = open(filename, "w")
    f.write(f"{len(inter_list) - inter_list.count(None)}\n")
    for idx in range(len(inter_list)):
        if inter_list[idx] is not None:
            f.write(f"{idx}\n{len(inter_list[idx])}\n")
            for key, value in inter_list[idx].items():
                f.write(f"{id2street[key].name} {value}\n")
    f.close()

class Car:
    def __init__(self):
        self.id = None
        self.streets = []
        self.remaining = 0
    
    def read_input(self,line):
        global street_map
        global id2street
        global car_dict
        global street_density
        
        car_info = line.rstrip('\n').split(' ')
        self.id = len(car_dict)
        for i in car_info[1:]:
            self.streets.append(street_map[i])
            
            car_dict[self.id] = self
            if street_map[i] in street_density:
                street_density[street_map[i]] += 1
            else:
                street_density[street_map[i]] = 1

        id2street[self.streets[0]].queue.append(self.id)
        
        
class Street:
    def __init__(self):
        self.id = None
        self.name = ""
        self.start = None
        self.end = None
        self.time = None
        self.queue = []
        
    def read_input(self, line):
        global street_map
        global id2street
        global inter_map
        
        street_info = line.rstrip('\n').split(' ')
        self.name = street_info[2]
        self.start = int(street_info[0])
        self.end = int(street_info[1])
        self.time = int(street_info[3])

        self.id = len(street_map)
        street_map[self.name] = self.id
        id2street.append(self)

        inter_list[self.end][self.id] = None

def solve_silly():
    for dt in inter_list:
        for key in dt.keys():
            dt[key] = 1

def solve_densities():
    global inter_list
    for idx in range(len(inter_list)):
        gcd = None
        
        for street_id, _ in inter_list[idx].items():
            if gcd is None and street_id in street_density:
                gcd = street_density[street_id]
            elif street_id in street_density:
                gcd = math.gcd(gcd, street_density[street_id])

        if gcd is None:
            inter_list[idx] = None
        else:
            new_dict = dict()
            for street in inter_list[idx].keys():
                if street in street_density:
                    new_dict[street] = street_density[street] // gcd
            inter_list[idx] = new_dict

def next_traffic(intersection_id, current_traffic):
    return traffic_order[intersection_id][(traffic_order[intersection_id].index(current_traffic) + 1) % len(traffic_order[intersection_id])]

def step_simulation():
    global traffic_lights, id2street, current_timestamp, car_dict
    new_car_dict = {}

    for car_idx, car in car_dict.items():
        if len(car.streets) > 0: # If there are streets to go
            new_car_dict[car_idx] = car
            current_street = id2street[car.streets[0]]
            # print(f"{current_street.name} -> {current_street.id}: intersection {current_street.end} {traffic_ligths[current_street.end]}")
            if len(current_street.queue) > 0 and current_street.queue[0] == car_idx and \
                traffic_ligths[current_street.end][0] == current_street.id:
                current_street.queue.pop(0)
                del car.streets[0]
                if len(car.streets) > 0:
                    car.remaining = id2street[car.streets[0]].time
            elif car_idx not in current_street.queue:
                car.remaining -= 1
                if car.remaining == 0:
                    current_street.queue.append(car_idx)

    for i in range(len(traffic_ligths)):
        if traffic_ligths[i] is not None:
            traffic_ligths[i][1] -= 1
            if traffic_ligths[i][1] <= 0:
                next_traffic_l = next_traffic(i, traffic_ligths[i][0])
                traffic_ligths[i][0] = next_traffic_l
                traffic_ligths[i][1] = inter_list[i][next_traffic_l]

    car_dict = new_car_dict
    current_timestamp += 1

def run_simulation():
    global D
    for i in range(D):
        step_simulation()
    
if __name__ == "__main__":

    f = open(sys.argv[1], "r")
    first_line = f.readline().rstrip('\n').split(' ')
    D = int(first_line[0])
    I = int(first_line[1])
    S = int(first_line[2])
    V = int(first_line[3])
    F = int(first_line[4])
    
    # intersections init
    inter_list = [ {} for i in range(I) ]
    
    # streets
    for i in range(int(S)):
        street = Street()
        street.read_input(f.readline())
    
    # cars
    for j in range(int(V)):
        car = Car()
        car.read_input(f.readline())

    # solve_silly()
    solve_densities()
    # car_dict_backup = car_dict

    # # Init traffic lights orders
    # for i in range(len(inter_list)):
    #     if inter_list[i] is not None:
    #         traffic_order.append(np.random.permutation(list(inter_list[i].keys())).tolist())
    #         traffic_ligths.append([traffic_order[-1][0], inter_list[i][traffic_order[-1][0]]])
    #     else:
    #         traffic_order.append(None)
    #         traffic_ligths.append(None)
    # run_simulation()
    # score = V - len(car_dict)

    write_output(sys.argv[1].replace(".in", ".out"))






