import pytest
from ...synthesizer import *
from ..starter2 import Starter as Starter2


@pytest.fixture
def key():
    return "827402c2958dcf515e4480b7b2bb93d1025f9389"


# def test_starter2(key):
#     st = Starter2(key, "CA", "Napa County")
#     synthesize_all(st, num_geogs=1)