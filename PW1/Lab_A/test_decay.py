"""
Tests for the decay simulation.

One complete test is given as a model. Add the two tests described in the
lab handout (a negative-rate test, and a test against the analytical law).
Run with:  pytest -v
"""

import numpy as np
import pytest
from decay import simulate, simulate_loop


def test_starts_at_N0():
    # at time zero, no atoms have decayed yet
    assert simulate(1000, 0.4)[0] == 1000


def test_rejects_negative_rate():
    #   Check that calling simulate(...) with a negative lam raises a ValueError.
    with pytest.raises(ValueError):
        simulate(1000, -0.4)

#   Which pytest tool checks that an error is raised?
#   raises(name_of_error) helps to check if error is raised in spesific condition


def test_matches_law():
    #  Check that the simulation's AVERAGE over many seeds is close to the
    NO, lam = 10000, 0.4
    avg = np.mean([simulate(NO, lam, seed=i) for i in range(200)], axis=0)
    t = np.arange(len(avg))*0.05  #number of steps are interpreted as array from 1 to 200 and multiplied by 0.05 to get the correct intervals (0.05, 0.1, ...)
    expected = NO * np.exp(-lam*t)
    assert avg == pytest.approx(expected, rel=0.05)
    
#   physical law  N0 * exp(-lam * t).
#   Which pytest tool compares floating-point values with a tolerance?
#   pytest.approx() - compare floats with tolerance