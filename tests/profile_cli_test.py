# tests/profile_cli_test.py

from core import profile

def test_profile_summary_includes_name():
    summary = profile.profile_summary_for_prompt()
    assert summary.startswith("You are an assistant")
    assert "the user's name is" in summary.lower()
    assert "interests include" in summary.lower()

