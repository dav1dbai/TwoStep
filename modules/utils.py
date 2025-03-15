DOMAINS = [ ## .nl not changed for multi excpet gripper, since planner doesnt use it
    "barman",
    "blocksworld",
    # "floortile",
    # "storage",
    "termes",
    "tyreworld",
    "grippers",
    "barman-multi",
    "barman-enabled",
    "blocksworld-multi",
    "termes-multi",
    "tyreworld-multi",
    "tyreworld-enabled",
    "grippers-multi",
]

def get_cost(x):
    splitted = x.split()
    counter = 0
    found = False
    cost = 1e5
    for i, xx in enumerate(splitted):
        if xx == "cost":
            counter = i
            found = True
            break
    if found:
        cost = float(splitted[counter+2])
    return cost