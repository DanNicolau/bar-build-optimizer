import copy
from simulated_annealing.utils import print_actions
from simulated_annealing.initial_solution import generate
from simulated_annealing.vary import vary
from simulated_annealing.evaluate import accept, evaluate

def optimize(desired_entities, starting_entities, build_options):

    current_solution = generate(starting_entities, build_options)

    done = False
    iterations = 0

    while not done:
        variation = vary(current_solution, starting_entities, build_options)

        best_score = evaluate(current_solution, desired_entities)

        iterations += 1

        is_variation_better, variation_score = accept(best_score, variation, desired_entities, build_options)
        if is_variation_better:
            current_solution = variation
            best_score = variation_score

        if iterations == 50:
            done = True

    print('after 50 iters:')
    print_actions(current_solution)
    print(f'cost: {best_score} seconds')