#!/usr/bin/env python3
""" Permute beer script

Run directly from IPython with:

    run permute_general.py

When you want to move onto the more advanced tests:

    run permute_general.py
    test_random()  # Run the random test
    test_median()  # Run the median test
    test_alternative()  # Run the alternative test

Or - if you are brave, from the terminal command line:

    pytest permute_general
"""

import numpy as np

rng = np.random.default_rng()

import pandas as pd
pd.set_option('mode.copy_on_write', True)


# Load up example data frame
_mosquitoes = pd.read_csv('data/mosquito_beer.csv')
EG_DF = _mosquitoes[_mosquitoes['test'] == 'after']


def permutation_test(data,
                     group_col_name,
                     value_col_name,
                     summary_func='mean',
                     alternative='greater',
                     n_iters=10_000):
    groups = data[group_col_name]
    values = data[value_col_name]
    summarized = values.groupby(groups).agg(summary_func)
    actual_diff = np.diff(summarized)
    fake_diffs = np.zeros(n_iters)
    for i in range(n_iters):
        shuffled = rng.permutation(groups)
        means = values.groupby(shuffled).agg(summary_func)
        fake_diffs[i] = np.diff(means)
    if alternative == 'greater':  # First group is greater than second
        n_alt = np.count_nonzero(fake_diffs <= actual_diff)
    elif alternative == 'less':  # First group is less than second
        n_alt = np.count_nonzero(fake_diffs >= actual_diff)
    else:
        raise ValueError(f'Unexpected alternative "{alternative}"')
    return actual_diff, fake_diffs, n_alt / n_iters
