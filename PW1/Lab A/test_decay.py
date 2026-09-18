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


# TODO 1: test_rejects_negative_rate
#   Check that calling simulate(...) with a negative lam raises a ValueError.
#   Which pytest tool checks that an error is raised?


# TODO 2: test_matches_law
#   Check that the simulation's AVERAGE over many seeds is close to the
#   physical law  N0 * exp(-lam * t).
#   Which pytest tool compares floating-point values with a tolerance?
import pytest
import numpy as np
import decay

# 1. Negatif oran verildiğinde ValueError fırlatıldığını kontrol eden test
def test_negative_rate_raises_valueerror():
    with pytest.raises(ValueError):
        decay.simulate(1000, -0.4)

# 2. Çok sayıda simülasyonun ortalamasının teorik $N_0 e^{-\lambda t}$ değerine yakınlığını kontrol eden test
def test_simulation_average_close_to_theory():
    N0 = 1000
    rate = 0.4
    t = 1.0
    expected = N0 * np.exp(-rate * t)
    
    # t=1.0 anına denk gelen 10. indeksi ([10]) alıyoruz
    simulations = [decay.simulate(N0, rate)[20] for _ in range(500)]
    avg_result = np.mean(simulations)
    
    assert avg_result == pytest.approx(expected, rel=1e-1)