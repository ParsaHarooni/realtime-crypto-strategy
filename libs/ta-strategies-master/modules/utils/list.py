def list_of_element_occurrences(l:list,element:any):
    indices = [i for i, x in enumerate(l) if x == element]
    return indices

# map 2d list
def map_2d_lists(inputs, map_fn):
    return list(map(map_fn, inputs))
