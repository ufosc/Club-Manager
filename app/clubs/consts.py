"""
General constants and initial values for club items.
"""

from typing import TypedDict


class ClubRoleType(TypedDict):
    name: str
    default: bool
    permissions: list[str]


INITIAL_CLUB_ROLES: list[ClubRoleType] = [
    {
        "name": "Member",
        "default": True,
        "permissions": [
            "clubs.view_club",
            "clubs.view_event",
            "clubs.view_team",
        ],
    },
    {
        "name": "Officer",
        "default": False,
        "permissions": [
            "clubs.view_club",
            "clubs.change_club",
            "clubs.view_event",
            "clubs.change_event",
            "clubs.view_team",
            "clubs.change_team",
        ],
    },
]
