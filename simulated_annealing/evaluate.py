from simulated_annealing.utils import entity_counts, update_counts
from collections import namedtuple

# THIS HAS A BUG

def is_valid(solution, starting_entities, desired_entities):
    
    final_counts = entity_counts(starting_entities)
    #get final counts
    for action in solution:
        update_counts(final_counts, action)

    for dent in desired_entities:
        if not dent in final_counts:
            return False
        elif final_counts[dent] < desired_entities[dent]:
            return False

    return True

def time_to_complete_actions(actions, starting_entities, build_options):
    time = 0

    return len(actions)
    return time

# lower is better
def evaluate(solution, desired_entities, starting_entities, build_options):

    if not is_valid(solution, starting_entities, desired_entities):
        return 4294967295.0 # arbitrarily large num

    return time_to_complete_actions(solution, starting_entities, build_options)

# # greedy for now
# # theres room to further optimize by caching the score of the previous best solution
# def accept(current_solution_score, proposed_solution, desired_entities, starting_entities, build_options):

#     proposed_solution_score = evaluate(proposed_solution, desired_entities, starting_entities, build_options)

#     if proposed_solution_score <= current_solution_score:
#         return True, proposed_solution_score
#     else:
#         return False, proposed_solution_score