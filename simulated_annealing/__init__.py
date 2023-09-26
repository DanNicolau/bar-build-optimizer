from copy import copy
from simulated_annealing.utils import print_actions
from simulated_annealing.initial_solution import generate
from simulated_annealing.vary import vary
from simulated_annealing.evaluate import evaluate

def optimize(desired_entities, starting_entities, build_options):
    current_solution = generate(starting_entities, build_options)

    done = False
    iterations = 0
    current_solution = vary(current_solution, starting_entities, build_options)
    best_score = evaluate(current_solution, desired_entities, starting_entities, build_options)

    while not done:

        variation = vary(current_solution, starting_entities, build_options)
        variation_score = evaluate(variation, desired_entities, starting_entities, build_options)

        print(f'{iterations}\t{best_score}\t{variation_score}')

        if variation_score <= best_score:
            current_solution = variation
            best_score = variation_score

        iterations += 1


        if iterations == 10000:
            done = True

    print('after 100 iters:')
    print_actions(current_solution)
    print(f'time: {best_score}')
