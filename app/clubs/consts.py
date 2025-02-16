"""
General constants and initial values for club items.
"""

from typing import TypedDict


class ClubRoleType(TypedDict):
    role_name: str
    default: bool
    permissions: list[str]


INITIAL_CLUB_ROLES: list[ClubRoleType] = [
    {
        "role_name": "Member",
        "default": True,
        "permissions": [
            "clubs.view_club",
        ],
    },
    {
        "role_name": "Officer",
        "default": False,
        "permissions": [
            "clubs.view_club",
            "clubs.change_club",
        ]
    }
]
