from general_utils.dictionary import dictionaries_intersect


def count_leaves_of_tree(tree, this_level='<ROOT>', count_type='all'):
    """
    Given a tree defined as a dictionary of lists or dicts, returns the number of leaves under each node

    Args:
        tree (dict): Tree defined as either:
                dict of lists of keys that refer back to the original dict, eg:
                    {'<ROOT>': ['1', '2'],
                     '1': ['11', '12']
                     '2': ['21', '22', '23']
                     '23': ['231', '232']
                     }
                (NOT IMPLEMENTED) dict of dicts, eg:
                {'<ROOT>': {'1': {'11': None,
                                  '12': None},
                            '2': {'21': None, 
                                  '22': None, 
                                  '23'" {'231': None,
                                         '232': None,}
                                  },
                }

        this_level (str): Key of tree level to start counting from
        count_type (str): Specifies which type of count to be returned:
                            all: Returns a count of all descendants below a node (children, grandchildren, ...)
                            first: Returns a count of only first-generation descendants for each node (children)
                            last: Returns a count of only last-generation descendants (those without children).  For 
                                    example:
                                        {'<ROOT>': ['1', '2'],
                                         '1': ['11', '12']
                                         '2': ['21', '22', '23']
                                         '23': ['231', '232']
                                         }
                                    would return:
                                        {'<ROOT>': 6, 
                                         '1': 2, 
                                         '2': 4, 
                                         '23': 2, 
                                         }

    Returns:
        (dict): Dict of {key: children_count} for all nodes from this level down (with counts returned according to
                count_type)
    """
    try:
        if isinstance(tree[this_level], list):
            children = tree[this_level]
        elif isinstance(tree[this_level], set):
            children = list(tree[this_level])
        elif isinstance(tree[this_level], dict):
            raise NotImplementedError("Not implemented.  Need code to know when at the bottom of a dict tree")
            # children = list(tree[this_level].keys())
        elif isinstance(tree[this_level], str):
            raise TypeError(
                "Lazy way to funnel strings into other type errors.  " 
                "Strings might not raise an error if node labels are integers")
        else:
            raise ValueError(f"Unknown data type in tree[{this_level}]")

        leaf_counts = {this_level: 0}
        for child in children:
            second_generation_counts = count_leaves_of_tree(tree, this_level=child, count_type=count_type)

            # Error check to make sure the dictionaries don't intersect
            if dictionaries_intersect(leaf_counts, second_generation_counts):
                raise ValueError("Error: redundancy found in tree - two parents have the same child")
            leaf_counts.update(second_generation_counts)

            if count_type == 'all':
                # Current level has this node plus any children under it
                leaf_counts[this_level] += leaf_counts[child] + 1
            elif count_type == 'first':
                leaf_counts[this_level] += 1
            elif count_type == 'last':
                # If child has children, take that count.  Otherwise, add 1 (as child is final-generation) 
                leaf_counts[this_level] += max(1, leaf_counts[child])
            else:
                raise ValueError(f'Invalid count_type {count_type}')

        return leaf_counts

    except (TypeError, KeyError):
        # This node has no children as it is not a reference to other nodes
        return {this_level: 0}


def count_future_generations(tree, this_level='<ROOT>'):
    try:
        if isinstance(tree[this_level], list):
            children = tree[this_level]
        elif isinstance(tree[this_level], set):
            children = list(tree[this_level])
        elif isinstance(tree[this_level], dict):
            raise NotImplementedError("Code exists for dictionary defined by a tree of dicts, but it was never tested")
            # children = list(tree[this_level].keys())
        elif isinstance(tree[this_level], str):
            raise TypeError(
                "Lazy way to funnel strings into other type errors.  " 
                "Strings might not raise an error if node labels are integers")
        else:
            raise ValueError(f"Unknown data type in tree[{this_level}]")

        max_depth = 0
        depths = {this_level: 0}
        for child in children:
            child_depths = count_future_generations(tree, this_level=child)
            if dictionaries_intersect(depths, child_depths):
                raise ValueError("Error: redundancy found in tree - two parents have the same child")
            depths.update(child_depths)
            depths[this_level] = max(depths[this_level], depths[child] + 1)

        return depths
    except (KeyError, TypeError):
        return {this_level: 0}

