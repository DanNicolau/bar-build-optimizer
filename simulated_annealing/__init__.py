import copy
from simulated_annealing.initial_solution import generate
from simulated_annealing.vary import vary

def optimize(desired_entities, starting_entities, build_options):

    current_solution = generate(starting_entities, build_options)

    done = False
    iterations = 0

    while not done:
        variation = vary(current_solution, starting_entities, build_options)
        iterations += 1

        current_solution = variation

        if iterations == 50:
            done = True

    print('after 50 iters:')
    print(current_solution)
