# core/profile.py

"""
User Profile Management

Stores and loads a user profile to personalize agent behavior.

Author: Shay Neufeld
"""

import os
import json
from typing import Dict, Any

PROFILE_PATH = os.path.join("data", "profile.json")
os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)

DEFAULT_PROFILE = {
    "name": "Shay",
    "location": "Vancouver",
    "interests": ["neuroscience", "biotech", "SaaS", "jazz piano"],
    "preferences": {"response_style": "concise and professional"},
}


def load_profile() -> Dict[str, Any]:
    if not os.path.exists(PROFILE_PATH):
        save_profile(DEFAULT_PROFILE)
        return DEFAULT_PROFILE
    with open(PROFILE_PATH, "r") as f:
        return json.load(f)


def save_profile(profile: Dict[str, Any]) -> None:
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=2)


def format_profile_as_context(profile: Dict[str, Any]) -> str:
    name = profile.get("name", "the user")
    location = profile.get("location", "")
    interests = profile.get("interests", [])
    style = profile.get("preferences", {}).get("response_style", "")

    parts = [f"The user's name is {name}."]
    if location:
        parts.append(f"They are based in {location}.")
    if interests:
        parts.append(f"Their interests include: {', '.join(interests)}.")
    if style:
        parts.append(f"Please respond in a {style} style.")

    return "\n".join(parts)


# core/profile.py

def create_system_message(profile: dict) -> str:
    """
    Build a system message string incorporating user profile info.

    Args:
        profile (dict): User profile loaded from profile.json

    Returns:
        str: System prompt describing user info and behavior instructions
    """
    interests = ", ".join(profile.get("interests", []))
    style = profile.get("preferences", {}).get("response_style", "concise and professional")
    name = profile.get("name", "User")

    system_msg = (
        "You are a helpful assistant. "
        "Use the following information to personalize your responses:\n"
        f"User's name: {name}\n"
        f"Interests: {interests}\n"
        f"Preferred response style: {style}\n"
        "Only use external tools like search if the user's question requires "
        "information beyond what you confidently know or the user profile."
    )
    return system_msg

