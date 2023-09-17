from simulated_annealing.utils import entity_counts
from collections import namedtuple

# def is_valid_solution(solution, desired_entities):

#     desired_entities_counts = entity_counts(desired_entities)

#     running_ent_count = {}

#     for action in solution:
#         if action.entity in desired_entities:
#             if not action.entity in running_ent_count:
#                 running_ent_count[action.entity] = 1
#                 if action.type != 'build':
#                     raise ValueError()
#             else:
#                 running_ent_count[action.entity] += 1 if action.type == 'build' else -1

#     for d in desired_entities_counts:
#         if not d in running_ent_count:
#             return False
#         if running_ent_count[d] < desired_entities_counts[d]:
#             return False
#     return True

# def time_to_complete_actions(actions, starting_entities, build_options):
#     time = 0
#     resources = {
#         'metal': min( build_options['base_metal_storage'], build_options['starting_metal']),
#         'energy': min( build_options['base_energy_storage'], build_options['starting_energy']),
#         'entities': generate_current_entities(actions, starting_entities, build_options)
#     }

#     for action in actions:
#         time += 1
#         # print(resources)

#     return time

# # lower is better
# def evaluate(solution, desired_entities, starting_entities, build_options):

#     if not is_valid_solution(solution, desired_entities):
#         return 4294967295.0 # arbitrarily large numb

#     return time_to_complete_actions(solution, starting_entities, build_options)

#     time_to_build = 0
#     # for action in solution:
#     #     time_to_build += time_to_complete_action(action)


#     return time_to_build

# # greedy for now
# # theres room to further optimize by caching the score of the previous best solution
# def accept(current_solution_score, proposed_solution, desired_entities, starting_entities, build_options):

#     proposed_solution_score = evaluate(proposed_solution, desired_entities, starting_entities, build_options)

#     if proposed_solution_score <= current_solution_score:
#         return True, proposed_solution_score
#     else:
#         return False, proposed_solution_score