# tests/profile_cli_test.py

from core import profile

def test_profile_summary_includes_name():
    summary = profile.profile_summary_for_prompt()
    assert "You are an assistant" in summary
    assert "The user you are helping is named" in summary

