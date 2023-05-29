import time
import datetime
from typing import List, Dict
import random
from BuildOrder import BuildOrder
from Entity import Entity
from starting_solution import generate_starting_build
from vary import vary_solution
from evaluate import evaluate
from Solution import Solution
import math

inf = float('inf')

def acceptance_probability(candidate_solution: Solution, current_solution: Solution, temperature: float, build_options: Dict):

    evaluate(candidate_solution, build_options)
    candidate_score = candidate_solution.score
    current_score = current_solution.score

    if candidate_score >= current_score:
        return 1.0
    else:
        return math.exp( -(candidate_score - current_score) / temperature )

def optimize(starting_entities_input: Dict, desired_entities: List, build_options: Dict):

    #convert starting entities to a list of strings that we keep as a dict for god knows what reason
    starting_entities = []
    for ent_id, ent in starting_entities_input.items():
        starting_entities.append(ent.id_string)

    # a good starting solution might not even be necessary..., we can just keep inserting until a time can be calculated, otherwise inf if prod neg or no builder
    starting_solution = Solution(
        build_order = generate_starting_build(starting_entities, desired_entities, build_options),
        score = inf)
    
    current_solution = starting_solution # .copy() ??

    start_time = time.time()
    end_time = time.time() + build_options['search_time']
    total_seconds = end_time - start_time
    iterations = 0
    while time.time() < end_time:
        temperature = float(end_time - time.time()) / total_seconds
        candidate_solution = vary_solution(current_solution, build_options)

        if (acceptance_probability(candidate_solution, current_solution, temperature, build_options) >= random.random()):
            current_solution = candidate_solution

        iterations += 1

    #we have an optimized build order now