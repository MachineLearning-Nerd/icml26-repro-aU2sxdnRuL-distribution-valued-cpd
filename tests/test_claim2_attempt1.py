import numpy as np

from src.claim2_attempt1_empirical_arl import empirical_upper, run_length


def test_empirical_upper_uses_documented_order_statistic():
    values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    # ceil((1-.2)*5)=4: one-indexed fourth order statistic.
    assert empirical_upper(values, 0.2) == 4.0


def test_run_length_is_one_based_and_uses_union_alarm():
    t2 = np.array([0.1, 0.2, 1.1])
    spe = np.array([0.1, 1.1, 0.2])
    assert run_length(t2, spe, 1.0, 1.0) == 2


def test_no_alarm_returns_horizon_plus_one():
    assert run_length(np.zeros(3), np.zeros(3), 1.0, 1.0) == 4
