from maxbot import *
from pytest import approx, mark


def test_simpleparse():
    msg = 'I\'ll be on in 15 minutes'
    seconds = views.parse_message(msg)
    assert seconds/60 == approx(15,.1)

def test_failure():
    msg = 'be on soon'
    assert views.parse_message(msg) is None