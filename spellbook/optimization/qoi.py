#!/usr/bin/env python3
##############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other
# Merlin-Spellbook Project developers. See top-level LICENSE and COPYRIGHT
# files for dates and other details. No copyright assignment is required to
# contribute to Merlin-Spellbook.
##############################################################################

import numpy as np

from spellbook.utils import load_infile


""" Construct a quantity of interest (cost function) for use in optimization"""


def barrier(x, threshold, threshold_type="greater"):
    """Implement the 'barrier penalty' function from Haftka and Starnes, AIAA Journal 14 (6): 718 (1976).

    x is the quantity
    threshold is the constraint threshold
    threshold_type: one of "greater" or "less"

    Note: this is just the penalty term, which must be combined with the objective
    Use this with make_barrier_qoi to apply them

    """
    C = 3e-1
    p = 1.0 / 3.0

    if threshold_type == "less":
        xx = -1.0 * x
        threshold = -1.0 * threshold
    elif threshold_type == "greater":
        xx = 1.0 * x
    else:
        raise ValueError("threshold_type must be one of 'greater' or 'less'")

    penalty = np.zeros_like(xx)
    sign_x = np.sign(xx)
    g0 = C * np.abs(xx) ** p
    gi = xx - threshold
    group1 = gi > g0
    group2 = gi <= g0
    group3 = xx >= threshold

    penalty[group1] = sign_x[group1] * xx[group1] / gi[group1]
    penalty[group2] = (
        sign_x[group2]
        * xx[group2]
        * ((1.0 / g0[group2]) * ((gi[group2] / g0[group2]) ** 2 - 3.0 * (gi[group2] / g0[group2]) + 3.0))
    )
    penalty[group3] = 0.0

    return penalty


def min_max_norm(x):
    minx = np.min(x)
    maxx = np.max(x)
    if minx == maxx:
        return np.ones(x.shape)
    return (x - minx) / (maxx - minx)


def make_barrier_qoi(f, g_constraints, maximize=False):
    """Constructs a cost function for f optimization with barrier penalty constraints.

    Returns the qoi cost function suitable for either minimization (if maximize==False: default)
    or maximization (if maximize==True)

    Each constraint in g_constraints applies a barrier penalty.
    g_constraints are a tuple of tuples with g, threshold, threshold_type

    f and g are discrete arrays

    to pass in to optimizing functions, could fit a surrogate model to cost_qoi

    Example:

    f = x*x+4*x

    gs = ((x*x,9,'less'),
          (x,-2,'greater'),
          (np.sin(x),0,'greater'))

    cost_qoi = make_barrier_qoi(f, gs)

    plt.plot(x,cost_qoi)
    best = cost_qoi.argmin()
    plt.plot(x[best],cost_qoi[best],'*')
    plt.plot(x[best],f[best],'*')

    cost_2 = make_barrier_qoi(f, gs, maximize=True)
    best2 = cost_2.argmax()
    plt.plot(x[best2], f[best2], 'o')

    """
    # Need to normalize constraints and f to be similar scales
    # Also make sure we are all 1D arrays (via ravel)
    # And flip the sign if we are maximizing
    if maximize:
        qoi = -1.0 * min_max_norm(f).ravel()
    else:
        qoi = min_max_norm(f).ravel()

    # Now add the penalty terms (which assume minimization)
    for g, threshold, threshold_type in g_constraints:
        penalty = barrier(g.ravel(), threshold, threshold_type)
        norm_penalty = min_max_norm(penalty)
        qoi += norm_penalty

    # If we are not minimizing, then we undo the negative transformation
    # so that we return a function that has the same sign as the original
    if maximize:
        qoi *= -1.0

    # set dimensions to be consistent w/ sklearn
    qoi = np.atleast_2d(qoi).T
    return qoi


def parse_constraints(constraint_args, data):
    """Pull the constraints from the loaded data, translating the arguments.

    args are in strings of form
        c1<4.0,c5>68.9
    """
    if constraint_args is None:
        return []
    constraint_data = []
    constraints = constraint_args.split(",")
    for constraint in constraints:
        if "<" in constraint:
            threshold_type = "less"
            splitter = "<"
        elif ">" in constraint:
            threshold_type = "greater"
            splitter = ">"
        else:
            raise ValueError('Bad constraint format: must be "name<value" or "name>value"')
        name, value_name = constraint.split(splitter)
        value = float(value_name)
        constraint_data.append((data[name], value, threshold_type))
    return constraint_data


def process_args(args):
    input_file = args.infile
    output_file = args.outfile
    x_variables = args.X
    objective_name = args.objective
    maximize = args.maximize_objective
    constraint_metadata = args.constraints
    data = np.load(input_file)
    x, f = load_infile(input_file, x_variables, objective_name)
    constraints = parse_constraints(constraint_metadata, data)
    qoi = make_barrier_qoi(f, constraints, maximize)
    np.savez(output_file, X=x, y=qoi)
