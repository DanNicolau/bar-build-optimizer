import TeamState
import Cost

def remove_previous_path(costs_arr, parents_arr, cost_to_remove):
    idx = costs_arr.index(cost_to_remove)
    costs_arr.pop(idx)
    parents_arr.pop(idx)

def remove_inferior_goal(goals, goal_to_remove):
    print(f'removing inferior goal: {goal_to_remove}')
    print(f'goals: {goals}')

    goals.remove(goal_to_remove)


def handle_found_goal(new_goal: TeamState, new_goal_cost: Cost, goals: list):
    #if the goal is dominated, return fail
    #if the goal dominates another, excise the other from goals list
    #update global cost limit

    for i in range(len(goals)):
        existing_goal, existing_goal_cost = goals[i]
        if new_goal_cost.is_dominated_by(existing_goal_cost):
            print(f'goal found was inferior')
            return
        elif existing_goal_cost.is_dominated_by(new_goal_cost):
            print(f'goal {new_goal} has beat {existing_goal}')
            remove_inferior_goal(goals, goals[i])

    goals.append((new_goal, new_goal_cost))