"""
Unit tests for handler.handle_command
=====================================

These tests ensure that the command handler interprets
raw text commands correctly and returns expected responses.

Author: dotDennis
Course: IDATA2304
"""

import pytest
from handler import handle_command
from config import APP_NAME, APP_VERSION


def test_empty_command():
    """Empty input should trigger an 'Empty command' error."""
    assert "Empty command" in handle_command("   ")


def test_help_contains_key_lines():
    """Help output should include key commands and descriptions."""
    out = handle_command("help")
    assert "Supported commands" in out
    assert "set_ch <n>" in out
    assert "version" in out


def test_version_uses_config():
    """Version command should return APP_NAME and APP_VERSION from config."""
    out = handle_command("version")
    assert f"{APP_NAME}-{APP_VERSION}" == out


def test_on_off_status_texts_exist():
    """ON, OFF, and status commands should return appropriate strings."""
    assert "ON" in handle_command("on")
    assert "OFF" in handle_command("off")
    assert isinstance(handle_command("status"), str)


def test_get_c_and_get_ch_current_impl():
    """
    get_c and get_ch should return current placeholder responses
    as implemented in the handler.
    """
    assert "channel 1" in handle_command("get_c").lower()
    assert "10" in handle_command("get_ch") and "available" in handle_command("get_ch").lower()


def test_set_ch_ok():
    """Valid set_ch command should confirm the new channel."""
    out = handle_command("set_ch 3")
    assert "Channel set to 3" == out


@pytest.mark.parametrize("bad", ["set_ch", "set_ch 1 2", "set_ch x"])
def test_set_ch_errors(bad):
    """Invalid set_ch usage should return an appropriate error message."""
    out = handle_command(bad)
    assert any(
        key in out
        for key in [
            "expected 1 argument",
            "Invalid channel number",
            "Channel out of range",
        ]
    )


def test_set_ch_out_of_range_message():
    """set_ch should warn clearly when the channel is out of range."""
    out = handle_command("set_ch 42")
    assert "out of range" in out and ("1-10" in out or "1–10" in out)


def test_unknown_command_message_is_clear():
    """Unknown commands should return an explicit error message."""
    out = handle_command("blargh")
    assert "unknown command" in out.lower() or "unkown command" in out.lower()


def test_argless_commands_reject_extra_args():
    """Argless commands should fail if extra arguments are provided."""
    for cmd in ["help", "version", "on", "off", "status", "get_c", "get_ch", "quit"]:
        out = handle_command(f"{cmd} 123")
        assert "expected 0 arguments" in out