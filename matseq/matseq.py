def mult_mat_mat(*args):
    """Multiply two matrices for any indexable types."""
    if len(args) == 2:
        a, b = args
        return [[sum(ae*be for ae, be in zip(a_row, b_col)) for b_col in zip(*b)] for a_row in a]
    else:
        return mult_mat_mat(args[0], mult_mat_mat(*args[1:]))


def mult_mat_vec(a, b):
    """Multiply matrix times vector for any indexable types."""
    return [sum(ae*be for ae, be in zip(a_row, b)) for a_row in a]


def mult_vec_mat(a, b):
    """Multiply vector times matrix for any indexable types."""
    return [sum(ae*be for (ae, be) in zip(a, b_col)) for b_col in zip(*b)]


def mult_mat_scalar(a, s):
    return [[e*s for e in row] for row in a]