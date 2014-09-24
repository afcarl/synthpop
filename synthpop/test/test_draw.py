import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
from pandas.util import testing as pdt

from .. import draw


@pytest.fixture
def seed(request):
    current = np.random.get_state()

    def fin():
        np.random.set_state(current)
    request.addfinalizer(fin)

    np.random.seed(0)


@pytest.fixture
def index():
    return np.array(['v', 'w', 'x', 'y', 'z'], dtype=np.str_)


@pytest.fixture
def weights():
    return np.array([1, 2, 3, 4, 5])


@pytest.fixture
def num():
    return 10


def test_simple_draw(index, weights, num, seed):
    drawn_indexes = draw.simple_draw(num, weights, index)

    npt.assert_array_equal(
        drawn_indexes, ['y', 'z', 'y', 'y', 'y', 'y', 'y', 'z', 'z', 'x'])


def test_execute_draw():
    hh_df = pd.DataFrame(
        {'a': range(5),
         'b': range(5, 10),
         'serialno': [11, 22, 33, 44, 55]},
        index=pd.Index(['a', 'b', 'c', 'd', 'e'], name='hh_id'))

    pp_df = pd.DataFrame(
        {'x': range(100, 110),
         'y': range(110, 120),
         'serialno': [22, 33, 11, 55, 22, 33, 44, 55, 11, 33]},
        index=pd.Index(['q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']))

    indexes = ['c', 'a', 'd', 'e', 'a', 'c', 'e', 'e', 'a', 'c', 'e']

    synth_hh, synth_pp = draw.execute_draw(
        indexes, hh_df, pp_df, hh_index_start=1000)

    expected_index = pd.Index(range(1000, 1011))
    pdt.assert_index_equal(synth_hh.index, expected_index)
    pdt.assert_series_equal(
        synth_hh.serialno,
        pd.Series(
            [33, 11, 44, 55, 11, 33, 55, 55, 11, 33, 55],
            index=expected_index))
    assert list(synth_hh.columns) == ['a', 'b', 'serialno']

    pdt.assert_index_equal(synth_pp.index, pd.Index(range(24)))
    pdt.assert_series_equal(
        synth_pp.serialno,
        pd.Series(([33] * 9) + ([11] * 6) + ([55] * 8) + [44]))
    pdt.assert_series_equal(
        synth_pp.hh_id,
        pd.Series(
            ([1000, 1005, 1009] * 3) + ([1001, 1004, 1008] * 2) +
            ([1003, 1006, 1007, 1010] * 2) + [1002]))


def test_compare_to_constraints_exact():
    constraints = pd.Series([1, 3, 2], index=['a', 'b', 'c'])
    synth = pd.Series(['a', 'c', 'b', 'c', 'b', 'b'])

    chisq, p = draw.compare_to_constraints(synth, constraints)

    assert chisq == 0
    assert p == 1


def test_compare_to_constraints():
    constraints = pd.Series([1, 1, 2, 1, 3], index=['a', 'b', 'c', 'd', 'e'])
    synth = pd.Series(['e', 'a', 'e', 'e', 'c', 'e'])

    chisq, p = draw.compare_to_constraints(synth, constraints)
