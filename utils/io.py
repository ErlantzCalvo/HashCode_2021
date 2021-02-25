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
    
def read_input_qualification(filename):
    f = open(filename, "r")

    # TODO: fill me

    return None

def write_output_qualification(filename, *args):
    f = open(filename, "w")

    # TODO: fill me

    pass