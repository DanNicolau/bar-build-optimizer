import time
import datetime
from typing import List, Dict
import random
import BuildOrder
from Entity import Entity
from starting_solution import generate_starting_solution



#varies the solution in a small way, this must return a copy of the input, not a reference to the same object passed in
def vary_solution():
    raise NotImplementedError()

def evaluate():
    raise NotImplementedError()

def acceptance_probability(candidate_solution, current_solution, temperature, build_options):

    e = evaluate(solution)

    raise NotImplementedError()

def optimize(starting_entities_input: Dict, desired_entities: List, build_options: Dict):

    #convert starting entities to a list of strings that we keep as a dict for god knows what reason
    starting_entities = []
    for ent_id, ent in starting_entities_input.items():
        starting_entities.append(ent.id_string)

    # best_solution = generate_starting_solution() # can play with this instead to see if current solution is very far from best seen however a learning curve might be more informational
    current_solution = generate_starting_solution(starting_entities, desired_entities, build_options)

    raise NotImplementedError()

    start_time = time.time()
    end_time = time.time() + build_options['search_time']

    total_seconds = end_time - start_time
    
    iterations = 0
    while time.time() < end_time:
        temperature = float(end_time - time.time()) / total_seconds
        candidate_solution = vary_solution(current_solution)

        if (acceptance_probability(candidate_solution, current_solution, temperature, build_options) >= random.random()):
            current_solution = candidate_solution

        iterations += 1

    #we have an optimized build order now