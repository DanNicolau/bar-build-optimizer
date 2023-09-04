import copy
from simulated_annealing.initial_solution import generate
from simulated_annealing.vary import vary

def optimize(desired_entities, starting_entities, build_options):

    current_solution = generate(starting_entities, build_options)

    done = False

    while not done:
        variation = vary(current_solution, starting_entities, build_options)

