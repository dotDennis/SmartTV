"""
Unit tests for logic.tv.SmartTV
===============================

These tests validate the SmartTV class, ensuring that the
core device logic (power state and channel management)
works as expected.

Author: dotDennis
Course: IDATA2304
"""

import pytest
from logic.tv import SmartTV


def test_tv_is_off_by_default():
    """TV should start powered OFF by default."""
    tv = SmartTV()
    assert tv.is_on() is False


def test_turn_on_and_off():
    """Turning the TV ON and OFF should toggle its state correctly."""
    tv = SmartTV()
    tv.turn_on()
    assert tv.is_on() is True
    tv.turn_off()
    assert tv.is_on() is False


def test_default_channel_and_count():
    """TV should default to channel 1 and have 10 available channels."""
    tv = SmartTV()
    assert tv.get_channel_count() == 10
    assert tv.get_channel() == 1


def test_set_channel_valid():
    """Setting a valid channel number should update the current channel."""
    tv = SmartTV()
    tv.set_channel(5)
    assert tv.get_channel() == 5


@pytest.mark.parametrize("bad", [0, 11, -1, 999])
def test_set_channel_out_of_range_raises(bad):
    """Setting a channel outside 1–10 should raise ValueError."""
    tv = SmartTV()
    with pytest.raises(ValueError):
        tv.set_channel(bad)