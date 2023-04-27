def reconstruct_path(path_costs, parents, best_hash):
    print('RECONSTRUCTING')

    path = []

    done = False
    hash_ptr = best_hash
    while hash_ptr != None:
        path.append(f' {hash_ptr}:{path_costs[hash_ptr]}')
        hash_ptr = parents[hash_ptr]

    path.reverse()
    
    return path

def find_added_element(list1, list2):
    for i in range(len(list1)):
        if i >= len(list2) or list1[i] != list2[i]:
            return list2[i]
    return list2[-1]

def print_build_order_delta(arr):
    prev = []
    result = []
    for elem in arr:
        parts = elem.split(':')
        buildings = parts[0].split(',')
        added_entity = find_added_element(prev, buildings)
        prev = buildings
        print(f'{float(parts[1]):.2f}:\t{added_entity}')