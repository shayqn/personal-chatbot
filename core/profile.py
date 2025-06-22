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
    if not os.path.exists(PROFILE_PATH):
        save_profile(DEFAULT_PROFILE)
        return DEFAULT_PROFILE.copy()
    with open(PROFILE_PATH, "r") as f:
        return json.load(f)

def save_profile(profile: Dict[str, Any]) -> None:
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=2)

def update_profile_field(field: str, value: Any) -> None:
    profile = load_profile()
    profile[field] = value
    save_profile(profile)

def add_interest(interest: str) -> None:
    profile = load_profile()
    interests = profile.get("interests", [])
    if interest not in interests:
        interests.append(interest)
        profile["interests"] = interests
        save_profile(profile)

def profile_summary_for_prompt() -> str:
    profile = load_profile()
    name = profile.get("name", "User")
    interests = ", ".join(profile.get("interests", []))
    style = profile.get("preferences", {}).get("response_style", "")
    return (
        f"User's name is {name}. "
        f"Interests include: {interests}. "
        f"Preferred response style: {style}."
    )
