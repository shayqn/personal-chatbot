# core/profile.py

"""
User Profile Management and System Message Construction

Manages loading, saving, and formatting user profile information
for personalized system prompts.

Author: Shay Neufeld
"""

import os
import json
from typing import Dict, Any

PROFILE_PATH = os.path.join("data", "profile.json")
os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)

DEFAULT_PROFILE = {
    "name": "Shay",
    "interests": ["neuroscience", "biotech", "SaaS", "jazz piano"],
    "preferences": {
        "response_style": "concise and professional"
    }
}


def load_profile() -> Dict[str, Any]:
    """
    Load the user profile from disk, or create default profile if none exists.

    Returns:
        Dict[str, Any]: User profile dictionary.
    """
    if not os.path.exists(PROFILE_PATH):
        save_profile(DEFAULT_PROFILE)
        return DEFAULT_PROFILE.copy()
    with open(PROFILE_PATH, "r") as f:
        return json.load(f)


def save_profile(profile: Dict[str, Any]) -> None:
    """
    Save the user profile to disk.

    Args:
        profile (Dict[str, Any]): Profile dictionary to save.
    """
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=2)


def create_system_message(profile: Dict[str, Any]) -> str:
    """
    Build a system message string incorporating user profile info.

    Args:
        profile (Dict[str, Any]): User profile dictionary.

    Returns:
        str: System prompt describing user info and behavior instructions.
    """
    name = profile.get("name", "User")
    interests = ", ".join(profile.get("interests", []))
    style = profile.get("preferences", {}).get("response_style", "helpful and friendly")

    system_msg = (
        "You are a helpful assistant. "
        "Use the following information to personalize your responses:\n"
        f"User's name: {name}\n"
        f"Interests: {interests}\n"
        f"Preferred response style: {style}\n"
        "Only use external tools like search if the user's question requires information beyond what you confidently know or the user profile."
    )
    return system_msg
